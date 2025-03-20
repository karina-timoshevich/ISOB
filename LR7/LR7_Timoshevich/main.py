import re
import random
import string
import keyword
import builtins
import base64


def rename_identifiers(code):
    reserved = set(keyword.kwlist) | set(dir(builtins))
    code_clean = re.sub(r'(\"|\').*?(\1)', '', code, flags=re.DOTALL)
    code_clean = re.sub(r'#.*', '', code_clean)
    identifiers = re.findall(r'\b(?!def\b|class\b)([a-zA-Z_][a-zA-Z0-9_]*)\b', code_clean)
    identifiers = {name for name in identifiers if name not in reserved}
    replacements = {name: ''.join(random.choices(string.ascii_letters, k=8)) for name in identifiers}
    for old, new in replacements.items():
        code = re.sub(r'\b{}\b'.format(re.escape(old)), new, code)
    return code


def add_junk(code):
    junk_templates = [
        '    for _ in range(10): pass\n',
        '    print("Junk: {}".format(random.randint(0, 100)))\n',
        '    x = [i**2 for i in range(100) if i % 3 == 0]\n'
    ]
    lines = code.split('\n')
    for _ in range(3):
        pos = random.randint(0, len(lines))
        lines.insert(pos, random.choice(junk_templates))
    return '\n'.join(lines)


def encrypt_strings(code):
    strings = re.findall(r'"(.*?)"', code)
    for s in strings:
        encoded = base64.b64encode(s.encode()).decode()
        code = code.replace(f'"{s}"', f'base64.b64decode("{encoded}").decode()')
    return code


def obfuscate(code):
    code = rename_identifiers(code)
    code = add_junk(code)
    code = encrypt_strings(code)
    return code


source_code = '''
def calculate(a, b):
    result = a + b
    print("Result:", result)
    return result

calculate(5, 3)
'''

obfuscated_code = obfuscate(source_code)
print(obfuscated_code)

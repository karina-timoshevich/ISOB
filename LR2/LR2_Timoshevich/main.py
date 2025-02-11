def caesar_encrypt(text, shift, language='en'):
    encrypted_text = []

    if language == 'ru':
        upper_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        lower_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        alphabet_size = 33
    else:
        upper_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lower_alphabet = 'abcdefghijklmnopqrstuvwxyz'
        alphabet_size = 26

    for char in text:
        if char in upper_alphabet:
            idx = upper_alphabet.index(char)
            new_idx = (idx + shift) % alphabet_size
            encrypted_text.append(upper_alphabet[new_idx])
        elif char in lower_alphabet:
            idx = lower_alphabet.index(char)
            new_idx = (idx + shift) % alphabet_size
            encrypted_text.append(lower_alphabet[new_idx])
        else:
            encrypted_text.append(char)

    return ''.join(encrypted_text)


def caesar_decrypt(text, shift, language='en'):
    return caesar_encrypt(text, -shift, language)


def encrypt_file_caesar(input_file, output_file, shift, language='en'):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    encrypted_text = caesar_encrypt(text, shift, language)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(encrypted_text)


def decrypt_file_caesar(input_file, output_file, shift, language='en'):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    decrypted_text = caesar_decrypt(text, shift, language)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(decrypted_text)


def vigenere_encrypt(text, key, language='en'):
    encrypted_text = []

    if language == 'ru':
        upper_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        lower_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        alphabet_size = 33
    else:
        upper_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lower_alphabet = 'abcdefghijklmnopqrstuvwxyz'
        alphabet_size = 26

    key_idx = 0
    for char in text:
        if char in upper_alphabet:
            shift = upper_alphabet.index(key[key_idx % len(key)].upper())
            new_idx = (upper_alphabet.index(char) + shift) % alphabet_size
            encrypted_text.append(upper_alphabet[new_idx])
            key_idx += 1
        elif char in lower_alphabet:
            shift = lower_alphabet.index(key[key_idx % len(key)].lower())
            new_idx = (lower_alphabet.index(char) + shift) % alphabet_size
            encrypted_text.append(lower_alphabet[new_idx])
            key_idx += 1
        else:
            encrypted_text.append(char)

    return ''.join(encrypted_text)


def vigenere_decrypt(text, key, language='en'):
    decrypted_text = []

    if language == 'ru':
        upper_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        lower_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        alphabet_size = 33
    else:
        upper_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lower_alphabet = 'abcdefghijklmnopqrstuvwxyz'
        alphabet_size = 26

    key_idx = 0
    for char in text:
        if char in upper_alphabet:
            shift = upper_alphabet.index(key[key_idx % len(key)].upper())
            new_idx = (upper_alphabet.index(char) - shift) % alphabet_size
            decrypted_text.append(upper_alphabet[new_idx])
            key_idx += 1
        elif char in lower_alphabet:
            shift = lower_alphabet.index(key[key_idx % len(key)].lower())
            new_idx = (lower_alphabet.index(char) - shift) % alphabet_size
            decrypted_text.append(lower_alphabet[new_idx])
            key_idx += 1
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)



def encrypt_file_vigenere(input_file, output_file, key, language='en'):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    encrypted_text = vigenere_encrypt(text, key, language)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(encrypted_text)


def decrypt_file_vigenere(input_file, output_file, key, language='en'):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    decrypted_text = vigenere_decrypt(text, key, language)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(decrypted_text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    shift = 3
    encrypt_file_caesar('input.txt', 'encrypted_caesar.txt', shift, language='ru')
    decrypt_file_caesar('encrypted_caesar.txt', 'decrypted_caesar.txt', shift, language='ru')

    key = "ключ"
    encrypt_file_vigenere('input.txt', 'encrypted_vigenere.txt', key, language='ru')
    decrypt_file_vigenere('encrypted_vigenere.txt', 'decrypted_vigenere.txt', key, language='ru')


import sqlite3


def create_database():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    users = [
        ('admin', 'secure_password'),
        ('user1', 'password123'),
        ('user2', 'qwerty')
    ]
    cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)
    conn.commit()
    return conn


def unsafe_login(conn, username, password):
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"[Уязвимый запрос] Выполняется запрос: {query}")
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        print(f"[Уязвимый запрос] Найден пользователь: {result}")
        return True
    else:
        print("[Уязвимый запрос] Пользователь не найден")
        return False


def safe_login(conn, username, password):
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f"[Безопасный запрос] Выполняется запрос: {query} с параметрами ({username}, {password})")
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    if result:
        print(f"[Безопасный запрос] Найден пользователь: {result}")
        return True
    else:
        print("[Безопасный запрос] Пользователь не найден")
        return False


def demonstration():
    conn = create_database()

    # Пример корректного входа
    print("\n=== Попытка корректного входа ===")
    if safe_login(conn, 'admin', 'secure_password'):
        print("Вход выполнен успешно!")
    else:
        print("Ошибка входа.")

    # Пример SQL-инъекции
    evil_password = "' OR '1'='1"
    print("\n=== Попытка SQL-инъекции ===")
    print(f"Используем зловредный пароль: {evil_password}")

    print("\n--- Уязвимая проверка ---")
    if unsafe_login(conn, 'admin', evil_password):
        print("Успешный взлом! SQL-инъекция сработала.")
    else:
        print("Вход отклонен.")

    print("\n--- Безопасная проверка ---")
    if safe_login(conn, 'admin', evil_password):
        print("Вход выполнен.")
    else:
        print("SQL-инъекция предотвращена!")


if __name__ == "__main__":
    demonstration()
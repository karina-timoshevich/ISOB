import socket
import threading

HOST = '0.0.0.0'
PORT = 12345
MAX_CONNECTIONS = 5
client_threads = []


def handle_client(client_socket, client_address):
    print(f"[INFO] Подключен клиент: {client_address}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"[{client_address}] Получено: {data.decode('utf-8')}")
            client_socket.sendall(data)
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
    finally:
        print(f"[INFO] Отключение {client_address}")
        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)
    print(f"[INFO] Сервер запущен на {HOST}:{PORT}")

    try:
        while True:
            print("[INFO] Ожидание подключения...")
            client_socket, client_address = server_socket.accept()
            print(f"[INFO] Подключен клиент: {client_address}")

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True
            client_thread.start()
            client_threads.append(client_thread)

    except KeyboardInterrupt:
        print("\n[INFO] Остановка сервера...")
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
    finally:
        print("[INFO] Закрытие всех соединений...")
        for thread in client_threads:
            thread.join(timeout=1)
        server_socket.close()
        print("[INFO] Сервер остановлен.")


if __name__ == "__main__":
    start_server()

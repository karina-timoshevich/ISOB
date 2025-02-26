import socket
import threading
import time

HOST = '0.0.0.0'
PORT = 12345
MAX_CONNECTIONS = 5
TIMEOUT = 5
ip_connections = {}

lock = threading.Lock()


def handle_client(client_socket, client_address):
    ip = client_address[0]
    print(f"[INFO] Подключен клиент: {client_address}")

    client_socket.settimeout(TIMEOUT)

    try:
        data = client_socket.recv(1024)
        if not data:
            raise Exception("Пустое сообщение")

        print(f"[{client_address}] Получено: {data.decode('utf-8')}")
        client_socket.sendall(data)

    except socket.timeout:
        print(f"[WARNING] Таймаут клиента {client_address}")
    except Exception as e:
        print(f"[ERROR] {client_address}: {e}")

    finally:
        with lock:
            ip_connections[ip] -= 1
            if ip_connections[ip] == 0:
                del ip_connections[ip]

        print(f"[INFO] Отключение {client_address}")
        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)

    print(f"[INFO] Защищенный сервер запущен на {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            ip = client_address[0]

            with lock:
                if ip in ip_connections and ip_connections[ip] >= 2:
                    print(f"[WARNING] {ip} пытается создать слишком много соединений!")
                    client_socket.close()
                    continue
                ip_connections[ip] = ip_connections.get(ip, 0) + 1

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True
            client_thread.start()

    except KeyboardInterrupt:
        print("[INFO] Остановка сервера")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()

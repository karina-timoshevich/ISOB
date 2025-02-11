import json
import time
import base64
import hashlib
from cryptography.fernet import Fernet


def derive_key(password):
    hash_digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hash_digest)


class AuthServer:
    def __init__(self, tgs_key):
        self.registered_clients = {}
        self.tgs_key = tgs_key

    def add_client(self, client_name, password):
        self.registered_clients[client_name] = derive_key(password)

    def generate_tgt(self, client_name):
        if client_name not in self.registered_clients:
            raise ValueError("Unknown client")
        client_key = self.registered_clients[client_name]
        session_key = Fernet.generate_key()
        timestamp = int(time.time())
        tgt_payload = {
            'client': client_name,
            'session_key': session_key.decode(),
            'timestamp': timestamp,
            'validity': 3600
        }
        encrypted_tgt = Fernet(self.tgs_key).encrypt(json.dumps(tgt_payload).encode())
        response = {
            'session_key': session_key.decode(),
            'tgt': encrypted_tgt.decode(),
            'timestamp': timestamp,
            'validity': 3600
        }
        return Fernet(client_key).encrypt(json.dumps(response).encode())


class TicketServer:
    def __init__(self, tgs_key):
        self.tgs_key = tgs_key
        self.services = {}

    def add_service(self, service_name, service_key):
        self.services[service_name] = service_key

    def generate_service_ticket(self, tgt, authenticator, service_name):
        decrypted_tgt = json.loads(Fernet(self.tgs_key).decrypt(tgt).decode())
        session_key = decrypted_tgt['session_key'].encode()
        client_name = decrypted_tgt['client']

        auth_data = json.loads(Fernet(session_key).decrypt(authenticator).decode())
        if auth_data['client'] != client_name:
            raise ValueError("Client mismatch")
        if time.time() - auth_data['timestamp'] > 30:
            raise ValueError("Authenticator expired")
        if service_name not in self.services:
            raise ValueError("Service not found")

        service_key = self.services[service_name]
        service_session_key = Fernet.generate_key()
        ticket_payload = {
            'client': client_name,
            'service_session_key': service_session_key.decode(),
            'timestamp': int(time.time()),
            'validity': 3600
        }
        encrypted_ticket = Fernet(service_key).encrypt(json.dumps(ticket_payload).encode())

        response = {
            'service_session_key': service_session_key.decode(),
            'service_ticket': encrypted_ticket.decode()
        }
        return Fernet(session_key).encrypt(json.dumps(response).encode())


class ServiceServer:
    def __init__(self, service_key):
        self.service_key = service_key

    def authenticate_request(self, service_ticket, authenticator):
        ticket_data = json.loads(Fernet(self.service_key).decrypt(service_ticket).decode())
        session_key = ticket_data['service_session_key'].encode()
        client_name = ticket_data['client']

        auth_data = json.loads(Fernet(session_key).decrypt(authenticator).decode())
        if auth_data['client'] != client_name:
            raise ValueError("Client mismatch")
        if time.time() - auth_data['timestamp'] > 30:
            raise ValueError("Authenticator expired")
        return True


if __name__ == "__main__":
    tgs_master_key = Fernet.generate_key()
    service_master_key = Fernet.generate_key()

    auth_server = AuthServer(tgs_master_key)
    ticket_server = TicketServer(tgs_master_key)
    service_server = ServiceServer(service_master_key)

    auth_server.add_client("bob", "securepass")
    ticket_server.add_service("data_storage", service_master_key)

    client = type('', (), {})()
    client.name = "bob"
    client.password = "securepass"
    client.key = derive_key(client.password)

    tgt_response = auth_server.generate_tgt(client.name)
    decrypted_tgt = json.loads(Fernet(client.key).decrypt(tgt_response).decode())

    client.session_key = decrypted_tgt['session_key'].encode()
    client.tgt = decrypted_tgt['tgt'].encode()

    authenticator = Fernet(client.session_key).encrypt(
        json.dumps({'client': client.name, 'timestamp': int(time.time())}).encode()
    )

    service_response = ticket_server.generate_service_ticket(client.tgt, authenticator, "data_storage")
    decrypted_service_data = json.loads(Fernet(client.session_key).decrypt(service_response).decode())

    client.service_session_key = decrypted_service_data['service_session_key'].encode()
    client.service_ticket = decrypted_service_data['service_ticket'].encode()

    final_authenticator = Fernet(client.service_session_key).encrypt(
        json.dumps({'client': client.name, 'timestamp': int(time.time())}).encode()
    )

    print("Authentication successful:", service_server.authenticate_request(client.service_ticket, final_authenticator))

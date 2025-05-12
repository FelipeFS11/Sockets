import socket
import threading
from cryptography.fernet import Fernet

clients = {}
keys = {}
lock = threading.Lock()

def broadcast(message, sender_socket=None):
    with lock:
        for client, name in clients.items():
            if client != sender_socket:
                try:
                    encrypted_msg = keys[client].encrypt(message.encode())
                    client.send(encrypted_msg)
                except:
                    client.close()
                    del clients[client]
                    del keys[client]

def handle_client(client_socket):
    try:
        # Gerar e enviar chave Fernet
        key = Fernet.generate_key()
        fernet = Fernet(key)
        client_socket.send(key)

        # Receber nome de usuário criptografado
        encrypted_username = client_socket.recv(1024)
        username = fernet.decrypt(encrypted_username).decode()

        with lock:
            clients[client_socket] = username
            keys[client_socket] = fernet

        broadcast(f"{username} entrou no chat.", client_socket)

        while True:
            encrypted_msg = client_socket.recv(1024)
            msg = fernet.decrypt(encrypted_msg).decode()

            if msg.startswith("/msg "):
                target_name, _, private_msg = msg[5:].partition(" ")
                with lock:
                    for c, n in clients.items():
                        if n == target_name:
                            private_encrypted = keys[c].encrypt(f"[PM de {username}]: {private_msg}".encode())
                            c.send(private_encrypted)
                            break
            else:
                broadcast(f"{username}: {msg}", client_socket)
    except:
        pass
    finally:
        with lock:
            name = clients.get(client_socket, "Desconhecido")
            del clients[client_socket]
            del keys[client_socket]
        broadcast(f"{name} saiu do chat.")
        client_socket.close()

def start_server(host='localhost', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Servidor ouvindo em {host}:{port}...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão de {addr}")
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    start_server()

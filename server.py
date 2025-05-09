import socket
import threading

clients = {}
lock = threading.Lock()

def broadcast(message, sender_socket=None):
    with lock:
        for client, name in clients.items():
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except:
                    client.close()
                    del clients[client]

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode()
        with lock:
            clients[client_socket] = username
        broadcast(f"{username} entrou no chat.", client_socket)

        while True:
            msg = client_socket.recv(1024).decode()
            if msg.startswith("/msg "):
                target_name, _, private_msg = msg[5:].partition(" ")
                with lock:
                    for c, n in clients.items():
                        if n == target_name:
                            c.send(f"[PM de {username}]: {private_msg}".encode())
                            break
            else:
                broadcast(f"{username}: {msg}", client_socket)
    except:
        pass
    finally:
        with lock:
            name = clients.get(client_socket, "Desconhecido")
            del clients[client_socket]
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

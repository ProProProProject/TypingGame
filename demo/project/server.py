import socket
import threading

clients = []
lock = threading.Lock()
game_text = "Typing Race Multiplayer! Let's see who types the fastest!"

def broadcast_positions():
    while True:
        data = "UPDATE|" + "|".join(f"{i}:{c['progress']}" for i, c in enumerate(clients))
        for client in clients:
            try:
                client['conn'].sendall(data.encode())
            except:
                pass

def handle_client(conn, addr, index):
    conn.sendall(f"TEXT|{game_text}".encode())
    while True:
        try:
            msg = conn.recv(1024).decode()
            if msg.startswith("PROGRESS|"):
                typed = msg.split("|")[1]
                with lock:
                    clients[index]['progress'] = len(typed)
        except:
            break
    conn.close()
    with lock:
        clients.pop(index)

def main():
    host = '0.0.0.0'
    port = 50007
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(4)
    print("Server listening on port 50007")

    threading.Thread(target=broadcast_positions, daemon=True).start()

    while True:
        conn, addr = server.accept()
        with lock:
            if len(clients) >= 4:
                conn.sendall("FULL".encode())
                conn.close()
                continue
            index = len(clients)
            clients.append({'conn': conn, 'addr': addr, 'progress': 0})
            threading.Thread(target=handle_client, args=(conn, addr, index), daemon=True).start()

if __name__ == "__main__":
    main()

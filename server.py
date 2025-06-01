# server.py
import socket
import threading
import time
import compair

clients = {'Player 1': 0, 'Player 2': 0, 'Player 3': 0, 'Player 4': 0}
client_sockets = {}
positions = {'Player 1': 50, 'Player 2': 50, 'Player 3': 50, 'Player 4': 50}
gameEnd = 'False:None'

def broadcast_combined():
    data = f"BROADCAST|{positions['Player 1']},{positions['Player 2']},{positions['Player 3']},{positions['Player 4']}|{gameEnd}"
    for sock in client_sockets.values():
        try:
            sock.send((data + '\n').encode('utf-8'))  # 注意 \n
        except:
            pass

def periodic_broadcast():
    while True:
        broadcast_combined()
        time.sleep(0.3)  # 每 300 毫秒廣播一次

def handle_client(client_socket, address):
    print(f"Connection from {address} has been established!")
    role = None
    for i in clients:
        if clients[i] == 0:
            clients[i] = address[1]
            role = i
            break
    print(clients)
    if not role:
        client_socket.close()
        return

    client_sockets[role] = client_socket
    client_socket.send(role.encode('utf-8'))

    l = 0
    global gameEnd
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "__EXIT__":
                print(f"{address} 離線，重置角色")
                clients[role] = 0
                del client_sockets[role]
                l = 0
                positions[role] = 50
                gameEnd = 'False:None'
                break

            l, clear, end = compair.compair(message, l)
            print(f"Received from {address}: {message}, {l, clear, end}")

            if end:
                gameEnd = f'True:{role}'
            if clear:
                positions[role] += 150

            reply_data = f"REPLY|{str(l)} {str(clear)}"
            client_socket.send((reply_data + '\n').encode('utf-8'))

        except Exception as e:
            print(f"連線錯誤：{e}")
            break
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("Server is listening on port 5555...")

    broadcast_thread = threading.Thread(target=periodic_broadcast, daemon=True)
    broadcast_thread.start()

    while True:
        client_socket, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    start_server()

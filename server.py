# server.py
import socket
import threading
import select
import time
import compare

clients = {'Player 1': 0, 'Player 2': 0, 'Player 3': 0, 'Player 4': 0}
client_sockets = {}
positions = {'Player 1': 50, 'Player 2': 50, 'Player 3': 50, 'Player 4': 50}
gameEnd = 'False:None'
game_started = False
countdown_started = False
start_time = None
lock = threading.Lock()

def broadcast_combined():
    active_roles = ','.join(client_sockets.keys())
    pos_data = f"{positions['Player 1']},{positions['Player 2']},{positions['Player 3']},{positions['Player 4']}"
    data = f"BROADCAST|{pos_data}|{gameEnd}|{active_roles}"
    for sock in client_sockets.values():
        try:
            sock.send((data + '\n').encode('utf-8'))
        except:
            pass

def periodic_broadcast():
    global countdown_started, game_started, start_time
    while True:
        with lock:
            if countdown_started and not game_started:
                elapsed = int(time.time() - start_time)
                remaining = 30 - elapsed
                for sock in client_sockets.values():
                    try:
                        sock.send(f"COUNTDOWN|{remaining}\n".encode('utf-8'))
                    except:
                        pass
                if elapsed >= 30:
                    if len(client_sockets) >= 2:
                        game_started = True
                        for sock in client_sockets.values():
                            sock.send("START_GAME\n".encode('utf-8'))
                    else:
                        for sock in client_sockets.values():
                            sock.send("CANCEL_GAME|Not enough players\n".encode('utf-8'))
                    countdown_started = False
        broadcast_combined()
        time.sleep(1)

def handle_client(client_socket, address):
    global gameEnd, countdown_started, start_time, game_started
    print(f"Connection from {address} has been established!")
    role = None
    with lock:
        if len(client_sockets) >= 4:
            client_socket.send("WAIT_NEXT_ROUND\n".encode('utf-8'))
            client_socket.close()
            return
        for i in clients:
            if clients[i] == 0:
                clients[i] = address[1]
                role = i
                break

    if not role:
        client_socket.close()
        return

    client_sockets[role] = client_socket
    client_socket.send(role.encode('utf-8'))

    with lock:
        if not countdown_started:
            countdown_started = True
            start_time = time.time()

    l = 0
    while True:
        try:
            ready_to_read, _, _ = select.select([client_socket], [], [], 0.5)
            if client_socket in ready_to_read:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                if message == "__EXIT__":
                    print(f"{address} 離線，重置角色")
                    with lock:
                        clients[role] = 0
                        client_sockets.pop(role, None)
                        positions[role] = 50
                        gameEnd = 'False:None'
                        if len(client_sockets) < 2:
                            game_started = False
                    break

                if not game_started:
                    continue

                l, clear, end = compare.compare(message, l)
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

    threading.Thread(target=periodic_broadcast, daemon=True).start()

    while True:
        client_socket, address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, address), daemon=True).start()

if __name__ == "__main__":
    start_server()

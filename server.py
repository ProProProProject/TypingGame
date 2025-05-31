#server.py
import socket
import threading
import compair

clients={'img1':0,'img2':0}
client_sockets = {}
positions = {'img1': 50, 'img2': 50}

def broadcast_positions():
    data = f"{positions['img1']},{positions['img2']}"
    for sock in client_sockets.values():
        try:
            sock.send(data.encode('utf-8'))
        except:
            pass  # 忽略失敗


def handle_client(client_socket, address):
    print(f"Connection from {address} has been established!")
    role = None
    for i in clients:
        if clients[i] == 0:
            clients[i] = address[1]
            role = i
            break
    print (clients)        
    if not role:
        client_socket.close()
        return

    client_sockets[role] = client_socket
    client_socket.send(role.encode('utf-8'))  # 發角色給 client

    l=0
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message=="__EXIT__":
                print(f"{address}離線，重置角色")
                clients[role]=0
                del client_sockets[role]
                l=0
                positions[role] = 50
                break 

            l,clear,end = compair.compair(message,l)
            print(f"Received from {address}: {message},{l,clear}")

            if clear == True:
                positions[role] += 50  # 移動圖片

            broadcast_positions()  # 廣播所有圖片座標給所有 client

            # Echo the message back to the client
            client_socket.send((str(clear)).encode('utf-8'))
        except Exception as e:
            print(f"連線錯誤：{e}")
            break
    client_socket.close()


# Main server function
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))  # Bind to all interfaces on port 5555
    server.listen(5)  # Listen for incoming connections
    print("Server is listening on port 5555...")  

    while True:
        client_socket, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()
        

if __name__ == "__main__":
    start_server()
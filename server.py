#server.py
import socket
import threading
import time
import compair

clients={'img1':0,'img2':0, 'img3':0, 'img4':0}
client_sockets = {}
positions = {'img1': 50, 'img2': 50, 'img3' : 50, 'img4' : 50}
gameEnd = 'False:None'
def broadcast_positions():
    data = f"{positions['img1']},{positions['img2']}, {positions['img3']}, {positions['img4']}"
    for sock in client_sockets.values():
        try:
            sock.send(data.encode('utf-8'))
        except:
            pass  # 忽略失敗

def boardcast_end():
    data = gameEnd
    for sock in client_sockets.values():
        try:
            sock.send(data.encode('utf-8'))
        except:
            pass  # 忽略失敗

def periodic_broadcast():
    while True:
        broadcast_positions()
        time.sleep(0.15)  # 每 300 毫秒廣播一次
        boardcast_end()
        time.sleep(0.15)  # 每 300 毫秒廣播一次

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
    global gameEnd
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message=="__EXIT__":
                print(f"{address}離線，重置角色")
                clients[role]=0
                del client_sockets[role]
                l=0
                positions[role] = 50
                broadcast_positions()
                gameEnd = 'False:None'
                boardcast_end()
                break 

            l,clear,end= compair.compair(message,l)
            print(f"Received from {address}: {message},{l,clear,end}")

            if end == True:
                gameEnd='True:'+role
            if clear == True:
                positions[role] += 150  # 移動圖片
           
            # Echo the message back to the client
            client_socket.send((str(l)+" "+str(clear)).encode('utf-8'))
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

    broadcast_thread = threading.Thread(target=periodic_broadcast, daemon=True)
    broadcast_thread.start()

    while True:
        client_socket, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()
        

if __name__ == "__main__":
    start_server()
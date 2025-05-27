import socket
import threading
import select

def handle_client(client_socket, address):
    print(f"Connection from {address} has been established!")
    while True:
        try:
            message = client_socket.recv(1).decode('utf-8')
            if not message:
                break
            print(f"Received from {address}: {message}")
            # Echo the message back to the client
            client_socket.send(f"Server received: {message}".encode('utf-8'))
        except:
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
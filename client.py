# client.py
import socket
import threading
from window import GUI

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

role = client.recv(1024).decode('utf-8')
print('role = ' + role)

gui = None

def receive_server():
    global gui
    buffer = ''
    while True:
        try:
            buffer += client.recv(1024).decode('utf-8')
            while '\n' in buffer:
                data, buffer = buffer.split('\n', 1)
                if not data:
                    continue

                if data.startswith('BROADCAST|'):
                    _, payload = data.split('BROADCAST|', 1)
                    pos_data, end_data = payload.split('|')
                    x1, x2, x3, x4 = map(int, pos_data.split(','))
                    if gui:
                        gui.update_position(x1, x2, x3, x4)

                    if end_data != 'False:None':
                        end, winner = end_data.split(':')
                        if end == 'True':
                            gui.ending_view(winner)
                            return

                elif data.startswith('REPLY|'):
                    _, payload = data.split('REPLY|', 1)
                    line, clear = payload.split()
                    if gui:
                        gui.change_line(int(line))
                        if clear == 'True':
                            gui.clear_text()

        except Exception as e:
            print("接收錯誤:", e)
            break

def send_key_to_server(key_str):
    try:
        client.send(key_str.encode('utf-8'))
    except Exception as e:
        print(f"傳送失敗：{e}")

def start_gui():
    global gui
    gui = GUI(send_key_to_server, role)
    gui.change_line(0)
    threading.Thread(target=receive_server, daemon=True).start()
    gui.run()

if __name__ == "__main__":
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()
    gui_thread.join()

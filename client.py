# client.py
import socket
import threading
import select
from window import GUI

def receive_server():
    global gui
    buffer = ''
    while True:
        try:
            ready_to_read, _, _ = select.select([client], [], [], 0.5)
            if client in ready_to_read:
                data_chunk = client.recv(1024).decode('utf-8')
                if not data_chunk:
                    break
                buffer += data_chunk

            while '\n' in buffer:
                data, buffer = buffer.split('\n', 1)
                if not data:
                    continue

                if data.startswith('BROADCAST|'):
                    _, payload = data.split('BROADCAST|', 1)
                    pos_data, end_data, actives_roles = payload.split('|')
                    x1, x2, x3, x4 = map(int, pos_data.split(','))
                    roles = actives_roles.split(',')

                    if gui:
                        gui.update_position(x1, x2, x3, x4)
                        gui.update_active_roles(roles)

                    if end_data != 'False:None':
                        end, winner = end_data.split(':')
                        if end == 'True':
                            gui.ending_view(winner)
                            return

                elif data.startswith('REPLY|'):
                    _, payload = data.split('REPLY|', 1)
                    parts = payload.strip().split()
                    if len(parts) == 2:
                        line_str, clean_str = parts
                        line = int(line_str)
                        clear = clean_str == 'True'
                        if gui:
                            gui.change_line(line)
                            if clear:
                                gui.clear_text()

                elif data.startswith('COUNTDOWN|'):
                    seconds = int(data.split('|')[1])
                    if gui:
                        gui.show_countdown(seconds)

                elif data == 'START_GAME':
                    if gui:
                        gui.enable_input()
                        gui.change_line(0)

                elif data.startswith('CANCEL_GAME|'):
                    if gui:
                        gui.show_cancel_message(data.split('|')[1])

                elif data == 'WAIT_NEXT_ROUND':
                    print("伺服器已滿，請等待下一局")
                    return

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
    gui.disable_input()
    threading.Thread(target=receive_server, daemon=True).start()
    gui.run()

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))  # 改成你的 server IP

    role = client.recv(1024).decode('utf-8')
    print('role = ' + role)
    
    gui = None
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()
    gui_thread.join()

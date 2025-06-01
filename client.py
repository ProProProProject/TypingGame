#client.py
import socket
import threading
from window import GUI

# 建立 socket client 並連接
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))  # 請改為server所在機器的ip

role=client.recv(1024).decode('utf-8')
print('role = '+role)

gui = None  # 先建立 gui 的容器

def receive_server():
    global gui
    line=0
    while True:
        try:
            gui.change_line(int(line))
            data = client.recv(1024).decode('utf-8')
            if not data:
                break
            if ',' not in data :
                if " " in data:
                    line,clear=data.split()
                    if clear == 'True' and gui:
                        gui.clear_text()
                else:  
                    end,winner=data.split(':') 
                    if end=='True':
                        gui.ending_view(winner)
                        break
            else:
                x1, x2, x3, x4 = map(int, data.split(','))
                if gui:
                    gui.update_position(x1, x2, x3, x4)
        except Exception as e:
            print(data)
            print("接收錯誤:", e)
            break


def send_key_to_server(key_str):
    try:
        client.send(key_str.encode('utf-8'))
    except Exception as e:
        print(f"傳送失敗：{e}")
    

def start_gui():
    global gui   
    gui = GUI(send_key_to_server,role)
    threading.Thread(target=receive_server, daemon=True).start()    
    gui.run()


# 主程式
if __name__ == "__main__":
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()
    gui_thread.join()

    
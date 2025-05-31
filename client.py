#client.py
import socket
import threading
from window import GUI

# 建立 socket client 並連接
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.106', 5555))  # 請改為server所在機器的ip

role=client.recv(1024).decode('utf-8')
print('role= '+role)

# 啟動鍵盤監聽器（用 thread 避免阻塞 GUI）
def start_gui():
    gui = None  # 先建立 gui 的容器


    def send_key_to_server(key_str):
        try:
            client.send(key_str.encode('utf-8'))
        except Exception as e:
            print(f"⚠️ 傳送失敗：{e}")

        
        def receive_loop():
            while True:
                try:
                    data=client.recv(1024).decode('utf-8')
                    if not data:
                        break
                    if ',' not in data and data=='True':
                        gui.clear_text()
                    x1,x2=map(int,data.split(','))
                    gui.update_position(x1,x2)
                except:
                    break

        threading.Thread(target=receive_loop, daemon=True).start()        
   
    gui = GUI(send_key_to_server,role)
    gui.run()


# 主程式
if __name__ == "__main__":
    # 啟動鍵盤監聽器（在背景 thread）
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()
    gui_thread.join()

    
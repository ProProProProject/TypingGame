import socket
import sys
from pynput.keyboard import Key, Listener as KeyboardListener


# 建立 socket client 並連接
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.141.115', 5555))  # 請確保伺服器已在此埠運行

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
            return False
        elif key == Key.space:
            key_str = str(" ")
        elif key == Key.enter:
            key_str = str("\n")
        else:
            key_str = ''

    print(f"Pressed: {key_str}")
    send_key_to_server(key_str)

# 啟動鍵盤監聽器
listener = KeyboardListener(on_press=on_press, suppress=True)
# listener = KeyboardListener(on_press=on_press)
listener.start()

# 保持主執行緒存活（或你可以放你其他的主邏輯）
listener.join()
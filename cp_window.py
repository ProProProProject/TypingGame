import tkinter as tk
from PIL import Image, ImageTk

class GUI:
    def __init__(self):
        # 建立主視窗
        self.root = tk.Tk()
        self.root.title("Tkinter 輸入框範例")
        self.root.geometry("1000x600+350+200")

        # 載入圖片
        image = Image.open("picture/bluebird_fired.png")
        width,height=image.size
        image = image.resize((int(width*0.5), int(height*0.5)))  # 調整尺寸
        self.photo = ImageTk.PhotoImage(image)

        # 顯示圖片
        label = tk.Label(self.root, image=self.photo)
        label.place(x=50, y=100)  # 設定絕對位置，x=水平, y=垂直

        # 創建輸入框
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=50,side="bottom")

        # 綁定 Enter 鍵（Return）觸發清除
        self.entry.bind("<Return>", self.clear_text)


    def clear_text(self,event=None):
        self.entry.delete(0,tk.END)

    def run(self):
        self.root.mainloop()


    
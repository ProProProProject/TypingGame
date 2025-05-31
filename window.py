#window.py
import tkinter as tk
from PIL import Image, ImageTk

class GUI:
    def __init__(self,send_callback,role):
        self.send_callback = send_callback
        self.role=role

        # 建立主視窗
        self.root = tk.Tk()
        self.root.title("Typing Game")
        self.root.geometry("1000x600+350+200")

        label_user=tk.Label(self.root,text=role,font=("Arial", 14), anchor='ne')
        label_user.config(fg="red")
        label_user.pack()


        file=open("typing_script.txt",'r')
        content=file.read()
        label=tk.Label(self.root,text=content,font=("Arial", 14), justify="left")
        label.pack()

        # 載入圖片
        image1 = Image.open("picture/bluebird_fired.png").convert("RGBA")
        image1 = image1.resize((100, 100))
        # width1,height1=image1.size
        # image1 = image1.resize((int(width1*0.3), int(height1*0.3)))  # 調整尺寸
        self.photo1 = ImageTk.PhotoImage(image1)

        image2 = Image.open("picture/bluebird.png").convert("RGBA")
        image2 = image2.resize((100, 100))
        self.photo2 = ImageTk.PhotoImage(image2)

        # 顯示圖片
        self.canvas=tk.Canvas(self.root,width=1000,height=300)
        self.canvas.pack()
        self.x1=self.x2=50
        self.img1=self.canvas.create_image(self.x1,50,image=self.photo1)
        self.img2=self.canvas.create_image(self.x2,100,image=self.photo2)
    

        # 建立一個文字變數並與 Entry 綁定
        self.text_var = tk.StringVar()
        self.text_var.trace_add("write", self.on_change)  # 當內容變動時觸發 on_change

        # 創建輸入框
        self.entry = tk.Entry(self.root, width=50, textvariable=self.text_var)
        self.entry.pack(pady=50,side="bottom")

        # 綁定 Enter 鍵（Return）觸發清除
        #self.entry.bind("<Return>", self.clear_text)

        self.root.protocol("WM_DELETE_WINDOW",self.on_close)


    def on_change(self,*args):
        current_text = self.text_var.get()
        if current_text!="":
            self.send_callback(current_text)  # 傳送給 server
        
    def clear_text(self,event=None):
        self.entry.delete(0,tk.END)

    # def move(self):
    #     if self.role=='img1':
    #         self.x1+=50
    #         self.canvas.coords(self.img1,self.x1,50)
    #     elif self.role=='img2':
    #         self.x2+=50
    #         self.canvas.coords(self.img2,self.x2,100)
    
    def update_position(self,x1,x2):
        self.x1=x1
        self.x2=x2
        self.canvas.coords(self.img1,self.x1,50)
        self.canvas.coords(self.img2,self.x2,100)
    def on_close(self):
        try:
            self.send_callback("__EXIT__")  # 傳送空字串給 server
        except Exception as e:
            print("⚠️ 傳送失敗：", e)
        self.root.destroy()  # 關閉視窗

    def run(self):
        self.root.mainloop()


    
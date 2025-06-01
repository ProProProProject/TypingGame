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
        

        #標示user為第幾張圖
        label_user=tk.Label(self.root,text=role,font=("Arial", 24), anchor='nw')
        label_user.config(fg="red")
        label_user.pack(side="top",fill="x",padx=30,pady=10)

        #題目
        self.canvas=tk.Canvas(self.root,width=1000,height=400)
        self.canvas.pack(fill="both", expand=True)
        self.label=tk.Label(self.root,text="",font=("Arial", 30),anchor='center')
        self.label.config(fg="orange")
        # 將 Label 放到 Canvas 上方 (x=center, y=100)
        self.canvas.create_window(500, 50, window=self.label,anchor='center')


        # 載入背景圖
        bg_image = Image.open("picture/bg_grass.jpg")
        bg_image=bg_image.resize((1250,500))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # 載入圖片
        # image1 = Image.open("picture/bluebird_fired.png").convert("RGBA")
        # image1 = image1.resize((100, 100))
        # self.photo1 = ImageTk.PhotoImage(image1)

        # image2 = Image.open("picture/bluebird.png").convert("RGBA")
        # image2 = image2.resize((100, 100))
        # self.photo2 = ImageTk.PhotoImage(image2)

        # image3 = Image.open("picture/bluebird_fired.png").convert("RGBA")
        # image3 = image3.resize((100, 100))
        # self.photo3 = ImageTk.PhotoImage(image3)

        # image4 = Image.open("picture/bluebird.png").convert("RGBA")
        # image4 = image4.resize((100, 100))
        # self.photo4 = ImageTk.PhotoImage(image4)

        self.photos = {
            'Player 1': ImageTk.PhotoImage(Image.open("picture/bluebird_fired.png").resize((100, 100)).convert("RGBA")),
            'Player 2': ImageTk.PhotoImage(Image.open("picture/bluebird.png").resize((100, 100)).convert("RGBA")),
            'Player 3': ImageTk.PhotoImage(Image.open("picture/bluebird_fired.png").resize((100, 100)).convert("RGBA")),
            'Player 4': ImageTk.PhotoImage(Image.open("picture/bluebird.png").resize((100, 100)).convert("RGBA")),
        }

        # 顯示圖片
        self.bg_img=self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        # self.x1=self.x2=self.x3=self.x4=50
        # self.img1=self.canvas.create_image(self.x1,120,image=self.photo1)
        # self.img2=self.canvas.create_image(self.x2,200,image=self.photo2)
        # self.img3=self.canvas.create_image(self.x3,280,image=self.photo3)
        # self.img4=self.canvas.create_image(self.x4,360,image=self.photo4)

        self.positions = {
            'Player 1': (50, 120),
            'Player 2': (50, 200),
            'Player 3': (50, 280),
            'Player 4': (50, 360)
        }

        #若有需要每個玩家放置不同照片則需改成下列程式碼
        
        # if self.role == 'player1':
        #     self.img1 = self.canvas.create_image(self.x1, 120, image=self.photo1)
        # elif self.role == 'player2':
        #     self.img2 = self.canvas.create_image(self.x2, 200, image=self.photo2)
        # elif self.role == 'player3':
        #     self.img3 = self.canvas.create_image(self.x3, 280, image=self.photo3)
        # elif self.role == 'player4':
        #     self.img4 = self.canvas.create_image(self.x4, 360, image=self.photo4)

        self.obj_widgets = {}
        for role, (x, y) in self.positions.items():
            self.obj_widgets[role] = self.canvas.create_image(x, y, image=self.photos[role])

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

    def change_line(self,l):
        with open("typing_script.txt","r", encoding='utf-8') as file:
            lines = file.readlines()
            #print(f"目前進度第 {l} 行 / 總共 {len(lines)} 行")
            if l<len(lines):
                self.label.config(text=lines[l].replace('\n',''))
            else:
                self.label.config(text='finish!!')

    def update_position(self,x1,x2,x3,x4):
        # self.x1=x1
        # self.x2=x2
        # self.x3=x3
        # self.x4=x4
        # self.canvas.coords(self.img1,self.x1,120)
        # self.canvas.coords(self.img2,self.x2,200)
        # self.canvas.coords(self.img3,self.x3,280)
        # self.canvas.coords(self.img4,self.x4,360)

        updates = [x1, x2, x3, x4]
        for i, role in enumerate(['Player 1', 'Player 2', 'Player 3', 'Player 4']):
            x, y = updates[i], self.positions[role][1]
            self.canvas.coords(self.obj_widgets[role], x, y)
    
    def update_active_roles(self, active_roles):
        all_roles = ['Player 1', 'Player 2', 'Player 3', 'Player 4']
        for role in all_roles:
            if role in self.obj_widgets:
                state = 'normal' if role in active_roles else 'hidden'
                self.canvas.itemconfigure(self.obj_widgets[role], state=state)

    def on_close(self):
        try:
            self.send_callback("__EXIT__")  
        except Exception as e:
            print("⚠️ 傳送失敗：", e)
        self.root.destroy()  # 關閉視窗

    def run(self):
        self.root.mainloop()


    def ending_view(self,winner):
        self.entry.config(state='disabled')
        # 建立結束畫面視窗
        end_window = tk.Toplevel(self.root)
        end_window.title("🏁遊戲結束🏁")
        end_window.geometry("400x300+200+100")
        end_window.configure(bg="#FDF6EC")

        label1 = tk.Label(end_window, text="遊戲結束！", font=("Helvetica", 22, "bold"), bg="#FDF6EC", fg="#4B3869")
        label1.pack(pady=30)
        label2 = tk.Label(end_window, text="Winner is " + winner, font=("Helvetica", 26, "bold"), bg="#FDF6EC", fg="#F59A50")
        label2.pack(pady=30)

        quit_btn = tk.Button(end_window, text="離開", command=self.on_close, fg="white", bg="#30344A", font=("Helvetica", 14, "bold"), padx=20, pady=10, bd=4)
        quit_btn.pack(pady=20)

        # 可選：關閉主視窗的互動
        #self.root.withdraw()  # 隱藏主畫面（如果不想用就拿掉）
        

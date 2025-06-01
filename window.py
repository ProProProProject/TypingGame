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

        self.photos = {
            'Player 1': ImageTk.PhotoImage(Image.open("picture/bluebird_fired.png").resize((100, 100)).convert("RGBA")),
            'Player 2': ImageTk.PhotoImage(Image.open("picture/bluebird.png").resize((100, 100)).convert("RGBA")),
            'Player 3': ImageTk.PhotoImage(Image.open("picture/bluebird_fired.png").resize((100, 100)).convert("RGBA")),
            'Player 4': ImageTk.PhotoImage(Image.open("picture/bluebird.png").resize((100, 100)).convert("RGBA")),
        }

        # 顯示背景圖片
        self.bg_img=self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
    
        #初始化role位置
        self.positions = {
            'Player 1': (50, 120),
            'Player 2': (50, 200),
            'Player 3': (50, 280),
            'Player 4': (50, 360)
        }
        self.obj_widgets = {}
        for role, (x, y) in self.positions.items():
            self.obj_widgets[role] = self.canvas.create_image(x, y, image=self.photos[role])

        #更新所有role位置
        def update_position(self,x1,x2,x3,x4):
            updates = [x1, x2, x3, x4]
            for i, role in enumerate(['Player 1', 'Player 2', 'Player 3', 'Player 4']):
                x, y = updates[i], self.positions[role][1]
                self.canvas.coords(self.obj_widgets[role], x, y)

        # 建立一個文字變數並與輸入框綁定，當輸入框被寫入，文字變數會偵測到，並呼叫on_change執行
        self.text_var = tk.StringVar()
        self.text_var.trace_add("write", self.on_change)  # 當內容變動時觸發 on_change
        # 創建輸入框
        self.entry = tk.Entry(self.root, width=50, textvariable=self.text_var)
        self.entry.pack(pady=50,side="bottom")

        #關閉視窗按扭被點擊時呼叫on_close()
        self.root.protocol("WM_DELETE_WINDOW",self.on_close)

    #回傳文字變數的內容給建立GUI填入的參數(function)
    def on_change(self,*args):
        current_text = self.text_var.get()
        if current_text!="":
            self.send_callback(current_text)  # 回傳給GUI輸入的參數(function)

    #清空輸入框   
    def clear_text(self,event=None):
        self.entry.delete(0,tk.END)

    #顯示題目
    def change_line(self,l):
        with open("typing_script.txt","r", encoding='utf-8') as file:
            lines = file.readlines()
            #print(f"目前進度第 {l} 行 / 總共 {len(lines)} 行")
            if l<len(lines):
                self.label.config(text=lines[l].replace('\n',''))
            else:
                self.label.config(text='finish!!')

    #依輸入列表(active_roles)顯示需要/該出現的角色
    def update_active_roles(self, active_roles):
        all_roles = ['Player 1', 'Player 2', 'Player 3', 'Player 4']
        for role in all_roles:
            if role in self.obj_widgets:
                state = 'normal' if role in active_roles else 'hidden'
                self.canvas.itemconfigure(self.obj_widgets[role], state=state)

    #傳送結束訊息並關閉視窗
    def on_close(self):
        try:
            self.send_callback("__EXIT__")  
        except Exception as e:
            print("⚠️ 傳送失敗：", e)
        self.root.destroy()  # 關閉視窗

    #維持視窗運行
    def run(self):
        self.root.mainloop()

    #比賽結束頁面
    def ending_view(self,winner):
        self.entry.config(state='disabled')#輸入框停用
        # 建立結束畫面子視窗
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


        

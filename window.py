# window.py
import tkinter as tk
from PIL import Image, ImageTk

class GUI:
    def __init__(self, send_callback, role):
        self.send_callback = send_callback
        self.role = role

        self.root = tk.Tk()
        self.root.title("Typing Game")
        self.root.geometry("1000x600+350+200")

        label_user = tk.Label(self.root, text=role, font=("Arial", 24), anchor='nw')
        label_user.config(fg="red")
        label_user.pack(side="top", fill="x", padx=30, pady=10)

        self.canvas = tk.Canvas(self.root, width=1000, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.label = tk.Label(self.root, text="等待其他玩家...", font=("Arial", 30), anchor='center', fg="orange")
        self.canvas.create_window(500, 50, window=self.label, anchor='center')

        bg_image = Image.open("picture/bg_grass.jpg").resize((1250, 500))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.photos = {
            'Player 1': ImageTk.PhotoImage(Image.open("picture/bluebird_fired.png").resize((100, 100)).convert("RGBA")),
            'Player 2': ImageTk.PhotoImage(Image.open("picture/bluebird.png").resize((100, 100)).convert("RGBA")),
            'Player 3': ImageTk.PhotoImage(Image.open("picture/bluebird_fired.png").resize((100, 100)).convert("RGBA")),
            'Player 4': ImageTk.PhotoImage(Image.open("picture/bluebird.png").resize((100, 100)).convert("RGBA")),
        }

        self.bg_img = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.positions = {
            'Player 1': (50, 120),
            'Player 2': (50, 200),
            'Player 3': (50, 280),
            'Player 4': (50, 360)
        }
        self.obj_widgets = {}
        for role, (x, y) in self.positions.items():
            self.obj_widgets[role] = self.canvas.create_image(x, y, image=self.photos[role])

        self.text_var = tk.StringVar()
        self.text_var.trace_add("write", self.on_change)
        self.entry = tk.Entry(self.root, width=50, textvariable=self.text_var)
        self.entry.pack(pady=50, side="bottom")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_change(self, *args):
        current_text = self.text_var.get()
        if current_text != "":
            self.send_callback(current_text)

    def clear_text(self, event=None):
        self.entry.delete(0, tk.END)

    def change_line(self, l):
        try:
            with open("typing_script.txt", "r", encoding='utf-8') as file:
                lines = file.readlines()
                if l < len(lines):
                    self.label.config(text=lines[l].strip())
                else:
                    self.label.config(text="Finish!!")
        except Exception as e:
            self.label.config(text="無法載入題目")

    def update_position(self, x1, x2, x3, x4):
        updates = [x1, x2, x3, x4]
        for i, role in enumerate(['Player 1', 'Player 2', 'Player 3', 'Player 4']):
            x, y = updates[i], self.positions[role][1]
            self.canvas.coords(self.obj_widgets[role], x, y)

    def update_active_roles(self, active_roles):
        all_roles = ['Player 1', 'Player 2', 'Player 3', 'Player 4']
        for role in all_roles:
            state = 'normal' if role in active_roles else 'hidden'
            self.canvas.itemconfigure(self.obj_widgets[role], state=state)

    def on_close(self):
        try:
            self.send_callback("__EXIT__")
        except Exception as e:
            print("⚠️ 傳送失敗：", e)
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def ending_view(self, winner):
        self.entry.config(state='disabled')
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

    def show_countdown(self, seconds):
        self.label.config(text=f"等待其他玩家加入中… 還有 {seconds} 秒")

    def show_cancel_message(self, msg):
        self.label.config(text=f"⚠️ {msg}")
        self.entry.config(state='disabled')

    def enable_input(self):
        self.entry.config(state='normal')
        self.clear_text()

    def disable_input(self):
        self.entry.config(state='disabled')

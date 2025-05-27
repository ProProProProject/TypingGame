import tkinter as tk
from tkinter import messagebox
import socket
import threading
import random

WIDTH, HEIGHT = 800, 400
CAR_COLORS = ['red', 'blue', 'green', 'orange']
NUM_TREES = 5

class TypingGameClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Multiplayer Typing Race")
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg='lightblue')
        self.canvas.pack()

        self.track = self.canvas.create_rectangle(0, HEIGHT//2, WIDTH, HEIGHT, fill='gray')
        self.tree_images = [self.canvas.create_oval(-40, random.randint(0, HEIGHT//2 - 60), -10, random.randint(30, HEIGHT//2 - 10), fill="green") for _ in range(NUM_TREES)]

        self.player_car = self.canvas.create_rectangle(0, 210, 40, 250, fill=CAR_COLORS[0])
        self.other_cars = [self.canvas.create_rectangle(0, 260 + i*30, 40, 300 + i*30, fill=CAR_COLORS[i+1]) for i in range(3)]

        self.text_label = tk.Label(master, text="", wraplength=WIDTH, font=("Helvetica", 14))
        self.text_label.pack()
        self.entry = tk.Entry(master, font=("Helvetica", 16))
        self.entry.pack()
        self.entry.focus_set()
        self.entry.bind("<KeyRelease>", self.on_typing)

        self.client = None
        self.progress = 0
        self.positions = [0, 0, 0, 0]

        self.connect_to_server()

        self.update_trees()

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(("localhost", 50007))  # 可替換成你的伺服器 IP
        except Exception as e:
            messagebox.showerror("Error", f"無法連線伺服器: {e}")
            return

        threading.Thread(target=self.listen_server, daemon=True).start()

    def listen_server(self):
        while True:
            try:
                msg = self.client.recv(1024).decode()
                if msg.startswith("TEXT|"):
                    self.game_text = msg[5:]
                    self.text_label.config(text=self.game_text)
                elif msg.startswith("UPDATE|"):
                    updates = msg[7:].split("|")
                    for up in updates:
                        i, p = map(int, up.split(":"))
                        self.positions[i] = p
                    self.update_cars()
            except:
                break

    def on_typing(self, event):
        typed = self.entry.get()
        if self.game_text.startswith(typed):
            self.entry.config(fg="black")
        else:
            self.entry.config(fg="red")
        self.client.sendall(f"PROGRESS|{typed}".encode())

    def update_cars(self):
        for i in range(4):
            x = (self.positions[i] / len(self.game_text)) * (WIDTH - 100)
            car = self.player_car if i == 0 else self.other_cars[i - 1]
            self.canvas.coords(car, x, car[1], x + 40, car[3])

    def update_trees(self):
        for tree in self.tree_images:
            self.canvas.move(tree, 5, 0)
            x1, y1, x2, y2 = self.canvas.coords(tree)
            if x1 > WIDTH:
                self.canvas.coords(tree, -40, random.randint(0, HEIGHT//2 - 60), -10, random.randint(30, HEIGHT//2 - 10))
        self.master.after(100, self.update_trees)

if __name__ == "__main__":
    root = tk.Tk()
    game = TypingGameClient(root)
    root.mainloop()

import tkinter as tk
import threading, random, time, datetime
import inspect
import ctypes
from tkinter import ttk
from pygame import mixer
from PIL import Image, ImageTk

FLAG = True
CARFLAG = True
ROAD = ''

class Player:
    def __init__(self, username):
        self.username = '[玩家]' + username

    def car_create(self, c, carposy_list):
        self.car = Car('./sucai/car1.jpg', carposy_list, 'img1', self.username)
        image = Image.open(self.car.filepath)
        self.car_img = ImageTk.PhotoImage(image)
        c.create_image(self.car.posx, self.car.posy, image=self.car_img, tag=self.car.cartag)
        c.create_text(self.car.posx-30, self.car.posy, text=self.car.username, font=("Purisa", 16), fill='white', tag=self.car.username)

class Computer:
    def __init__(self, username='[電腦]'):
        self.username = username

    def car_create(self, c, filepath, posy, cartag, username):
        self.car = Car(filepath, posy, cartag, username)
        image = Image.open(self.car.filepath)
        self.car_img = ImageTk.PhotoImage(image)
        c.create_image(self.car.posx, self.car.posy, image=self.car_img, tag=self.car.cartag)
        c.create_text(self.car.posx-30, self.car.posy, text=self.car.username, font=("Purisa", 16), fill='white', tag=self.car.username)

class Road:
    def __init__(self, roadtype):
        self.text = []
        with open(f'./sucai/{roadtype}關鍵字.txt', mode='r', encoding='utf-8') as f:
            for line in f:
                self.text.append(line.strip().split('\t')[0])
        self.road_number = int(len(self.text)*1.2) if ROAD == 'Python' else int(len(self.text)*1.5)
        self.road_length = (self.road_number - 3) * 1000
        self.road_s = 0.0

    def begin(self, c):
        c.create_rectangle(100, 50, 150, 352, fill='#FFF6EE', tag='begin')
        c.create_text(135, 200, text='R\ne\na\nd\ny\ni\nn\ng\n \nG\nO', font=("Purisa", 20), fill='black', tag='begin')

    def destination(self, c):
        self.c_end = c.create_text(self.road_length - 120, 200, text='終\n點', font=("Purisa", 52), fill='white', tag='end')

    def road_move(self, c, tag_road):
        global FLAG, player
        self.tag_road = tag_road
        if FLAG:
            self.road_s += player.car.speed
            if self.road_s > 1000:
                self.road_s = 0.0
                if self.tag_road:
                    c.delete(self.tag_road.pop(0))
            for i in range(1, self.road_number + 1):
                c.move(i, -player.car.speed, 0)
            c.move(self.c_end, -player.car.speed, 0)

class Tree:
    speed = 0
    def __init__(self, posx, posy, filepath, treetag='tree'):
        self.posx = posx
        self.posy = posy
        self.filepath = filepath
        self.treetag = treetag

    def tree_create(self, c):
        image = Image.open(self.filepath)
        self.tree_img = ImageTk.PhotoImage(image)
        c.create_image(self.posx, self.posy, image=self.tree_img, tag=self.treetag)

    def treemove(self, c):
        global FLAG, player
        if FLAG:
            if self.posx > 10:
                self.speed = player.car.speed
                self.posx -= self.speed
                c.delete(self.treetag)
                c.create_image(self.posx, self.posy, image=self.tree_img, tag=self.treetag)
            else:
                self.posx = random.randint(550, 950)
                self.speed = player.car.speed
                self.posx -= self.speed
                c.create_image(self.posx, self.posy, image=self.tree_img, tag=self.treetag)

class Car:
    speed = 2.0
    posx = 70
    car_move_distance = []
    def __init__(self, filepath, posy, cartag, username):
        self.filepath = filepath
        self.posy = posy
        self.cartag = cartag
        self.username = username

    def car_move(self, c, car_img):
        global FLAG
        print(self.username, '準備就緒...')
        self.car_img = car_img
        def run():
            if FLAG:
                if CARFLAG:
                    self.posx += self.speed
                    self.car_move_distance = []
                    self.car_move_distance.append((self.cartag, self.posx))
                    c.delete(self.cartag)
                    c.create_text(self.posx, self.posy, text=self.car_img, tag=self.cartag)
                    c.delete(self.username)
                    c.create_text(self.posx, self.posy, text=self.username, font=("Purisa", 13), fill='white', tag=self.username)
                else:
                    c.delete(self.cartag)
                    c.create_image(self.posx, self.posy, image=self.car_img, tag=self.cartag)
                    c.delete(self.username)
                    c.create_text(self.posx, self.posy, text=self.username, font=('Purisa', 13), fill='white', tag=self.username)
                c.after(10, run)
            else: print(f'{self.username} 車子停止')
        run()

    def car_speed_change(self):
        global FLAG, player
        time.sleep(2.3)
        while FLAG:
            if player.car.speed < 14: self.speed = random.uniform(player.car.speed - 0.3, player.car.speed + 0.7)
            elif 14 < player.car.speed < 18: self.speed = random.uniform(player.car.speed - 0.8, player.car.speed + 0.5)
            else: self.speed = random.uniform(19 -1.1, 19 + 0.3)
            time.sleep(1)

class display_text:
    def __init__(self, gw):
        self.gw = gw
        self.l1_oop = []
        self.l2_oop = []
        self.cpm_list = []
        self.typespeed = 0.0
        self.anwser = ''
        self.text = self.gw.road.text
        self.text2 = self.text.copy()
        self.text.extend(self.text2)
        self.text_number = len(self.text) / 2
        self.loading_text()
    
    def loading_text(self):
        col = 1
        number = 20
        for i, text in enumerate(self.text[:number]):
            l1 = tk.Label(gw.text_frame, text=text, bg='white', font=('微軟雅黑', 15))
            l2 = tk.Label(gw.text_frame, text='', bg='white', font=('微軟雅黑', 15))
            if i < int(number / 2):
                l1.grid(row=1, column=col, )
                l2.grid(row=2, column=col, )
            elif int(number / 2) <= i < number:
                l1.grid(row=3, column=col - int(number / 2), )
                l2.grid(row=4, column=col - int(number / 2), )
            col += 1
            l1.focus_set()
            l1.bind("<Key>", self.l_bind)
            self.l1_oop.append(l1)
            self.l2_oop.append(l2)
        
    def l_bind(self, event):
        global FLAG
        if not FLAG: return
        if not self.text: return
        if event.keycode == 8:
            self.anwser = ''
            self.l2_oop[0].configure(text='')
            return
        if not 65 <= event.keycode <= 90: return
        self.anwser += event.char
        self.l2_oop[0].configure(text=self.anwser, bg='#FFFAE3')
        result = self.text[0]
        if self.anwser.strip() == result:
            self.cpm_list.append(result)
            self.l1_oop[0].configure(fg='red')
            self.text.remove(result)
            self.l1_oop.pop(0)
            self.l2_oop.pop(0)
            self.anwser = ''
            if not self.l1_oop and len(self.text) != 0:
                gw.text_frame.destroy()
                gw.display_text_frame()
                self.loading_text()
            return
        if len(self.anwser) >= len(result):
            self.anwser = ''

    def typing_speed(self):
        global FLAG
        time_ = 0
        while FLAG:
            time_ += 1
            try:
                self.cpm = round(len(''.join(self.cpm_list)) / time_ * 60)
                self.wpm = round(len(self.cpm_list) / (time_ / 60))
                gw.cpm_label.configure(text=f'cpm: {self.cpm}')
                gw.wpm_label.configure(text=f'wpm: {self.wpm}')
            except:
                self.cpm = 0
                self.wpm = 0
            self.typespeed = self.cpm / 12
            time.sleep(1)

# 遊戲窗口類
class GameWindow:
    bgcolor = '#86896e'  # 畫面背景色
    root = tk.Tk()  # 主視窗
    root.title("打字小遊戲開發")  # 視窗標題

    screenwidth = root.winfo_screenwidth()    # 螢幕寬度
    screenheight = root.winfo_screenheight()  # 螢幕高度

    def __init__(self):
        pass

    # 設定畫面大小與居中顯示
    def window_page_size(self, self_windowsize):
        rootwidth, rootheight = self_windowsize
        rootposx = int((self.screenwidth - rootwidth) / 2)
        rootposy = int((self.screenheight - rootheight) / 2) - 100
        self.root.geometry('{}x{}+{}+{}'.format(rootwidth, rootheight, rootposx, rootposy))
        time.sleep(0.1)

    # 選擇賽道
    def select_road(self):
        def func(event):
            global FLAG, CARFLAG, ROAD
            FLAG = True
            CARFLAG = True
            road = event.widget["text"]  # 取得按鈕上的文字
            print(road)
            ROAD = road[:-2]  

            # 銷毀原選擇視窗與初始化遊戲畫面
            self.select_road_frame.destroy()
            self.window_page_size((1000, 560))
            self.create_canvas()
            configuration_project(ROAD)
            self.recording_time()
            self.display_typing_speed()
            self.replay_button()
            self.return_button()

        # 重設畫面大小與位置
        self.window_page_size((500, 300))
        self.select_road_frame = tk.Frame(self.root)
        self.select_road_frame.place(x=0, y=0, width=500, height=300)
        for road in ['Python賽道', 'Java賽道', 'MySql賽道']:
            b = tk.Button(self.select_road_frame, text=road, font=('華文行楷', 26),relief=tk.RAISED, cursor='hand2', width=12, height=1)
            b.pack(pady=20)
            b.bind("<Button-1>", func)

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=1000, height=400, bg=self.bgcolor)
        self.canvas.place(x=0, y=0)

    def create_road(self, roadtype):
        self.road = Road(roadtype)
        image = Image.open('./sucai/road.jpg')
        self.road_img = ImageTk.PhotoImage(image)
        self.c_road = [
            self.canvas.create_image(i, 200, image=self.road_img, tag=f'c_road{i}')
            for i in range(500, self.road.road_number * 1000, 1000)
        ]
        self.tag_road = [f'c_road{i}' for i in range(500, (self.road.road_number - 2) * 1000, 1000)]
    #創建兩棵樹
    def create_tree(self):
        self.tree1 = Tree(posx=160, posy=350, filepath='./sucai/tree1.jpg', treetag='tree1')
        self.tree1.tree_create(self.canvas)
        self.tree2 = Tree(posx=230, posy=340, filepath='./sucai/tree2.jpg', treetag='tree2')
        self.tree2.tree_create(self.canvas)

    #創建跑程進度條
    def displayprogressbar(self, caroop_list):
        maximum = self.road.road_length
        self.progressbar_list = []

        for i in range(4):
            progressbar = ttk.Progressbar(self.canvas, length=200, maximum=maximum)
            progressbar.place(x=10, y=0 if i == 0 else i * 40 + 20)
            tk.Label(self.canvas, text=caroop_list[i].username, fg='#191970')\
                .place(x=215, y=20 if i == 0 else i * 40 + 20)
            self.progressbar_list.append(progressbar)

    #重新開始的按扭
    def replay_button(self):
        def function():
            global FLAG, CARFLAG, end_label_list, dt
            FLAG = False
            CARFLAG = False
            for t in threading.enumerate()[1:]:
                stop_thread(t)
            self.canvas.destroy()
            self.text_frame.destroy()
            if end_label_list:
                for i in end_label_list:
                    i.destroy()
            del dt

            FLAG = True
            CARFLAG = True
            self.create_canvas()
            configuration_project(ROAD)
            self.recording_time()
            self.return_button()

        image = Image.open('./sucai/replay.jpg')
        self.replaybutton_img = ImageTk.PhotoImage(image)
        tk.Label(self.root, text='重新開始').place(x=920, y=480)
        replaybutton = tk.Button(self.root, image=self.replaybutton_img, command=function)
        replaybutton.place(x=910, y=400)

    # 返回按鈕
    def return_button(self):
        def function():
            global FLAG, CARFLAG, ROAD, end_label_list, dt
            FLAG = False
            CARFLAG = False
            ROAD = ''
            
            for t in threading.enumerate()[2:]:
                stop_thread(t)
            self.canvas.destroy()
            self.text_frame.destroy()
            self.cpm_label.destroy()
            self.wpm_label.destroy()
            
            if end_label_list:
                for i in end_label_list:
                    i.destroy()
            del dt
            self.select_road()
        image = Image.open('./sucai/return.jpg')
        self.returnbutton_img = ImageTk.PhotoImage(image)
        returnbutton = tk.Button(self.root, text='返回', image=self.returnbutton_img, command=function)
        returnbutton.place(x=900, y=50)

    # 紀錄遊戲時間
    def recording_time(self):
        time_label = tk.Label(self.canvas, text='時長: 00:00:00',
                            font=("華文行楷", 15), background='#DAEFE6')
        time_label.place(x=870, y=20)

        start_time = datetime.datetime.now()

        def run():
            global FLAG
            if FLAG:
                time_label.after(1000, run)
                update_time = datetime.datetime.now() - start_time
                self.time_ = f'時長: {update_time}'.split('.')[0]
                time_label.configure(text=self.time_)  # 顯示時間（去除毫秒）

        run()

    # 顯示文本區塊
    def display_text_frame(self):
        self.text_frame = tk.Frame(self.root, bg='white')
        self.text_frame.place(x=100, y=400, width=800, height=150)

    # 顯示打字速度 (CPM/WPM)
    def display_typing_speed(self):
        self.cpm_label = tk.Label(self.root, text='cpm: 0', font=("微軟雅黑", 13), fg='#A52A2A')
        self.cpm_label.place(x=8, y=410)

        self.wpm_label = tk.Label(self.root, text='wpm: 0', font=("微軟雅黑", 13), fg='#A52A2A')
        self.wpm_label.place(x=8, y=440)

    # 播放背景音樂函數
    def playmusic(self):
        global FLAG
        mixer.init()
        # mixer.music.load('./sucai/bgmusic.mp3')
        # mixer.music.play()

        while FLAG:
            time.sleep(2)
        mixer.music.stop()

    # 顯示視窗
    def displaywindow(self):
        self.root.resizable(False, False)
        self.root.mainloop()

def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("Invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def monitoring_data(gw, caroop_list, dt):
    global FLAG, CARFLAG, end_label_list
    time.sleep(2.5)  # 延遲 2.5 秒後才開始

    gw.displayprogressbar(caroop_list)  # 顯示完成跑道的進度條
    gw.canvas.delete('begin')  # 刪除起點線
    gw.road.destination(gw.canvas)  # 創建終點線

    player_car_s = player.car.car_move_distance[0][1]
    timesleep3_posx_s_list = {}

    for i in caroop_list:
        timesleep3_posx_s_list[i.username] = i.car.car_move_distance[0][1]
        print(i.username, '已跑起來')

    while FLAG:
        CARFLAG = False

        for idx, p in enumerate(gw.progressbar_list):
            p['value'] = timesleep3_posx_s_list[caroop_list[idx].username]

        if max(timesleep3_posx_s_list.values()) > gw.road.road_length:
            FLAG = False
            ranking = sorted(timesleep3_posx_s_list.items(), key=lambda x: x[1])  # 排名

            for idx, username in enumerate(ranking[::-1]):
                l = tk.Label(gw.root, text=username[0] + f' 第{idx + 1}名',
                             font=('微軟雅黑', 28), bg='white')
                l.pack(pady=30)
                end_label_list.append(l)

            print('遊戲結束')
            return

        player.car.speed = dt.typespeed  # 玩家速度 = 打字速度
        player_car_s += player.car.speed  # 玩家小車新的位置
        timesleep3_posx_s_list[player.username] = player_car_s

        for i , caroop in enumerate(caroop_list[1:]):
            caroop.car.speed = caroop.car.speed  # 對手速度維持不變
            timesleep3_posx_s_list[caroop.username] += caroop.car.speed

        gw.road.road_move(gw.canvas, gw.c_road)  # 賽道移動
        gw.tree1.treemove(gw.canvas)  # 樹木移動
        gw.tree2.treemove(gw.canvas)  # 樹木移動

        time.sleep(0.005)  # 控制更新頻率


#配置運行流程
def configuration_project(roadtype):
    print('Game Start!')
    global player,gw,dt,end_label_list
    tplaymusic = threading.Thread(target=gw.playmusic) #開啟一個撥放背景音樂的線程
    tplaymusic.daemon = True
    tplaymusic.start()
    gw.create_road(roadtype)
    gw.create_tree() 
    gw.road.begin(gw.canvas)
    gw.display_text_frame()
    end_label_list = []
    caroop_list = []
    carposy_list = [90,147,250,390]
    player = Player('yyds')
    player.car_create(gw.canvas, carposy_list[0])
    caroop_list.append(player)
    for i in range(3):
        computer = Computer(f'[電腦]{i+ 1}')
        computer.car_create(gw.canvas,f'./sucai/car{i+2}.jpg',carposy_list[i+1], f'img{i+2}', computer.username) #生成屬於電腦玩家的小車
        caroop_list.append(computer)
    for caroop in caroop_list:
        tcm = threading.Thread(target = caroop.car.car_move,args=(gw.canvas,caroop.car_img))
        tcm.daemon = True
        tcm.start()
        tscs = threading.Thread(target = caroop.car.car_speed_change)
        tscs.daemon = True
        tscs.start()
    dt = display_text(gw)
    tdt = threading.Thread(target=dt.typing_speed)
    tdt.daemon = True
    tdt.start()
    tmd = threading.Thread(target=monitoring_data, args=(gw, caroop_list, dt))
    tmd.daemon=True
    tmd.start()
def start():
    global gw
    gw = GameWindow()
    gw.select_road()
    gw.displaywindow()
if __name__== '__main__':
    start()          
                
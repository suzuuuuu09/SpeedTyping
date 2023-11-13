import tkinter as tk
import threading as th
import winsound, random, time, math, keyboard
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
from tkinter import *
from tkinter import ttk


#word.txtの読み込み
with open("word.txt", "r") as f:
    words = f.read().splitlines()


score = 0
time_limit = 60
start_time = None
ct = None
game_ended = False


#windowのサイズと開始位置
def display_pos():
    global w_dis, h_dis, w_win, h_win
    w_dis, h_dis = root.winfo_screenwidth(), root.winfo_screenheight()
    if w_dis > 1920 or h_dis > 1080:
        w_dis, h_dis = 1920, 1080
    w_win, h_win = math.floor(w_dis / 2.5), math.floor(h_dis / 2.5)
    return  str(w_win) + "x" + str(h_win) + "+" + str(math.floor(w_dis // 3.3)) + "+" + str(math.floor(h_dis // 3.3))


#オブジェクトリセット
def reset_pos():
    titleL.place_forget()
    wordL.place_forget()
    countL.place_forget()
    wordE.place_forget()
    scoreL.place_forget()
    startB.place_forget()
    settingB.place_forget()
    timerL.place_forget()
    seCB.pack_forget()
    backB.pack_forget()


#正解効果音
def hit_se():
    if se.get():
       winsound.PlaySound("sounds/hit.wav", winsound.SND_FILENAME)


#不正解効果音
def miss_se():
    if se.get():
        winsound.PlaySound("sounds/miss.wav", winsound.SND_FILENAME)


#タイトル画面
def title():
    reset_pos()
    startB.place(x=w // 3, y=h // 1.5, anchor = "center")
    settingB.place(x=w // 1.5, y=h // 1.5, anchor = "center")
    titleL.place(x=w // 2, y=h // 3.5, anchor = "center")


#設定画面
def setting():
    reset_pos()
    seCB.pack(anchor="w")
    backB.pack(side="bottom", anchor="w")


#ゲーム開始時カウントダウン
def start_ct(sec):
    global ct, start_time
    reset_pos()
    countL.place(x=w // 2, y=h // 2, anchor = "center")
    countL.config(text =str(sec))
    if sec > 0:
        ct = root.after(1000, start_ct, sec - 1)
    else:
        if ct:
            root.after_cancel(ct)
        countL.config(text="GO!")
        startB["state"] = "normal"
        wordE["state"] = "normal"
        wordE.focus_set()
        start_time = time.time()
        next_word()
        countdown()
        reset_pos()
        timerL.place(x= w // 10, y= h // 12, anchor="center")
        scoreL.place(x= w // 1.1, y= h // 12, anchor="center")
        wordL.place(x= w // 2, y= h // 3, anchor="center")
        wordE.place(x= w // 2, y= h // 2, anchor="center")


def start_game():
    global score, game_ended
    score = 0
    wordE.bind("<Return>", check_word)
    start_ct(3)
    startB["state"] = "disabled"
    game_ended = False


def next_word():
    if len(words) > 0:
        current_word = random.choice(words)
        wordL.config(text=current_word)
        words.remove(current_word)
    else:
        end_game()


def end_game():
    global score, game_ended
    wordL.config(text="ゲーム終了\nScore: " + str(score))
    wordE.delete(0, tk.END)
    startB["state"] = "normal"
    wordE["state"] = "disabled"
    game_ended = True


def check_word(event):
    global score
    if game_ended:
        return
    user_input = wordE.get()
    if user_input == wordL.cget("text"):
        score += 1
        next_word()
        hit_se()
    else:
        next_word()
        miss_se()
    scoreL.config(text="Score: " + str(score))
    wordE.delete(0, tk.END)
    

def countdown():
    global time_limit
    if start_time is not None:
        elapsed_time = time.time() - start_time
        remaining_time = max(time_limit - elapsed_time, 0)
        timerL.config(text=f"Time: {int(remaining_time)} ")
        if elapsed_time >= time_limit:
            end_game()
            wordE.unbind("<Return>")
        else:
            root.after(1000, countdown)


#ウィンドウ情報
root = tk.Tk()
root.geometry(display_pos())
root.update_idletasks()
root.resizable(0,0)
w, h = root.winfo_width(), root.winfo_height()
root.title("SpeedTyping")


#styleの設定
style = ttk.Style()
style.configure("t.TButton", font=("Segoe UI Emoji", 20))
style.configure("setting.TCheckbutton", font=("Segoe UI Emoji", 20))


#UI
startB = ttk.Button(root, text="START", style="t.TButton", padding=[10], command=start_game)
settingB = ttk.Button(root, text="SETTING", style="t.TButton", padding=[10], command=setting)
titleL = tk.Label(root, text="SpeedTyping", font=("fonts/smb.ttf", 80))


se = BooleanVar(root)
seCB = ttk.Checkbutton(root, text="Sound Effect (unstable)", style="setting.TCheckbutton", variable=se)
backB = ttk.Button(root, text="<Back", style="t.TButton", padding=[10], command=title)


wordL = tk.Label(root, font=("Helvetica", 48))
countL = tk.Label(root, font=("Helvetica", 54))
wordE = ttk.Entry(root, font=("Helvetica", 24), state="disabled", justify="center")
scoreL = tk.Label(root, text="Score: 0", font=("Helvetica", 18))
timerL = tk.Label(root, text=f"Time: {time_limit} ", font=("Helvetica", 18))

title()

root.mainloop()

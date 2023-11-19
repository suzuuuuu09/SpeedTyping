import tkinter as tk
import random, time, math
from tkinter import *
from tkinter import ttk
from pydub import AudioSegment
from pydub.playback import play


#word.txtの読み込み
with open("word.txt", "r") as f:
    words = f.read().splitlines()


score = 0
time_limit = 1
volume_percent = 70
enter_ct = 0
cor_ct = 0
start_time = None
ct = None
game_ended = False


#windowのサイズと開始位置
def display_pos():
    global w_dis, h_dis, w_win, h_win
    w_dis, h_dis = root.winfo_screenwidth(), root.winfo_screenheight()
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
    accuL.pack_forget()
    ButtonF.pack_forget()
    contiB.pack_forget()
    titleB.pack_forget()


#正解効果音
def play_hit_se():
    global volume_percent
    if se.get():
        hit_se = AudioSegment.from_wav("sounds/hit.wav")
        play(hit_se + (20 * math.log10((volume_percent + 1) / 100)))


#不正解効果音
def play_miss_se():
    global volume_percent
    if se.get():
        miss_se = AudioSegment.from_wav("sounds/miss.wav")
        play(miss_se + (20 * math.log10((volume_percent + 1) / 100)))


#タイトル画面
def title():
    reset_pos()
    startB.place(x=w // 3, y=h // 1.5, anchor="center")
    settingB.place(x=w // 1.5, y=h // 1.5, anchor="center")
    titleL.place(x=w // 2, y=h // 3.5, anchor="center")


#設定画面
def setting():
    reset_pos()
    seCB.pack(anchor="w")
    backB.pack(side="bottom", anchor="w")


#結果画面
def result():
    global score, game_ended, cor_ct, enter_ct
    try:
        accu = cor_ct / enter_ct * 100
    except:
        accu = 0.0
    accuL.config(text=str(round(accu, 1)) + "%")
    reset_pos()
    accuL.pack()
    ButtonF.pack(fill="x", side="bottom")
    contiB.pack(padx=5, pady=5, side="right")
    titleB.pack(padx=5, pady=5, side="left")
    game_ended = True


#ゲーム開始時カウントダウン
def start_ct(sec):
    global ct, start_time
    reset_pos()
    countL.place(x=w // 2, y=h // 2, anchor="center")
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
        result()
 

def check_word(event):
    global score, enter_ct, cor_ct, cur_word
    if game_ended:
        return
    user_input = wordE.get()
    cur_word = wordL.cget("text")
    if user_input == cur_word:
        score += len(cur_word)
        cor_ct += 1
        enter_ct += 1
        play_hit_se()
    else:
        enter_ct += 1
        play_miss_se()
    next_word()
    scoreL.config(text="Score: " + str(score))
    wordE.delete(0, tk.END)
    

def countdown():
    global time_limit
    if start_time is not None:
        elapsed_time = time.time() - start_time
        remaining_time = max(time_limit - elapsed_time, 0)
        timerL.config(text=f"Time: {int(remaining_time)} ")
        if elapsed_time >= time_limit:
            result()
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
style.theme_use("clam")
style.configure("title.TButton", font=("Helveticai", 20))
style.configure("setting.TCheckbutton", font=("Helvetica", 20))


#UI
startB = ttk.Button(root, text="START", style="title.TButton", padding=[10], command=start_game)
settingB = ttk.Button(root, text="SETTING", style="title.TButton", padding=[10], command=setting)
titleL = tk.Label(root, text="SpeedTyping", font=("Helvetica", 80))


se = BooleanVar(root)
seCB = ttk.Checkbutton(root, text="Sound Effect (unstable)", style="setting.TCheckbutton", variable=se)
backB = ttk.Button(root, text="<Back", style="title.TButton", padding=[10], command=title)


wordL = tk.Label(root, font=("Helvetica", 48))
countL = tk.Label(root, font=("Helvetica", 54))
wordE = ttk.Entry(root, font=("Helvetica", 24), state="disabled", justify="center")
scoreL = tk.Label(root, text="Score: 0", font=("Helvetica", 18))
timerL = tk.Label(root, text=f"Time: {time_limit} ", font=("Helvetica", 18))


accuL = tk.Label(root, font=("Helvetica", 48))
#voluS = ttk.Scale(root, variable=val,)
ButtonF = tk.Frame(root, pady=5, padx=5, bd=0)
contiB = ttk.Button(ButtonF, text="CONTINUE", style="title.TButton", padding=[10], command=start_game)
titleB = ttk.Button(ButtonF, text="TITLE", style="title.TButton", padding=[10], command=title)


title()

root.mainloop()

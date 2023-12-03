import tkinter as tk
import random, time, math
from tkinter import *
from tkinter import ttk
from pydub import AudioSegment
from pydub.playback import play
from ttkthemes import ThemedTk


time_limit = 0
volume_percent = 70
start_time = None
ct = None
game_end = False


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
    buttonF.pack_forget()
    contiB.pack_forget()
    titleB.pack_forget()
    modeF.place_forget()
    modeL.pack_forget()
    easyB.pack_forget()
    normalB.pack_forget()
    hardB.pack_forget()
    score_rL.pack_forget()
    volS.pack_forget()


#音量調整
def volume_control(vol_var):
    global volume_percent
    volume_percent = vol_var


#正解効果音
def play_hit_se():
    global volume_percent, v
    if se.get():
        v = float(volume_percent)
        hit_se = AudioSegment.from_wav("sounds/hit.wav")
        play(hit_se + (20 * math.log10((math.ceil(v) + 1) / 100)))


#不正解効果音
def play_miss_se():
    global volume_percent, v
    if se.get():
        v = float(volume_percent)
        miss_se = AudioSegment.from_wav("sounds/miss.wav")
        play(miss_se + (20 * math.log10((math.ceil(v)) + 1) / 100))


def easy_mode():
    global min_value, max_value, time_limit, score
    max_value = 6
    min_value = 0
    time_limit = 5
    start_game()


def normal_mode():
    global min_value, max_value, time_limit, score
    max_value = 10
    min_value = 5
    time_limit = 90
    start_game()


def hard_mode():
    global min_value, max_value, time_limit, score
    max_value = 99
    min_value = 9
    time_limit = 120
    start_game()


#タイトル画面
def title():
    reset_pos()
    startB.place(x=w // 3, y=h // 1.5, anchor="center")
    settingB.place(x=w // 1.5, y=h // 1.5, anchor="center")
    titleL.place(x=w // 2, y=h // 3.5, anchor="center")


#モード選択画面
def mode_select():
    reset_pos()
    modeF.place(x=w // 2, y=h // 2, anchor="center")
    modeL.pack()
    easyB.pack(padx=5, pady=5)
    normalB.pack(padx=5, pady=5)
    hardB.pack(padx=5, pady=5)


#設定画面
def setting():
    reset_pos()
    seCB.pack(anchor="w")
    volS.pack(anchor="w")
    backB.pack(side="bottom", anchor="w")


#結果画面
def result():
    global score, game_end, cor_ct, enter_ct
    try:
        accu = cor_ct / enter_ct * 100
    except:
        accu = 0.0
    accuL.config(text="Accuracy\n" + str(round(accu, 1)) + "%")
    score_rL.config(text="score\n" + str(score))
    reset_pos()
    accuL.pack()
    score_rL.pack()
    buttonF.pack(fill="x", side="bottom")
    contiB.pack(padx=5, pady=5, side="right")
    titleB.pack(padx=5, pady=5, side="left")
    game_end = True


#ゲーム開始時カウントダウン
def start_ct(sec):
    global ct, start_time, cur_word
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


#ゲーム開始時の初期化
def start_game():
    global score, game_end, enter_ct, cor_ct, conti_ct
    score = 0
    enter_ct = 0
    cor_ct = 0
    conti_ct = 0
    wordE.delete(0, tk.END)
    if score > 0:
        score = 0
        scoreL.config(text="Score: " + str(score))
    if cor_ct > 0:
        cor_ct = 0
    if enter_ct > 0:
        enter_ct = 0
    if conti_ct > 0:
        conti_ct = 0
    wordE.bind("<Return>", check_word)
    start_ct(3)
    startB["state"] = "disabled"
    game_end = False
    

def next_word():
    global min_value, max_value
    with open("word.txt", "r", encoding="utf-8") as f:
        words = f.read().splitlines()
        if len(words) > 0:
            current_word = random.choice([word for word in words if len(word) >= min_value and len(word) <= max_value])
            wordL.config(text=current_word)
            words.remove(current_word)
        else:
            result()
 

def check_word(event):
    global score, enter_ct, cor_ct, cur_word, conti_ct
    if game_end:
        return
    user_input = wordE.get()
    cur_word = wordL.cget("text")
    if user_input == cur_word:
        score += len(cur_word)
        cor_ct += 1
        enter_ct += 1
        conti_ct += 1
        play_hit_se()
    else:
        enter_ct += 1
        conti_ct = 0
        play_miss_se()
    next_word()
    scoreL.config(text="Score: " + str(score))
    wordE.delete(0, tk.END)
    

def countdown():
    global time_limit, conti_ct
    if start_time is not None:
        elapsed_time = time.time() - start_time
        remaining_time = max(time_limit - elapsed_time, 0)
        if conti_ct % 3 == 0:
            remaining_time += conti_ct / 3
        timerL.config(text=f"Time: {int(remaining_time)} ")
        if elapsed_time >= time_limit:
            result()
        else:
            root.after(1000, countdown)


#ウィンドウ情報
root = ThemedTk()
root.geometry(display_pos())
root.update_idletasks()
root.resizable(0,0)
w, h = root.winfo_width(), root.winfo_height()
root.title("SpeedTyping")


#styleの設定
style = ttk.Style()
style.theme_use("breeze")
style.configure("title.TButton", font=("Helveticai", 20))
style.configure("setting.TCheckbutton", font=("Helvetica", 20))


#UI
startB = ttk.Button(root, text="START", style="title.TButton", padding=[20], command=mode_select)
settingB = ttk.Button(root, text="SETTING", style="title.TButton", padding=[20], command=setting)
titleL = tk.Label(root, text="SpeedTyping", font=("Helvetica", 80))


se = BooleanVar(root)
seCB = ttk.Checkbutton(root, text="Sound Effect (unstable)", style="setting.TCheckbutton", variable=se)
vol_var = tk.IntVar()
vol_var.set(volume_percent)
volS = ttk.Scale(root, from_=0, to=100, variable=vol_var, command=volume_control)
backB = ttk.Button(root, text="<Back", style="title.TButton", padding=[20], command=title)


modeF = tk.Frame(root, pady=5, padx=5, bd=0)
modeL = tk.Label(root, text="Mode Select", font=("Helvetica", 40))
easyB = ttk.Button(modeF, text="EASY", style="title.TButton", padding=[20], command=easy_mode)
normalB = ttk.Button(modeF, text="NORMAL", style="title.TButton", padding=[20], command=normal_mode)
hardB = ttk.Button(modeF, text="HARD", style="title.TButton", padding=[20], command=hard_mode)


wordL = tk.Label(root, font=("Helvetica", 48))
countL = tk.Label(root, font=("Helvetica", 54))
wordE = ttk.Entry(root, font=("Helvetica", 24), state="disabled", justify="center")
scoreL = tk.Label(root, text="Score: 0", font=("Helvetica", 18))
timerL = tk.Label(root, text=f"Time: {time_limit} ", font=("Helvetica", 18))


accuL = tk.Label(root, font=("Helvetica", 48))
score_rL = tk.Label(root, font=("Helvetica", 48))
buttonF = tk.Frame(root, pady=5, padx=5, bd=0)
contiB = ttk.Button(buttonF, text="CONTINUE", style="title.TButton", padding=[20], command=start_game)
titleB = ttk.Button(buttonF, text="TITLE", style="title.TButton", padding=[20], command=title)


title()

root.mainloop()

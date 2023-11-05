import tkinter as tk
import threading as th
import winsound, random, time, math
from fractions import Fraction


#word.txtの読み込み
with open("word.txt", "r") as f:
    words = f.read().splitlines()
original_words = words.copy()

score = 0
time_limit = 60
start_time = None
game_ended = False

#windowのサイズと開始位置
def display_pos():
    width_dis = root.winfo_screenwidth()
    height_dis = root.winfo_screenheight()
    return str(width_dis // 2) + "x" + str(height_dis // 2) + "+" + str(width_dis // 4) + "+" + str(height_dis // 4)

def start_game():
    global score, start_time, game_ended
    score = 0
    start_time = time.time()
    next_word()
    start_button["state"] = "disabled"
    entry["state"] = "normal"
    countdown()
    game_ended = False

def next_word():
    if len(words) > 0:
        current_word = random.choice(words)
        label.config(text=current_word)
        words.remove(current_word)
    else:
        end_game()

def end_game():
    global score, game_ended
    label.config(text=f"ゲーム終了 スコア: {score}")
    entry.delete(0, tk.END)
    start_button["state"] = "normal"
    entry["state"] = "disabled"
    game_ended = True

def check_word(event):
    global score
    if game_ended:
        return
    user_input = entry.get()
    if user_input == label.cget("text"):
        score += 1
        scoreL.config(text="スコア: " + str(score))
    entry.delete(0, tk.END)
    next_word()

def countdown():
    global time_limit
    if start_time is not None:
        elapsed_time = time.time() - start_time
        remaining_time = max(time_limit - elapsed_time, 0)
        timerL.config(text=f"残り時間: {int(remaining_time)} 秒")
        if elapsed_time >= time_limit:
            end_game()
            entry.unbind("<Return>")
        else:
            root.after(1000, countdown)


#ウィンドウ情報
root = tk.Tk()
root.title("PyTyping")
root.geometry(display_pos())

label = tk.Label(root, font=("Helvetica", 48))
entry = tk.Entry(root, font=("Helvetica", 24), state="disabled")
scoreL = tk.Label(root, text="スコア: 0", font=("Helvetica", 18))
start_button = tk.Button(root, text="スタート", command=start_game)
timerL = tk.Label(root, text=f"残り時間: {time_limit} 秒", font=("Helvetica", 18))

label.pack()
entry.pack()
scoreL.pack()
start_button.pack()
timerL.pack()

entry.bind("<Return>", check_word)

root.mainloop()

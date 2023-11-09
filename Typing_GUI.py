import tkinter as tk
import threading as th
import winsound, random, time, math, keyboard

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
    w_win, h_win = math.floor(w_dis / 2.5), math.floor(h_dis / 2.5)
    return  str(w_win) + "x" + str(h_win) + "+" + str(math.floor(w_dis // 3.3)) + "+" + str(math.floor(h_dis // 3.3))

def reset_pos():
    timerL.place_forget()
    scoreL.place_forget()
    label.place_forget()
    entry.place_forget()
    start_button.place_forget()

def start_ct(sec):
    global ct, start_time
    label.config(text=str(sec))
    if sec > 0:
        ct = root.after(1000, start_ct, sec - 1)
    else:
        if ct:
            root.after_cancel(ct)
        label.config(text="GO!")
        start_button["state"] = "normal"
        entry["state"] = "normal"
        entry.focus_set()
        start_time = time.time()
        next_word()
        countdown()

def start_game():
    global score, game_ended
    score = 0
    start_ct(3)
    start_button.place_forget()
    start_button["state"] = "disabled"
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
    label.config(text="ゲーム終了\nScore: " + str(score))
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
        scoreL.config(text="Score: " + str(score))
    entry.delete(0, tk.END)
    next_word()

def countdown():
    global time_limit
    if start_time is not None:
        elapsed_time = time.time() - start_time
        remaining_time = max(time_limit - elapsed_time, 0)
        timerL.config(text=f"Time: {int(remaining_time)} ")
        if elapsed_time >= time_limit:
            end_game()
            entry.unbind("<Return>")
        else:
            root.after(1000, countdown)


#ウィンドウ情報
root = tk.Tk()
root.geometry(display_pos())
root.update_idletasks()
root.resizable(0,0)
w, h = root.winfo_width(), root.winfo_height()
root.title("PyTyping")

#UI
label = tk.Label(root, font=("Helvetica", 48))
entry = tk.Entry(root, font=("Helvetica", 24), state = "disabled", justify = "center")
scoreL = tk.Label(root, text="Score: 0", font=("Helvetica", 18))
start_button = tk.Button(root, text="Start!", command = start_game)
timerL = tk.Label(root, text=f"Time: {time_limit} ", font = ("Helvetica", 18))

timerL.place(x = w // 10, y = h // 12, anchor = "center")
scoreL.place(x = w // 1.1, y = h // 12, anchor = "center")
label.place(x = w // 2, y = h // 3, anchor = "center")
entry.place(x = w // 2, y = h // 2, anchor = "center")
start_button.place(x = w // 2, y = h // 1.5, anchor = "center")

entry.bind("<Return>", check_word)

root.mainloop()

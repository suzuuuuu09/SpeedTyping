import tkinter as tk
import random, keyboard, pyautogui, time, pyaudio, sys, wave


def TypingGame():
    label.config(text=random.choice(open('word.txt').read().splitlines()))


#開始時のカウントダウン
def StartCount():
    count = 100
    if count > 0:
        for i in range(count):
            start_ct.set(count)
            count -= 1
            time.sleep(1)


#アプリ終了
def quit():
    root.quit()
    root.destroy()

root = tk.Tk()



#開始時カウントダウン
start_ct = tk.StringVar(root)
start_ctL = tk.Label(root, textvariable = start_ct, width = 20, font = ("HG丸ｺﾞｼｯｸM-PRO", 46))
start_ctL.pack(padx = 50, pady = 80)


label = tk.Label(root, width = 20, font = ("HG丸ｺﾞｼｯｸM-PRO", 46))
label.pack(padx = 10, pady = 10)
button = tk.Button(root, text = 'a', command = StartCount)
button.pack(padx = 10, pady = 10)


#ウィンドウ情報
root.geometry("1280x720")
root.title("a")

root.mainloop()

'''
def button_countdown(i, label):
    if i > 0:
        i -= 1
        label.set(i)
        root.after(1000, lambda: button_countdown(i, label))
    else:
        close()

def close():
    root.destroy()

root = tk.Tk()

button_label = tk.StringVar()
button_label.set(10)
tk.Button(root, textvariable=button_label, command=close).pack()
button_countdown(10, button_label)
root.mainloop()
'''
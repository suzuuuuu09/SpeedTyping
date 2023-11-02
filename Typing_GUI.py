import tkinter as tk
import random, keyboard, pygame, pyautogui, time

#word.txtからランダム抽出
myline = random.choice(open('word.txt').read().splitlines())

def TypingGame():
    label.config(text=myline)

#アプリ終了
def quit():
    root.quit()
    root.destroy()

root = tk.Tk()
label = tk.Label(
    root,
    width = 20,
    font = ("HG丸ｺﾞｼｯｸM-PRO",46)
)

label.pack(padx=10, pady=10)

button = tk.Button(
    root,
    text='a',
    command=TypingGame
)
button.pack(padx=10, pady=10)

#ウィンドウサイズ固定
root.geometry("1280x720")
#タイトル名
root.title("a")

root.mainloop()

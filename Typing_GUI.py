import PySimpleGUI as sg
import tkinter as tk
import random, keyboard, pygame, pyautogui

#word.txtからランダム抽出
lines = open('word.txt').read().splitlines()
myline =random.choice(lines)

#GUIのテーマ
sg.theme('SystemDefault')

canvas = sg.Canvas(size=(1280,720))
layout = [[canvas]]

window = sg.Window('サンプル', layout, finalize=True)

canvas.tk_canvas.create_text(640, 360, text=myline, font=("HG丸ｺﾞｼｯｸM-PRO",46))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        for x in myline:
            if keyboard.read_read() == x:
                print(x)

window.close()
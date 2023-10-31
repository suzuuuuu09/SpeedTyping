import PySimpleGUI as sg
import tkinter as tk
import Typing_Game

sg.theme('SystemDefault')

canvas = sg.Canvas(size=(1280,720))
layout = [[canvas]]

window = sg.Window('サンプル', layout, finalize=True)

canvas.tk_canvas.create_text(640, 360, text="fuck", font=("HG丸ｺﾞｼｯｸM-PRO",46))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()
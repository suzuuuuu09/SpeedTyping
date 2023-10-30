import PySimpleGUI as sg
import random

layout = layout = [[sg.Text(key="-TEXT-")], [sg.Button("OK")]]

window = sg.Window("hogehoge", layout, size=(1920, 1080))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "OK":
        f = open("word.txt", "r")
        l = f.readlines()
        s = random.sample(1, 20)
        window["-TEXT-"].update(s)

window.close()

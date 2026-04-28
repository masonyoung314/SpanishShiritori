import PySimpleGUI as sg

# All the stuff inside your window.
layout = [  [sg.Text("Player 1: ")],
            [sg.InputText()],
            # [sg.Output()],
            [sg.Text("Player 2: ")],
            [sg.InputText()],
            # [sg.Output()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

sg.theme("topanga")

# Create the Window
introWindow = sg.Window('Spanish Shiritori', layout)


layout2 = [
    [sg.Text("Welcome to Spanish Shiritori!")]
]
gameWindow = sg.Window('Second Shiritori', layout2)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = introWindow.read()
    player1 = values[0]
    player2 = values[1]
    # if user closes window or clicks cancel

    gameEvent, gameValues = gameWindow.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break



window.close()
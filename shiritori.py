import PySimpleGUI as sg
import keyboard as k

def create_row(row_counter):
    row = [
        sg.pin(
            sg.Col([
                [
                    sg.Text("", key=("-WORD-", row_counter))
                ]
            ],
            key=("-ROW-", row_counter)
            )
        )
    ]
    return row
    

def process_input(word):
    points = len(word)
    return points

# All the stuff inside your window.
layout = [  [sg.Text("Player 1: ")],
            [sg.InputText(key="-PLAYERONEINPUT-")],
            # [sg.Output()],
            [sg.Text("Player 2: ")],
            [sg.InputText(key="-PLAYERTWOINPUT-")],
            # [sg.Output()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

sg.theme("Topanga")

# Create the Window
introWindow = sg.Window('Spanish Shiritori', layout)


playerOnePoints = 150
playerTwoPoints = 150

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = introWindow.read()
    # if user closes window or clicks cancel

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break


    player1 = values["-PLAYERONEINPUT-"]
    player2 = values["-PLAYERTWOINPUT-"]

    layout2 = [
            [sg.Text("Welcome to Spanish Shiritori!")],
            [sg.Text("Player 1", key="-PLAYERONE-"), sg.Push(), sg.Text("Player 2", key="-PLAYERTWO-")],   
            [sg.Column([create_row(0)], key="-PLAYERONEROW-"), sg.Column([create_row(0)], key="-PLAYERTWOROW-")],
            [sg.Text(f"Points: {playerOnePoints}", key="-PLAYERONEPOINTS-"), sg.Push(), sg.Text(f"Points: {playerTwoPoints}", key="-PLAYERTWOPOINTS-")],
            [sg.Input(key="-PLAYERONEWORDINPUT-"), sg.Button("Enter", key="-PLAYER1ENTER-"), sg.Input(key="-PLAYERTWOWORDINPUT-"), sg.Button("Enter", key="-PLAYER2ENTER-")],
            [sg.Button('Cancel')]
        ]
    gameWindow = sg.Window('Second Shiritori', layout2, finalize=True, font=15)

    gameWindow["-PLAYERONE-"].update(player1)
    gameWindow["-PLAYERTWO-"].update(player2)

    row_counter = 0;

    while True:
        gameEvent, gameValues = gameWindow.read()

        if gameEvent == sg.WIN_CLOSED or gameEvent == 'Cancel':
            gameWindow.close()
            break
        elif gameEvent == "-PLAYER1ENTER-":
            gameWindow.extend_layout(gameWindow["-PLAYERONEROW-"], [create_row(row_counter)])
            gameWindow[("-WORD-", row_counter)].update(gameValues["-PLAYERONEWORDINPUT-"])
            gameWindow["-PLAYERONEPOINTS-"].update(playerOnePoints - process_input(gameValues["-PLAYERONEWORDINPUT-"]))
            playerOnePoints -= process_input(gameValues["-PLAYERONEWORDINPUT-"])
        elif gameEvent == "-PLAYER2ENTER-":
            gameWindow.extend_layout(gameWindow["-PLAYERTWOROW-"], [create_row(row_counter)])
            gameWindow[("-WORD-", row_counter)].update(gameValues["-PLAYERTWOWORDINPUT-"])
            gameWindow["-PLAYERTWOPOINTS-"].update(playerTwoPoints - process_input(gameValues["-PLAYERTWOWORDINPUT-"]))
            playerTwoPoints -= process_input(gameValues["-PLAYERTWOWORDINPUT-"])
            row_counter += 1


gameWindow.close()
introWindow.close()

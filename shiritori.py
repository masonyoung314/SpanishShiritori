import PySimpleGUI as sg
import time

def create_row(row_counter, oneOrTwo):
    # Row number and ONE or TWO
    if oneOrTwo == "ONE":
        row = [
            sg.pin(
                sg.Col([
                    [
                        sg.Text("", key=(f"-WORD{oneOrTwo}-", row_counter), justification="left")
                    ]
                ],
                key=("-ROW-", row_counter)
                )
            )
        ]
    else:
        row = [
        sg.pin(
            sg.Col([
                [
                    sg.Text("", key=(f"-WORD{oneOrTwo}-", row_counter), expand_x=True, justification="right", size=(110, 1))
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


def game():


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

        lastLetter1 = '' # last letter of player 1's previous word
        lastLetter2 = '' # last letter of player 2's previous word

        layout2 = [
                [sg.Text("Welcome to Spanish Shiritori!")],
                [sg.Text("Player 1", key="-PLAYERONE-"), sg.Push(), sg.Text("Player 2", key="-PLAYERTWO-")],   
                [sg.Column([create_row(0, "ONE")], key="-PLAYERONEROW-"), sg.Column([create_row(0, "TWO")], key="-PLAYERTWOROW-")],
                [sg.Text(f"Points: {playerOnePoints}", key="-PLAYERONEPOINTS-"), sg.Push(), sg.Text(f"Points: {playerTwoPoints}", key="-PLAYERTWOPOINTS-")],
                [sg.Push(), sg.Text("10", key="-TIMER-"), sg.Push()],
                [sg.Input(key="-PLAYERONEWORDINPUT-"), sg.Button("Enter", key="-PLAYER1ENTER-"), sg.Push(), sg.Input(key="-PLAYERTWOWORDINPUT-"), sg.Button("Enter", key="-PLAYER2ENTER-")],
                [sg.Push(), sg.Text(key="-ERROROUTONE-"), sg.Push()],
                [sg.Button('Cancel')]
            ]
        gameWindow = sg.Window('Second Shiritori', layout2, finalize=True, font=15)

        gameWindow["-PLAYERONE-"].update(f"Player 1: {player1}")
        gameWindow["-PLAYERTWO-"].update(f"Player 2: {player2}")

        row_counter = 0;

        turn = 1

        while True:
            gameEvent, gameValues = gameWindow.read()

            winner = None

            layout3 = [
                [sg.Push(), sg.Text("You Win!!!"), sg.Push()],
                [sg.Push(), sg.Text(winner, key="-WINNER-"), sg.Push()],
                [sg.Button("Exit", key="-ENDEXIT-"), sg.Button("Play Again", key="-REPEAT-")]
            ]


            seconds = 10
            time_init = time.time()
            while seconds > 10:
                new_time = time.time()
                if new_time - time_init >= 1:
                    seconds -= 1
                    gameWindow["-TIMER-"].update(seconds)
                elif gameEvent == "-PLAYER1ENTER-" or gameEvent == "-PLAYER2ENTER-" or gameEvent == sg.WIN_CLOSED or gameEvent == "Cancel":
                    break
            
            if time == 0:
                gameWindow["-ERROROUTONE-"].update("Out of time")
                
                turn = 2 if turn == 1 else turn = 1

            if gameEvent == sg.WIN_CLOSED or gameEvent == 'Cancel':
                # gameWindow.close()
                break
            elif gameEvent == "-PLAYER1ENTER-" and turn == 1:
                gameWindow.extend_layout(gameWindow["-PLAYERONEROW-"], [create_row(row_counter, "ONE")])
                gameWindow[("-WORDONE-", row_counter)].update(gameValues["-PLAYERONEWORDINPUT-"])
                word = gameValues["-PLAYERONEWORDINPUT-"]

                if len(word) < 4:
                    gameWindow["-ERROROUTONE-"].update("Word must be at least 4 letters.")
                elif word[0] != lastLetter2 and lastLetter2 != '':
                    gameWindow["-ERROROUTONE-"].update(f"Your word doesn't start with {lastLetter2}")

                else:
                    gameWindow["-PLAYERONEPOINTS-"].update(f"Points: {playerOnePoints - process_input(gameValues["-PLAYERONEWORDINPUT-"])}")
                    playerOnePoints -= process_input(gameValues["-PLAYERONEWORDINPUT-"])
                    lastLetter1 = word[len(word) - 1]
                    gameWindow["-PLAYERTWOWORDINPUT-"].update(lastLetter1)
                    gameWindow["-ERROROUTONE-"].update("")
                    turn = 2
                    print(turn)

            elif gameEvent == "-PLAYER2ENTER-" and turn == 2:
                gameWindow.extend_layout(gameWindow["-PLAYERTWOROW-"], [create_row(row_counter, "TWO")])
                gameWindow[("-WORDTWO-", row_counter)].update(gameValues["-PLAYERTWOWORDINPUT-"])
                word = gameValues["-PLAYERTWOWORDINPUT-"]
                if len(word) < 4:
                    gameWindow["-ERROROUTONE-"].update("Word must be at least 4 letters.")
                elif word[0] != lastLetter1 and lastLetter1 != '':
                    gameWindow["-ERROROUTONE-"].update(f"Your word doesn't start with {lastLetter1}")
                else:
                    gameWindow["-PLAYERTWOPOINTS-"].update(f"Points: {playerTwoPoints - process_input(gameValues["-PLAYERTWOWORDINPUT-"])}")
                    playerTwoPoints -= process_input(gameValues["-PLAYERTWOWORDINPUT-"])
                    row_counter += 1
                    lastLetter2 = word[len(word) - 1]
                    gameWindow["-PLAYERONEWORDINPUT-"].update(lastLetter2)
                    gameWindow["-ERROROUTONE-"].update("")
                    turn = 1
            
            elif (gameEvent == "-PLAYER1ENTER-" and turn == 2) or (gameEvent == "-PLAYER2ENTER-" and turn == 1):
                gameWindow["-ERROROUTONE-"].update("It is not your turn.")


            if playerOnePoints <= 0 or playerTwoPoints <= 0:
                endWindow = sg.Window('Winner', layout3, finalize=True, font=30)
                winner = player1 if playerOnePoints <= 0 else player2
                endWindow["-WINNER-"].update(winner)

                while True:
                    endEvent, endValues = endWindow.read()

                    
                    if endEvent == sg.WIN_CLOSED or endEvent == "-ENDEXIT-":
                        endWindow.close()
                        gameWindow.close()
                        break
                    elif endEvent == "-REPEAT-":
                        endWindow.close()
                        gameWindow.close()
                        introWindow.close()
                        game()
        
            # endWindow.close()
        gameWindow.close()
    introWindow.close()


game()

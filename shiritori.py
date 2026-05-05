import PySimpleGUI as sg
import time
import enchant
import random
import string



orange = "#c15226"
purple = "#7a4d5f"
green = "#889743"


# theme = sg.LOOK_AND_FEEL_TABLE['Topanga']

# for key, value in theme.items():
#     print(f"{key}: {value}")


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
                    sg.Text("", key=(f"-WORD{oneOrTwo}-", row_counter), expand_x=True, justification="right", size=(110, 1), text_color=green)
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


# Check if word exists
# Pass in the word and the dictionary
def is_word(d, word):
    return True if d.check(word) == True else False


# Message Codes:
# 1 = Player 1 
# 2 = Player 2
# 3 = Cancel
# 4 = Spanish
# 5 = Welcome
# 6 = Points
# 7 = Enter
# 8 = Win
# 9 = Again
# 10 = Instructions
# 11 = Rules
# 12 = English

def print_message(spanish, message_code):
    message = ""

    if spanish == True:
        if message_code == 1:
            message = "Jugador 1:"
        elif message_code == 2:
            message = "Jugador 2:"
        elif message_code == 3:
            message = "Salir"
        elif message_code == 4:
            message = "Español"
        elif message_code == 5:
            message = "¡Bienvenidos a Shiritori en español!"
        elif message_code == 6:
            message = "Puntos: "
        elif message_code == 7:
            message = "Ok"
        elif message_code == 8:
            message = "Has ganado!!!"
        elif message_code == 9:
            message = "Jugar otra vez"
        elif message_code == 10:
            message = "Instrucciones"
        elif message_code == 11:
            message = """
            Reglas:
            - Tu palabra debe contener al menos 4 letras.
            - Tu palabra debe empezar por la letra al final de la palabra del otro jugador.
            - Tienes que poner tu palabra antes de que se acaba el tiempo (10 segundos).
            - No word can be used twice.
            - Tus puntos bajan por la longitud de tu palabra.
            - El primer jugador que tiene 0 o menos puntos gana!
            """
        elif message_code == 12:
            message = "Inglés"

    else:
        if message_code == 1:
            message = "Player 1:"
        elif message_code == 2:
            message = "Player 2:"
        elif message_code == 3:
            message = "Exit"
        elif message_code == 4:
            message = "Spanish"
        elif message_code == 5:
            message = "Welcome to Spanish Shiritori!"
        elif message_code == 6:
            message = "Points: "
        elif message_code == 7:
            message = "Ok"
        elif message_code == 8:
            message = "You Win!!!"
        elif message_code == 9:
            message = "Play Again"
        elif message_code == 10:
            message = "Instructions"
        elif message_code == 11:
            message = """
            Rules:
            - Your word must have at least 4 letters.
            - Your word must start with the last letter of the previous word entered by the other player.
            - You must respond with your word before the timer ends (10 seconds).
            - No puedes repetir palabras.
            - Your points lower relative correspondingly with the length of your word.
            - The first player to reach 0 or less points wins!
            """
        elif message_code == 12:
            message = "English"

    return message

# Error Codes
# 1 = Out of time
# 2 = Word not long enough
# 3 = Word doesn't start with correct letter
# 4 = Word doesn't exist
# 5 = Not your turn

def print_error(spanish, code, correct_letter = "", incorrect_word=""):
    message = ""
    if spanish == True:
        if code == 1:
            message = "Oh no! Tu tiempo se ha acabado."
        elif code == 2:
            message = "Tu palabra no tiene al menos 4 letras."
        elif code == 3:
            message = f"Tu palabra no empieza con la letra {correct_letter}."
        elif code == 4:
            message = f"{incorrect_word} no existe."
        elif code == 5:
            message = "No es tu turno."
        elif code == 6:
            message = "No puedes repetir palabras."
    else:
        if code == 1:
            message = "Oh no! You ran out of time."
        elif code == 2:
            message = "Word must have at least 4 letters."
        elif code == 3:
            message = f"Your word doesn't start with {correct_letter}."
        elif code == 4:
            message = f"{incorrect_word} doesn't exist."
        elif code == 5:
            message = "It is not your turn."
        elif code == 6:
            message = "You can't use the same word twice."

    return message

def main():

    global DICT
    DICT = enchant.Dict("es")
    # All the stuff inside your window.
    layout = [  [sg.Text(print_message(spanish=1, message_code=1), key="-PLAYERONENAME-", text_color="#E7C855", background_color="#292923")],
                [sg.InputText(key="-PLAYERONEINPUT-")],
                # [sg.Output()],
                [sg.Text(print_message(spanish=1, message_code=2), key="-PLAYERTWONAME-", text_color="#E7C855", background_color="#292923")],
                [sg.InputText(key="-PLAYERTWOINPUT-", enable_events=True)],
                # [sg.Output()],
                [sg.Button('Ok'), sg.Button(print_message(spanish=1, message_code=10), key="-INSTRUCTIONS-"),
                 sg.Button(print_message(spanish=1, message_code=3), key="-CANCEL-"), sg.Text(print_message(spanish=1, message_code=12), key="-ENGLISH-", background_color="#292923", text_color="#E7C855"),
                 sg.Image(toggle_btn_on, key='-TOGGLE-GRAPHIC-', enable_events=True, metadata=False, background_color="#292923", size=(50,50), zoom=1, subsample=20),
                 sg.Text(print_message(spanish=1, message_code=4), background_color="#292923", key="-SPANISH-", text_color="#E7C855")],
                 [sg.Text("", key="-INSTRUCTIONSINFO-", text_color="#E7C855", background_color="#292923")]
                 
            ]

    sg.theme("Topanga")

    alphabet = list(string.ascii_lowercase)

    # Create the Window
    introWindow = sg.Window('Spanish Shiritori', layout)


    playerOnePoints = 150
    playerTwoPoints = 150

    spanish = True
    instructions = False
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = introWindow.read()
        # if user closes window or clicks cancel


        introWindow["-PLAYERTWOINPUT-"].bind("<Return>", "_Enter")
        if event == sg.WIN_CLOSED or event == "-CANCEL-":
            break

        elif event == "-TOGGLE-GRAPHIC-":
            introWindow['-TOGGLE-GRAPHIC-'].metadata = not introWindow['-TOGGLE-GRAPHIC-'].metadata
            introWindow['-TOGGLE-GRAPHIC-'].update(toggle_btn_off if introWindow['-TOGGLE-GRAPHIC-'].metadata else toggle_btn_on, subsample=20)
            spanish = False if spanish == True else True
            introWindow["-PLAYERONENAME-"].update(print_message(spanish, 1))
            introWindow["-PLAYERTWONAME-"].update(print_message(spanish, 2))
            introWindow["-CANCEL-"].update(print_message(spanish, 3))
            introWindow["-SPANISH-"].update(print_message(spanish, 4))
            introWindow["-ENGLISH-"].update(print_message(spanish, 12))
            introWindow["-INSTRUCTIONS-"].update(print_message(spanish, 10))
            if instructions == True:
                introWindow["-INSTRUCTIONSINFO-"].update(print_message(spanish, 11))

            DICT = enchant.Dict("en_US") if spanish == False else enchant.Dict("es")

        elif event == "-INSTRUCTIONS-":
            if instructions == False:
                introWindow["-INSTRUCTIONSINFO-"].update(print_message(spanish, 11))
                instructions = True
            else:
                introWindow["-INSTRUCTIONSINFO-"].update("")
                instructions = False

        elif event == "Ok" or event == "-PLAYERTWOINPUT-" + "_Enter":

            player1 = values["-PLAYERONEINPUT-"]
            player2 = values["-PLAYERTWOINPUT-"]

            lastLetter1 = '' # last letter of player 1's previous word
            lastLetter2 = '' # last letter of player 2's previous word

            layout2 = [
                    [sg.Text(print_message(spanish, 5))],
                    [sg.Text(print_message(spanish, 1), key="-PLAYERONE-"), sg.Push(), sg.Text(print_message(spanish, 2), key="-PLAYERTWO-", text_color=green)],   
                    [sg.Column([create_row(0, "ONE")], key="-PLAYERONEROW-"), sg.Column([create_row(0, "TWO")], key="-PLAYERTWOROW-")],
                    [sg.Text(f"{print_message(spanish, 6)} {playerOnePoints}", key="-PLAYERONEPOINTS-"), sg.Push(), sg.Text(f"{print_message(spanish, 6)} {playerTwoPoints}", key="-PLAYERTWOPOINTS-", text_color=green)],
                    [sg.Push(), sg.Text("10", key="-TIMER-", font="Arial 50 bold"), sg.Push()],
                    [sg.Input(default_text=random.choice(alphabet), key="-PLAYERONEWORDINPUT-"), sg.Button(print_message(spanish, 7), key="-PLAYER1ENTER-"), sg.Push(), sg.Input(key="-PLAYERTWOWORDINPUT-", text_color=green), sg.Button(print_message(spanish, 7), key="-PLAYER2ENTER-", button_color=(green, "#284B5A"))],
                    [sg.Push(), sg.Text("", key="-ERROROUTONE-", font="Arial 20 bold", text_color=orange), sg.Push()],
                    [sg.Button(print_message(spanish, 3), key="-CANCEL-")]
                ]
            gameWindow = sg.Window('Game', layout2, finalize=True, font=15)


            gameWindow["-PLAYERONE-"].update(f"{print_message(spanish, 1)} {player1}")
            gameWindow["-PLAYERTWO-"].update(f"{print_message(spanish, 2)} {player2}")


            row_counter = 0;

            turn = 1
            seconds = 10
            time_init = time.time()

            gameWindow["-PLAYERONEWORDINPUT-"].set_focus()

            playerOneWords = []
            playerTwoWords = []

            while True:
                gameEvent, gameValues = gameWindow.read(timeout=1000)
                gameWindow["-PLAYERONEWORDINPUT-"].bind("<Return>", "_Enter")
                gameWindow["-PLAYERTWOWORDINPUT-"].bind("<Return>", "_Enter")

                winner = None

                layout3 = [
                    [sg.Push(), sg.Text(print_message(spanish, 8)), sg.Push()],
                    [sg.Push(), sg.Text(winner, key="-WINNER-"), sg.Push()],
                    [sg.Button(print_message(spanish, 3), key="-ENDEXIT-"), sg.Button(print_message(spanish, 9), key="-REPEAT-")]
                ]

                if gameEvent == sg.TIMEOUT_EVENT:
                    new_time = time.time()
                    if new_time - time_init >= 1:
                        seconds -= 1
                        gameWindow["-TIMER-"].update(seconds)
                    elif gameEvent == "-PLAYER1ENTER-" or gameEvent == "-PLAYER2ENTER-" or gameEvent == sg.WIN_CLOSED or gameEvent == "Cancel":
                        seconds = 10
                        break
                        
                if seconds <= 0:
                    gameWindow["-ERROROUTONE-"].update(print_error(spanish, 1))
                    gameWindow["-PLAYERONEWORDINPUT-"].update(lastLetter1) if turn == 2 else gameWindow["-PLAYERTWOWORDINPUT-"].update(lastLetter2)
                    turn = 2 if turn == 1 else 1
                    seconds = 10

                if gameEvent == sg.WIN_CLOSED or gameEvent == "-CANCEL-":
                    # gameWindow.close()
                    break
                elif (gameEvent == "-PLAYER1ENTER-" or gameEvent == "-PLAYERONEWORDINPUT-" + "_Enter") and turn == 1:
                    gameWindow.extend_layout(gameWindow["-PLAYERONEROW-"], [create_row(row_counter, "ONE")])
                    gameWindow[("-WORDONE-", row_counter)].update(gameValues["-PLAYERONEWORDINPUT-"])
                    word = gameValues["-PLAYERONEWORDINPUT-"]

                    if len(word) < 4:
                        gameWindow["-ERROROUTONE-"].update(print_error(spanish, 2))
                    elif word[0] != lastLetter2 and lastLetter2 != '':
                        gameWindow["-ERROROUTONE-"].update(print_error(spanish, 3, lastLetter2))
                        gameWindow["-PLAYERONEWORDINPUT-"].update(lastLetter2)
                    elif not is_word(DICT, word):
                        gameWindow["-ERROROUTONE-"].update(print_error(spanish, 4, incorrect_word={word}))
                    elif word in playerOneWords or word in playerTwoWords:
                        gameWindow["-ERROROUTONE-"].update(print_error(spanish, 6))

                    else:
                        gameWindow["-PLAYERONEPOINTS-"].update(f"Points: {playerOnePoints - process_input(gameValues["-PLAYERONEWORDINPUT-"])}")
                        playerOnePoints -= process_input(gameValues["-PLAYERONEWORDINPUT-"])
                        lastLetter1 = word[len(word) - 1]
                        gameWindow["-PLAYERTWOWORDINPUT-"].update(lastLetter1)
                        gameWindow["-ERROROUTONE-"].update("")
                        turn = 2
                        seconds = 10
                        gameWindow["-TIMER-"].update(seconds)
                        gameWindow["-PLAYERTWOWORDINPUT-"].set_focus()
                        playerOneWords.append(word)

                elif (gameEvent == "-PLAYER2ENTER-" or gameEvent == "-PLAYERTWOWORDINPUT-" + "_Enter") and turn == 2:
                    gameWindow.extend_layout(gameWindow["-PLAYERTWOROW-"], [create_row(row_counter, "TWO")])
                    gameWindow[("-WORDTWO-", row_counter)].update(gameValues["-PLAYERTWOWORDINPUT-"])
                    word = gameValues["-PLAYERTWOWORDINPUT-"]
                    if len(word) < 4:
                        gameWindow["-ERROROUTONE-"].update(print_error(spanish, 2))
                    elif word[0] != lastLetter1 and lastLetter1 != '':
                        gameWindow["-ERROROUTONE-"].update(print_error(spanish, 3, lastLetter1))
                        gameWindow["-PLAYERTWOWORDINPUT-"].update(lastLetter1)
                    elif not is_word(DICT, word):
                        gameWindow["-ERROROUTONE-"].update(print_error(spanish, 4, incorrect_word={word}))
                    elif word in playerOneWords or word in playerTwoWords:
                        gameWindow["-ERROROUTONE-"].update(print_error(spanish, 6))
                    else:
                        gameWindow["-PLAYERTWOPOINTS-"].update(f"Points: {playerTwoPoints - process_input(gameValues["-PLAYERTWOWORDINPUT-"])}")
                        playerTwoPoints -= process_input(gameValues["-PLAYERTWOWORDINPUT-"])
                        row_counter += 1
                        lastLetter2 = word[len(word) - 1]
                        gameWindow["-PLAYERONEWORDINPUT-"].update(lastLetter2)
                        gameWindow["-ERROROUTONE-"].update("")
                        turn = 1
                        seconds = 10
                        gameWindow["-TIMER-"].update(seconds)
                        gameWindow["-PLAYERONEWORDINPUT-"].set_focus()
                        playerTwoWords.append(word)
                
                elif (gameEvent == "-PLAYER1ENTER-" and turn == 2) or (gameEvent == "-PLAYER2ENTER-" and turn == 1):
                    gameWindow["-ERROROUTONE-"].update(print_error(spanish, 5))


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
                            main()
            
                # endWindow.close()
            gameWindow.close()
    introWindow.close()


if __name__ == "__main__":
    toggle_btn_off = "/Users/masonyoung/Desktop/Personal_Projects/Shiritori/RealToggleOff.png"
    toggle_btn_on = "/Users/masonyoung/Desktop/Personal_Projects/Shiritori/RealToggleOn.png"

    main()
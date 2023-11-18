## import libraries for GUI, nlp and regexes
import PySimpleGUI as sg
import nltk
from nltk.corpus import words
import re

## color
sg.theme("DarkTeal9")

## input fields
layout = [
    [sg.Text("Enter ur password, ma`am", size=(20,1)), sg.InputText(key="Password", password_char='*')],
    [sg.Submit(), sg.Exit()]
]

window = sg.Window('Password strength checker', layout)

## for later time estimation
entropy = 0
crack_speed = 40000000000

policies = {'Uppercase characters': 0,
            'Lowercase characters': 0,
            'Special characters': 0,
            'Numbers': 0}

entropies = {'Uppercase characters': 26,
             'Lowercase characters': 26,
             'Special characters': 33,
             'Numbers': 10}


## run program
while True:
    ## read user input from fields
    event, values = window.read()
    raw_password = list(values.values())[-1]
    letters = re.findall(r'\D+|\d+', raw_password)
    length = len(raw_password)
    res = True

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    ## the beginning of estimation process
    if event == 'Submit':
        print(letters)
        ## check if too short
        if length > 8:
            ## keep track of type and amount of characters
            for char in raw_password:
                if re.match("[0-9]", char):
                    policies["Numbers"] += 1
                elif re.match("[a-z]", char):
                    policies["Lowercase characters"] += 1
                elif re.match("[A-Z]", char):
                    policies["Uppercase characters"] += 1
                else: 
                    policies["Special characters"] += 1

            ## also for later time estimation
            for policy in policies.keys():
                num = policies[policy] if policies[policy] > 0 else '-'
                if policies[policy] > 0:
                    entropy += entropies[policy]

            # Calculate the time
            time_ = "hours"
            cracked = ((entropy**length) / crack_speed) / 3600
            if cracked > 24:
                cracked = cracked / 24
                time_ = "days"
            if cracked > 365:
                cracked = cracked / 365
                time_ = "years"
            if time_ == "years" and cracked > 100:
                cracked = cracked / 100
                time_ = "centuries"
            if time_ == "centuries" and cracked > 1000:
                cracked = cracked / 1000
                time_ = "millennia"

            ## check for real English words
            for i in letters:
                if i in words.words():
                    print(i)
                    res = False
                else:
                    res = True

            ## display warnings and time to crack
            sg.popup_ok("\n[+] Time to crack password:   {:,.2f} {}".format(cracked, time_))
            if res == False:
                sg.popup_error("password contains real words lol")
            if policies["Numbers"] == 0:
                sg.popup_error("password doesnt contain digits lol")
            if policies["Uppercase characters"] == 0:
                sg.popup_error("password doesnt contain uppercase letters lol")
            if policies["Special characters"] == 0:
                sg.popup_error("password doesnt contain any special chars")
            else:
                sg.popup_ok("cool, we re good")
        else:
            sg.popup_error("if ur dick is short, doesnt mean ur passw has to.. lol")


## well... close the window
window.close()
## delete password from memory
del raw_password, values, letters

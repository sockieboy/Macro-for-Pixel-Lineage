import pyautogui as auto
import pydirectinput as key
import time
import numpy as np
from pynput import keyboard
import os
auto.FAILSAFE = True
auto.PAUSE = 0.05

Options = {"AttackS","SkillS","ScrollS","GuardS","MeditatS","SatchelS"}
Selected = ''

def wait(x):
    time.sleep(x)

def WhatIsSelected():
    loops = 50
    for i in loops:
        for a in len(Options):
            if auto.pixelMatchesColor(50, 1245+a*45, (231, 196, 120), tolerance=10):
                global Selected
                Selected = Options[a]
                return a
        wait(.025) 
def SelectionMove(Selection):
    if WhatIsSelected() == None:
        PhaseCheck()
    elif WhatIsSelected() != Selection:
        if WhatIsSelected() < Selection:
            var = 6-abs(WhatIsSelected-Selection)
        else:
            var = abs(Selection-WhatIsSelected())
        for a in range(var):
           key.press("s")
 
def PhaseCheck():
    if auto.pixelMatchesColor(218, 1430, (231, 196, 120), tolerance=10):
        PathSelection()
        print("pathselecting")
    elif auto.pixelMatchesColor(2349, 1171, (214, 60, 56), tolerance=10):
        AttackSequence()
        print("attack")
def PathSelection():
    for a in range(3):
        #champion
        if auto.pixelMatchesColor(815, 700+200*a, (240, 110, 90), tolerance=10):
            key.moveTo(1200, 700+200*a)
            key.click()
        #mini boss
        elif auto.pixelMatchesColor(815, 700+200*a, (255, 120, 60), tolerance=10):
            key.moveTo(1200, 700+200*a)
            key.click()
        #bush
        elif auto.pixelMatchesColor(815, 700+200*a, (170, 130, 240), tolerance=10):
            key.moveTo(1200, 700+200*a)
            key.click()
            while auto.pixelMatchesColor(1772, 708, (235, 205, 140), tolerance=10) == False:
                key.moveTo(1772, 708)
                key.click()
        #scout
        elif auto.pixelMatchesColor(815, 700+200*a, (240, 200, 90), tolerance=10):
            key.moveTo(1200, 700+200*a)
            key.click()
            while auto.pixelMatchesColor(1941, 843, (235, 205, 140), tolerance=10) == False:
                key.moveTo(1941, 843)
                key.click()
        #trader
        elif auto.pixelMatchesColor(815, 700+200*a, (92, 170, 76), tolerance=10):
            key.moveTo(1200, 700+200*a)
            key.click()
            while auto.pixelMatchesColor(1838, 848, (235, 205, 140), tolerance=10) == False:
                key.moveTo(1838, 848)
                key.click()
    AttackSequence()

def AttackSequence():
    wait(1)
    while auto.pixelMatchesColor(2349, 1171, (214, 60, 56), tolerance=10) == False:
        wait(.2)
    SelectionMove(2)
    key.press("space")
    key.press("w")
    key.press("w")
    key.press("space")
    key.press("space")
    if auto.pixelMatchesColor(2072, 103, (232, 192, 92), tolerance=10):
        key.press("w")
        key.press("space")
    while auto.pixelMatchesColor(2349, 1171, (214, 60, 56), tolerance=10) == True:
        key.press("space")
        wait(.1)
    wait(1)
    if auto.pixelMatchesColor(318,1442, (106,92,63), tolerance=10):
        key.moveTo(1364, 900)
        key.click()
    elif auto.pixelMatchesColor(1353,1031, (235,205,140), tolerance=10):
        key.moveTo(1353,1031)
        key.click()
    PhaseCheck()

    PhaseCheck()
def main():
    AttackSequence()

def StartExitFunction(key):
    if key == keyboard.Key.f8:
        print("ON")
        main()
    elif key == keyboard.Key.esc:
        print("Exiting")
        os._exit(0)
with keyboard.Listener(on_press=StartExitFunction) as listener:
    print("F8 = start, Press esc to exit")
    listener.join()
    

        
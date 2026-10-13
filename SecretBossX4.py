import pyautogui as auto
import pydirectinput as key
import time
import numpy as np
from pynput import keyboard
import os
import threading
auto.FAILSAFE = True
auto.PAUSE = 0.05

Options = {"AttackS","SkillS","ScrollS","GuardS","MeditatS","SatchelS"}
RGBofPathSelectionsList = [[240, 110, 90], [255, 120, 60], [170, 130, 240], [240, 200, 90], [120, 220, 160], [255, 80, 90] ]
stop = threading.Event()
main_thread = None


def wait(x):
    time.sleep(x)
def ReturnMouse():
    key.moveTo(100,1000)
def WhatIsSelected():
    for a in range(6):
        if auto.pixelMatchesColor(300, 1225+(a*50), (30, 45, 65), tolerance=0):
            print(a)
            return a
def SelectionMove(Selection):
    print("selecting move")
    if WhatIsSelected() == None:
        PhaseCheck()
    elif WhatIsSelected() != Selection:
        if WhatIsSelected() > Selection:
            for a in range(WhatIsSelected() - Selection):
                key.press("w")
        else:
            for a in range(Selection-WhatIsSelected()):
                key.press("s")
def PhaseCheck():
    print("phase checking")
    ReturnMouse()
    while True:
        if auto.pixelMatchesColor(2121, 1168, (231, 196, 120), tolerance=10):
            key.moveTo(2349, 1171)
            key.moveRel(1, 0)
            key.doubleClick() 
            ReturnMouse()
        if auto.pixelMatchesColor(218, 1430, (231, 196, 120), tolerance=10):
            print("pathselecting")
            PathSelection()
        elif auto.pixelMatchesColor(2349, 1171, (214, 60, 56), tolerance=10):
            print("attack")
            AttackSequence()
def PathSelection():
    for a in range(5):
        for b in range(3):
            if auto.pixelMatchesColor(815, 700+200*b, (RGBofPathSelectionsList[a]), tolerance=10):
                key.moveTo(1200, 700+200*b)
                key.moveRel(1, 0)
                key.doubleClick()
                if a == 2:
                    while auto.pixelMatchesColor(2349, 1171, (214, 60, 56), tolerance=10) == False:
                        key.moveTo(1772, 708)
                        key.moveRel(1, 0)
                        key.doubleClick() 
                elif a == 3:
                    while auto.pixelMatchesColor(2349, 1171, (214, 60, 56), tolerance=10) == False:
                        key.moveTo(1941, 843)
                        key.moveRel(1, 0)
                        key.doubleClick() 
                elif a == 4:
                    while auto.pixelMatchesColor(2349, 1171, (214, 60, 56), tolerance=10) == False:
                        key.moveTo(1838, 848)
                        key.moveRel(1, 0)
                        key.doubleClick() 
            elif auto.pixelMatchesColor(815, 859, (255, 80, 90), tolerance=10):
                key.moveTo(1300, 1000)
                key.moveRel(1, 0)
                key.doubleClick()    
                break
def AttackSequence():
    boss = False
    ReturnMouse()
    while auto.pixelMatchesColor(2349, 1171, (214, 60, 56), tolerance=10) == False:
        wait(.01)
    SelectionMove(1)
    key.press("space")
    key.press("w")
    key.press("w")
    key.press("space")
    key.press("space")
    while auto.pixelMatchesColor(2349, 1171, (214, 60, 56), tolerance=10):
        key.moveTo(231,1222)
        key.moveRel(1, 0)
        key.doubleClick()
        wait(.05)
        #fix this, spam space bar 
    while auto.pixelMatchesColor(1360, 886, (231, 196, 120), tolerance=10) == False and auto.pixelMatchesColor(1362, 1042, (231, 196, 120), tolerance=10) == False and auto.pixelMatchesColor(218, 1430, (231, 196, 120), tolerance=10) == False:
        key.press("space")
        wait(.1)
    while True:
        ReturnMouse()
        key.moveRel(1, 0)
        print("choosing path")
        # after bosses
        if auto.pixelMatchesColor(1360, 886, (231, 196, 120), tolerance=10):
            key.moveTo(1360, 886)
            key.moveRel(1, 0)
            key.doubleClick()
        #after stage finishes
        elif auto.pixelMatchesColor(1362, 1042, (231, 196, 120), tolerance=10):
            key.moveTo(1362, 1042)
            key.moveRel(1, 0)
            key.doubleClick()
   # give the screen time to update
        if auto.pixelMatchesColor(218, 1430, (231, 196, 120), tolerance=10) or WhatIsSelected() != None:
            break
    ReturnMouse()
    key.moveRel(1, 0)
    ReturnMouse()
    key.moveRel(1, 0)
    ReturnMouse()
    PhaseCheck()

    PhaseCheck()
def main():
    while not stop.is_set():
        ReturnMouse()
        PhaseCheck()
        wait(0.1)
def StartExitFunction(key):
    global main_thread
    if key == keyboard.Key.f8:
        if main_thread is None or not main_thread.is_alive():
            print("ON")
            stop.clear()
            main_thread = threading.Thread(target=main, daemon=True)
            main_thread.start()
        else:
            print("OFF")
            stop.set()          # main finishes its current loop and stops
    elif key == keyboard.Key.esc:
        print("Exiting")
        os._exit(0)
with keyboard.Listener(on_press=StartExitFunction) as listener:
    print("F8 = start, Esc = exit")
    listener.join() 


        
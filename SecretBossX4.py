import pyautogui as auto
import pydirectinput as key
import time
import numpy as np
import Images
from pynput import keyboard
import os
def wait(x):
    time.sleep(x)


auto.FAILSAFE = True
auto.PAUSE = 0.05

#Finds whats being selected

Options = {"AttackS","SkillS","ScrollS","GuardS","MeditatS","SatchelS"}
Selected = ''
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
    if auto.pixelMatchesColor(218, 1430, (235, 205, 140), tolerance=10):
        
    return 'phase'


def AttackSequence():
    # selects big AOE attack (change if needed)
    WhatIsSelected()
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
    

        
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


def SelectingTheSkillButton(checks=40):
    """Checks for the arrow up to `checks` times. Returns True the moment it's found."""
    for i in range(checks):
        if auto.pixelMatchesColor(49, 1294, (231, 196, 120), tolerance=10):
            return True
        wait(0.025)
    return False

def AttackSequence():
    # selects big AOE attack (change if needed)
    while not SelectingTheSkillButton():
        key.press("s")
    print("works")   # arrow found, continue from here

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
    

        
import pyautogui as auto
import pydirectinput as key
import time
from pynput import keyboard
import os
import threading

auto.FAILSAFE = True
auto.PAUSE = 0.05

RGBofPathSelectionsList = [(240, 110, 90), (255, 120, 60), (170, 130, 240),
                           (240, 200, 90), (120, 220, 160), (255, 80, 90)]
GOLD = (231, 196, 120)
ATTACK_RED = (214, 60, 56)

stop = threading.Event()
main_thread = None


# ---------- helpers ----------

def wait(x):
    time.sleep(x)

def ReturnMouse():
    key.moveTo(100, 1000)

def click_at(x, y):
    key.moveTo(x, y)
    key.moveRel(1, 0)
    key.doubleClick()

def is_color(x, y, rgb, tol=10):
    return auto.pixelMatchesColor(x, y, rgb, tolerance=tol)

def attack_ready():
    return is_color(2349, 1171, ATTACK_RED)

def click_until_attack(x, y):
    while not stop.is_set() and not attack_ready():
        click_at(x, y)
        wait(0.2)


# ---------- game logic ----------

def WhatIsSelected():
    for a in range(6):
        if is_color(300, 1225 + a*50, (30, 45, 65), tol=8):
            print("selected:", a)
            return a
    return None

def SelectionMove(target):
    print("selecting move")
    current = WhatIsSelected()          # check once
    if current is None:
        return                          # PhaseCheck will sort it out
    if current > target:
        for _ in range(current - target):
            key.press("w")
    elif current < target:
        for _ in range(target - current):
            key.press("s")

def PathSelection():
    for a in range(5):
        for b in range(3):
            if is_color(815, 700 + 200*b, RGBofPathSelectionsList[a]):
                click_at(1200, 700 + 200*b)
                wait(0.3)
                if a == 2:
                    click_until_attack(1772, 708)
                elif a == 3:
                    click_until_attack(1941, 843)
                elif a == 4:
                    click_until_attack(1838, 848)
                return
            elif is_color(815, 859, (255, 80, 90)):
                click_at(1300, 1000)
                return

def AttackSequence():
    ReturnMouse()
    while not stop.is_set() and not attack_ready():
        wait(0.05)

    SelectionMove(1)
    key.press("space")
    key.press("w")
    key.press("w")
    key.press("space")
    key.press("space")

    while not stop.is_set() and attack_ready():
        click_at(231, 1222)
        wait(0.05)

    # spam space until a "next" button or the path screen shows up
    while not stop.is_set() and not (
            is_color(1360, 886, GOLD)
            or is_color(1362, 1042, GOLD)
            or is_color(218, 1430, GOLD)):
        key.press("space")
        wait(0.1)

    while not stop.is_set():
        ReturnMouse()
        key.moveRel(1, 0)
        print("choosing path")
        if is_color(1360, 886, GOLD):         # after bosses
            click_at(1360, 886)
        elif is_color(1362, 1042, GOLD):      # after stage finishes
            click_at(1362, 1042)
        wait(0.3)                             # give the screen time to update
        if is_color(218, 1430, GOLD) or WhatIsSelected() is not None:
            break

    ReturnMouse()
    # no PhaseCheck() here: just return, PhaseCheck's loop carries on

def PhaseCheck():
    print("phase checking")
    ReturnMouse()
    while not stop.is_set():                  # F8 can now stop it
        if is_color(2121, 1168, GOLD):
            click_at(2349, 1171)
            ReturnMouse()
        if is_color(218, 1430, GOLD):
            print("pathselecting")
            PathSelection()                   # runs, then comes back here
        elif attack_ready():
            print("attack")
            AttackSequence()                  # runs, then comes back here
        wait(0.05)


# ---------- start / stop ----------

def main():
    try:
        PhaseCheck()
    except Exception as e:
        print("crashed:", e)
    print("stopped")

def StartExitFunction(k):
    global main_thread
    if k == keyboard.Key.f8:
        if main_thread is None or not main_thread.is_alive():
            print("ON")
            stop.clear()
            main_thread = threading.Thread(target=main, daemon=True)
            main_thread.start()
        else:
            print("OFF")
            stop.set()
    elif k == keyboard.Key.esc:
        print("Exiting")
        os._exit(0)

with keyboard.Listener(on_press=StartExitFunction) as listener:
    print("F8 = start/stop, Esc = exit")
    listener.join()
import windowController
import pyautogui
import win32gui
import time, ctypes, sys


hwnd = windowController.switchWindow()
windowRect = win32gui.GetWindowRect(hwnd)

print("Window Rectangle:", windowRect)

pyautogui.hotkey('esc')

windowController.captureWindow(hwnd)
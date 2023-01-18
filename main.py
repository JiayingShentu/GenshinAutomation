import windowController
import logics
import pyautogui
import time

# Default window size: 1024 * 768

hwnd = windowController.switchWindow()
rolenum=logics.configureTeam(hwnd)
time.sleep(2)
print("press esc")
pyautogui.press('esc')
print("press rolenum")
time.sleep(3)
pyautogui.press(str(rolenum))

logics.exploreDispatch(hwnd)




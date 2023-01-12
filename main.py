import windowController
import logics
import pyautogui

# Default window size: 1024 * 768

hwnd = windowController.switchWindow()
logics.configureTeam(hwnd)

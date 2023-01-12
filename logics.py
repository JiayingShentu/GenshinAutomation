import windowController
import cvMatcher
import pyautogui
import time
import win32gui

def configureTeam(hwnd):
    for retryTimes in range(2):
        pyautogui.hotkey('esc')
        time.sleep(1)
        capture = windowController.captureWindow(hwnd)
        matchRect = cvMatcher.match("Resources/TeamConfig.png", capture)
        print("configure team:", ("fail" if matchRect == None else "success") + ",", "tried", retryTimes, "time(s)")
        if matchRect != None:
            break 

    if matchRect == None:
        print("configure team: give up")
        return None

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    pyautogui.click(left + matchRect[0], top + matchRect[1], duration=0.5)
    print("configure team: clicked")
    time.sleep(5)

    capture = windowController.captureWindow(hwnd)
    matchRect = cvMatcher.match("Resources/BodyAmber.png", capture)
    if matchRect != None:
        position=int(matchRect[0]/(width/4))+1
        print("Amber is already in team.","position:",position)
        return position
    
    pyautogui.click(left+width/5,top+height/2,duration=0.5)
    print("role 1: clicked")
    time.sleep(1)
    for retryTimes in range(3):
        capture = windowController.captureWindow(hwnd)
        matchRect = cvMatcher.match("Resources/RoleAmber.png", capture)
        if matchRect == None:
            print("select Amber: fail, tried",retryTimes,"time(s)")
            pyautogui.moveTo(left+width/5,top+height*5/6,duration=0.5)
            pyautogui.dragTo(left+width/5,top+height/6,duration=0.5)
        else:
            print("select Amber: success, tried",retryTimes,"time(s)")
            break 
    if matchRect == None:
        print("configure team: give up")
        return None
    pyautogui.click(left+matchRect[0],top+matchRect[1],duration=0.5)
    print("role Amber: clicked")

    capture=windowController.captureWindow(hwnd)
    matchRect=cvMatcher.match("Resources/RoleChange.png",capture)
    if matchRect == None:
        print("configure team: give up")
        return None
    pyautogui.click(left+matchRect[0],top+matchRect[1],duration=0.5)
    return 1



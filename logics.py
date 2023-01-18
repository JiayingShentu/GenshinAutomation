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

def exploreDispatch(hwnd):
    print("press M")
    time.sleep(1)
    pyautogui.press("M")
    time.sleep(3)
    capture = windowController.captureWindow(hwnd)
    matchRect = cvMatcher.match("Resources/ExploreDispatch_Map.png", capture)
    print("find Name ExploreDispatch:", ("fail" if matchRect == None else "success"))
     
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    pyautogui.click(left + matchRect[0], top + matchRect[1], duration=0.5)
    print("explore dispatch: clicked")

    time.sleep(1)
    capture = windowController.captureWindow(hwnd)
    
    nation_name=findNationName(capture)
    if nation_name==None:
        print("find nation name: give up")
        return None

    pyautogui.click(left + width*9/10,top + height*15/16,duration=0.5)
    print("transferTo"+nation_name+": clicked")
    return

def findNationName(capture):
    nations=["Monde","Liyue","Daoqi","Xumi"]
    for nation in nations:
        matchRect = cvMatcher.match("Resources/transferTo"+nation+".png", capture)
        if matchRect != None:
            return nation
        print("find transferTo"+nation+":", ("fail" if matchRect == None else "success"))
    return None

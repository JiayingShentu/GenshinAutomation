import win32con
import win32gui, win32ui
import numpy
import cv2

def switchWindow():
    hwnd = win32gui.FindWindow(None, u'原神')

    print("Handler of window:", hwnd)

    assert(hwnd != 0)

    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.SetForegroundWindow(hwnd)
    return hwnd

def captureWindow(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitmap = win32ui.CreateBitmap()
    saveBitmap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitmap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    capture = numpy.frombuffer(saveBitmap.GetBitmapBits(True), dtype='uint8')
    capture.shape = (height, width, 4)
    cv2.cvtColor(capture, cv2.COLOR_BGRA2RGB)
    cv2.imshow('Capture', capture)
    cv2.waitKey(0)
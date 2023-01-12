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
    hwndDC = win32gui.GetWindowDC(hwnd)                                 #返回句柄窗口的设备环境，覆盖整个窗口
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)                          #创建设备描述表
    saveDC = mfcDC.CreateCompatibleDC()                                 #创建内存设备描述表
    saveBitmap = win32ui.CreateBitmap()                                 #创建位图对象准备保存图片
    saveBitmap.CreateCompatibleBitmap(mfcDC, width, height)             #为bitmap开辟存储空间
    saveDC.SelectObject(saveBitmap)                                     #将截图保存到saveBitMap中
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)#保存bitmap到内存设备描述表
    capture = numpy.frombuffer(saveBitmap.GetBitmapBits(True), dtype='uint8')
    capture.shape = (height, width, 4)
    cv2.cvtColor(capture, cv2.COLOR_BGRA2RGB)
    cv2.imshow('Capture', capture)
    cv2.waitKey(0)
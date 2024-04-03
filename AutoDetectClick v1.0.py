import cv2
import numpy as np
import pyautogui
import time
import threading
import keyboard
import win32gui
import psutil
import win32process
import os

running = True
current_directory = os.path.dirname(__file__) 

def find_and_click(image_path, screenshot):
    # 读取模板图像
    template_rgb = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)

    # imdecode读取的是rgb，opencv处理需要转换成bgr
    template = cv2.cvtColor(template_rgb, cv2.COLOR_RGB2BGR)

    # 使用模板匹配方法
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    # 设置阈值
    threshold = 0.8
    loc = np.where(res >= threshold)
    
    # 如果找到匹配位置，模拟点击
    if len(loc[0]) > 0:
        # 取第一个匹配位置的中心点坐标
        target_x = int(loc[1][0] + template.shape[1] / 2)
        target_y = int(loc[0][0] + template.shape[0] / 2)
        #time.sleep(0.5) #设置延时
        pyautogui.click(target_x, target_y)
        return True
    return False

def get_active_window_process_name():
    hwnd = win32gui.GetForegroundWindow()
    pid = win32process.GetWindowThreadProcessId(hwnd)
    process = psutil.Process(pid[-1])
    return process.name()

def is_QQ():
    process_name = get_active_window_process_name()
    if process_name == "QQ.exe":
        return True
    return False

def run():
    global running
    global current_directory
    while running:
        try:
            if is_QQ():
                #print("窗口是QQ，开始搜索。")
                screenshot = pyautogui.screenshot()
                screenshot = np.array(screenshot)
                image_path = os.path.join(current_directory, 'source', 'toggle.jpg')
                if find_and_click(image_path, screenshot):
                    print("找到相似图像，已点击。")
        except Exception as e:
            print("发生异常:", e)
        time.sleep(1)

def on_key_press():
    global running
    print("按下F12键终止程序...")
    keyboard.wait('F12')
    print("程序已结束。")
    running = False  # 将running设置为False以退出主循环

if __name__ == "__main__":
    # 创建一个线程来监听键盘输入
    key_thread = threading.Thread(target=on_key_press)
    key_thread.start()

    run()

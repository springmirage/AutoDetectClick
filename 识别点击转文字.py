import cv2
import numpy as np
import pyautogui
import time
import threading
import keyboard

def find_and_click(image_path, screenshot):
    # 读取模板图像
    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

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
        pyautogui.click(target_x, target_y)
        return True
    return False

def run():
    while True:
        try:
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
            image_path = r'D:\toggle.jpg'
            if find_and_click(image_path, screenshot):
                print("找到相似图像，已点击。")
        except Exception as e:
            print("发生异常:", e)
        time.sleep(1)

def on_key_press():
    print("按下F12键终止程序...")
    keyboard.wait('F12')

if __name__ == "__main__":
    # 创建一个线程来监听键盘输入
    key_thread = threading.Thread(target=on_key_press)
    key_thread.start()
    
    run()

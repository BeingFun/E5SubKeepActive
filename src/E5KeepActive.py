import os.path
import random
import threading
import time
from datetime import datetime, timedelta
from authorization import Authorization
import authorization
from flask import Flask, request

from src.constants.constants import ROOT_PATH
from src.drive import OneDrive, threshold_size
from src.startwithsys import WithSysInit
from src.util.config_init import ConfigInit

app = Flask(__name__)
lock = threading.Lock()


# 定义用于接收重定向的路由
@app.route('/GetAuthorizationCode', methods=['GET'])
def receive_redirect():
    # 获取重定向中的参数
    code = request.args.get('code')
    # 使用锁确保线程安全
    with lock:
        # 在这里可以处理收到的参数
        if code is not None:
            authorization.authorization_code = code
        time.sleep(5)
    # 返回响应
    return "已经正常接收到应用授权码，现在你可以关闭浏览器窗口了"


def call_onedrive_api():
    print("start call onedrive api...")
    # 获取根目录
    if not OneDrive.check_exist_item(item_id="root", filename="E5KeepActive"):
        OneDrive.create_folder("root", "E5KeepActive")
    # get E5KeepActive id
    folder_id = OneDrive.get_item_id("E5KeepActive")
    if not OneDrive.check_exist_item(item_id=folder_id, filename="E5KeepActive.log"):
        OneDrive.create_file("root:/E5KeepActive", "E5KeepActive.log")
    # get content
    log_id = OneDrive.get_item_id("E5KeepActive/E5KeepActive.log")
    if OneDrive.get_item_size(log_id) >= threshold_size:
        OneDrive.delete_item(log_id)
    original_content = OneDrive.get_content(item_path="E5KeepActive/E5KeepActive.log")
    # 更新时间间隔 (单位:秒)
    period_min = int(ConfigInit.config_init().base_setting.call_func_period[0]) * 60
    period_max = int(ConfigInit.config_init().base_setting.call_func_period[1]) * 60
    period = random.randint(period_min, period_max)
    file_head = "This is E5KeepActive App detailed running time(the next to run about at {} {}):\n".format(
        datetime.now().strftime("%Y:%m:%d"),
        (datetime.now() + timedelta(seconds=period)).strftime("%H:%M:%S"),
    )
    if original_content == "":
        new_content = "\tE5KeepActive App last run at {} {}\n".format(
            datetime.now().strftime("%Y:%m:%d"),
            datetime.now().strftime("%H:%M:%S"),

        )
        content = file_head + new_content
    else:
        new_content = "\tE5KeepActive App last run at {} {}\n".format(
            datetime.now().strftime("%Y:%m:%d"),
            datetime.now().strftime("%H:%M:%S"),
        )
        original_str_list = original_content.split("\n")
        content = file_head + new_content + "\n".join(original_str_list[1:])

    # local log
    log_folder = ROOT_PATH + r"\logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_path = ROOT_PATH + r"\logs\log.log"
    if not os.path.exists(log_path):
        with open(log_path, "w"):
            pass
    with open(log_path, "w") as file:
        file.write(content)
    # 控制台输出
    # print(content)

    OneDrive.update_file(item_id=log_id, content=content)
    print("finish call onedrive api at one time...")
    time.sleep(period)


# 定义一个线程函数，用于执行onedrive api
def call_onedrive_thread():
    while True:
        print("*" * 20 + " start call onedrive thread " + "*" * 20)
        # step 1 授权令牌初始化
        Authorization.init()
        # step 2 开机启动初始化
        WithSysInit.init()
        # step 3 执行 onedrive 的相关API操作
        call_onedrive_api()


if __name__ == '__main__':
    # 启动 Flask 线程,用于接收 authorization_code
    flask_thread = threading.Thread(target=app.run, kwargs={'port': 2233}, name="flask_thread")
    flask_thread.start()

    # 启动 onedrive api 调用线程
    call_onedrive_thread = threading.Thread(target=call_onedrive_thread, name="call_onedrive_thread")
    call_onedrive_thread.start()

    # 等待 call_onedrive_thread 线程结束
    call_onedrive_thread.join()

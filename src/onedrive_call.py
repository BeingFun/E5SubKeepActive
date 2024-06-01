import os
import time
from datetime import datetime, timedelta

from src.authorization import Authorization
from src.constants.constants import Constants
from src.startwithsys import WithSysInit
from src.util.config_init import ConfigInit
from src.drive import OneDrive


def call_onedrive_api():
    print("start call onedrive api...")
    # 创建文件 root:Apps/E5KeepActive/E5KeepActive.log
    OneDrive.create_folder("root", "Apps")
    OneDrive.create_folder("root:/Apps", "E5KeepActive")
    OneDrive.create_file("root:/Apps/E5KeepActive", "E5KeepActive.log")

    # get content
    log_id = OneDrive.get_item_id("root:/Apps/E5KeepActive/E5KeepActive.log")
    if OneDrive.get_item_size(log_id) >= ConfigInit.config_init().base_setting.log_size:
        OneDrive.delete_item(log_id)

    original_content = OneDrive.get_content(item_id=log_id)

    # 更新时间间隔 (单位:秒)
    period = ConfigInit.config_init().base_setting.call_func_period

    file_head = "E5KeepActive App's detailed runtime record(the next to run about at {} {}):\n".format(
        datetime.now().strftime("%Y-%M-%d"),
        (datetime.now() + timedelta(seconds=period)).strftime("%H:%M"),
    )

    if original_content == "":
        new_content = "\tE5KeepActive App last run at {} {}\n".format(
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%H:%M:%S"),

        )
        content = file_head + new_content
    else:
        new_content = "\tE5KeepActive App last run at {} {}\n".format(
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%H:%M:%S"),
        )
        original_str_list = original_content.split("\n")
        content = file_head + new_content + "\n".join(original_str_list[1:])

    # local log
    log_path = Constants.get_value("root_path") + r"\E5KeepActive.log"
    # 创建文件
    if not os.path.exists(log_path):
        with open(log_path, "w"):
            pass
    # 写入日志
    with open(log_path, "w") as file:
        file.write(content)
    # 控制台输出
    # print(f"info log_content: {content}")

    OneDrive.update_file(item_id=log_id, content=content)
    print("finish call onedrive api at one time...")


def call_onedrive_thread():
    print("*" * 20 + " start call onedrive thread " + "*" * 20)
    while True:
        # step 1 授权令牌初始化
        Authorization.init()
        # step 2 开机启动初始化
        WithSysInit.init()
        # step 3 执行 onedrive 的相关API操作
        period = ConfigInit.config_init().base_setting.call_func_period
        call_onedrive_api()
        time.sleep(period)

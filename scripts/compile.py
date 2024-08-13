import sys
import os
from PyInstaller.__main__ import run

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants.constants import Constants
from src.util.file_tools import FileTools

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
VERSION = "release"

if __name__ == "__main__":
    Constants.global_init()
    program_path = Constants.get_value("root_path") + r"\src\main.py"
    performable_path = Constants.get_value("root_path") + r"\bin"
    icon_file_path = Constants.get_value("root_path") + r"\resources\ico\E5KeepActive.ico"
    work_path = CUR_PATH + r"\E5KeepActive_build"

    # 设置编译参数和选项
    options = [
        "--onefile",  # 打包成单个可执行文件
        # "--onedir",  # 生成一个包含可执行文件的目录
        # '--noconsole',  # 不显示控制台窗口
        "--clean",  # 清理临时文件
        "--name={}".format("E5KeepActive"),  # 指定生成的可执行文件名称
        "--distpath={}".format(performable_path),  # 指定生成的可执行文件路径
        "--icon={}".format(icon_file_path),  # 指定生成的可执行文件图标
        "--specpath={}".format(CUR_PATH),  # 指定 .spec 文件的输出路径
        "--workpath={}".format(work_path),  # 指定build 文件夹路径
        # "--hidden-import={}".format("msgraph"),  # 强制将模块包含在可执行文件中
        # "--hidden-import={}".format("azure.identity"),
        "--paths={}".format(
            "D:\\Programs\\Python\\Python310\\Lib\\site-packages"
        ),  # 用于搜索导入的路径
    ]

    if "release" == VERSION:
        options.append("--noconsole")  # 不显示控制台窗口

    print(options)
    # 运行 PyInstaller
    try:
        run(
            [
                str(program_path),
                *options,
            ]
        )
        FileTools.clear_file(work_path)
    except Exception as e:
        print(e)
        sys.exit(1)

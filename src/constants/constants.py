import os
import sys

# 是否为可执行程序
FROZEN = getattr(sys, "frozen", False)

# 获取当前文件所在目录的路径
if FROZEN:
    # 如果是可执行文件，则用 compass 获取可执行文件的目录
    _CUR_PATH = os.path.dirname(os.path.abspath(sys.executable))
else:
    # 否则，从 __file__ 中获取当前文件的路径，并取其所在目录作为当前目录
    _CUR_PATH = os.path.dirname(os.path.abspath(__file__))
    _CUR_PATH = os.path.dirname(_CUR_PATH)

# 根目录
ROOT_PATH = os.path.dirname(_CUR_PATH)

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.authorization import Authorization
from src.onedrive_call import call_onedrive_api

# step 1 授权令牌初始化
print("*" * 20 + " step 1 授权令牌初始化 " + "*" * 20)
Authorization.init()
# step 2 执行 onedrive 的相关API操作
print("*" * 20 + " step 2 执行 onedrive 的相关API操作 " + "*" * 20)
print("start call onedrive api...")
call_onedrive_api()
print("finish call onedrive api...")

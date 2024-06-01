from src.authorization import Authorization
from src.onedrive_call import call_onedrive_api
from src.util.config_init import ConfigInit

# step 1 授权令牌初始化
print("*" * 20 + "step 1 授权令牌初始化" + "*" * 20)
Authorization.init()
# step 2 执行 onedrive 的相关API操作
print("*" * 20 + "step 2 执行 onedrive 的相关API操作" + "*" * 20)
period = ConfigInit.config_init().base_setting.call_func_period
call_onedrive_api()

import json
import threading
import time
from flask import Flask, request

from src.constants.constants import Constants

# Flask 类实例化
local_serve = Flask(__name__)
# 配置服务地址和端口
Constants.global_init()
local_serve.config.from_file(Constants.get_value("root_path") +
                             r"/config/server_config.json",
                             load=json.load)
print(f"info: {local_serve.config}")


# 使用路由装饰器定义接收重定向的路由函数
@local_serve.route('/GetAuthorizationCode', methods=['GET'])
def receive_redirect():
  # 获取重定向中的参数
  code = request.args.get('code')
  while True:
    lock = threading.Lock()
    with lock:
      # 在这里可以处理收到的参数
      if code is not None:
        Constants.set_value("authorization_code", code)
        # 返回响应
        return "已经正常接收到应用授权码，现在你可以关闭浏览器窗口了"
    time.sleep(5)

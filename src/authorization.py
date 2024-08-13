import os
import time
import webbrowser
import requests
import json

from src.constants.constants import Constants
from src.server import local_serve
from src.util.config_init import ConfigInit

# 重定向url, 在 Microsoft Entra 添加的web平台重定向uri
redirect_uri = "http://{}/GetAuthorizationCode".format(local_serve.config["SERVER_NAME"])

# 使用默认值即可
response_type = "code"
response_mode = "query"
scopes = ["Files.ReadWrite.All", "offline_access"]

# endpoints
endpoints = "https://login.microsoftonline.com"
# 多租户 或 个人账号令牌节点
access_token_url = f"{endpoints}/common/oauth2/v2.0/token?"
# 多租户或个人账号鉴权节点
access_authorize_url = f"{endpoints}/common/oauth2/v2.0/authorize?"


class Authorization:
    @staticmethod
    def get_scope() -> str:
        global scopes
        scope = ""
        for item in scopes:
            scope = item + "+" + scope
        return scope[:-1]

    @staticmethod
    def init():
        print("start authorization init...")
        config = ConfigInit.config_init()
        ENV_TOKEN = None
        try:
            ENV_TOKEN = json.loads(os.environ.get("TOKEN"))
        except Exception as e:
            pass
        token = ENV_TOKEN or ConfigInit.load_token()
        Constants.set_value("token", token)
        # 如果刷新令牌为空，则重新登录获取令牌
        if token is None:
            # step 1.1 获取授权代码
            print("get authorization code...")
            authorization_url = f"{access_authorize_url}" \
                                f"&client_id={config.user_setting.client_id}" \
                                f"&response_type={response_type}" \
                                f"&scope={Authorization.get_scope()}" \
                                f"&redirect_uri={redirect_uri}" \
                                f"&response_mode={response_mode}"
            print(authorization_url)
            webbrowser.open_new(authorization_url)

            while True:
                authorization_code = Constants.get_value("authorization_code")
                if authorization_code is not None:
                    break
                time.sleep(1)
            # step 1.2 用授权代码获取访问令牌
            print("get access token...")
            authorization_code_body = {
                "client_id": config.user_setting.client_id,
                "grant_type": "authorization_code",
                "scope": scopes[0],
                "code": authorization_code,
                "redirect_uri": redirect_uri,
                "client_secret": config.user_setting.client_secret,
            }
            token = requests.post(access_token_url, data=authorization_code_body, proxies={}).json()
            token["expires_time"] = time.time() + token["expires_in"] - 20
            Constants.set_value("token", token)
            ConfigInit.dump_token(token)

        # 已有token但已经过期,通过refresh_token换取新的令牌
        if time.time() > token["expires_time"]:
            print("renew access token...")
            Authorization.renew_token()
        print("finish authorization init...")

    @staticmethod
    def renew_token():
        token = Constants.get_value("token")
        config = ConfigInit.config_init()
        refresh_token_body = {
            "client_id": config.user_setting.client_id,
            "grant_type": "refresh_token",
            "refresh_token": token["refresh_token"],
            "client_secret": config.user_setting.client_secret,
        }
        new_token = requests.post(access_token_url, data=refresh_token_body, proxies={}).json()
        new_token["expires_time"] = time.time() + new_token["expires_in"] - 20
        Constants.set_value("token", new_token)
        ConfigInit.dump_token(new_token)
        return new_token

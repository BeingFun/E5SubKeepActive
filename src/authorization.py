import time
import webbrowser

import requests

from src.util.config_init import ConfigInit

# 重定向url, 在 Microsoft Entra 添加的web平台重定向uri
redirect_uri = "http://localhost:2233/GetAuthorizationCode"

# 使用默认值即可
response_type = "code"
response_mode = "query"
scopes = ["offline_access", "Files.Read", "Files.Read.All",
          "Files.ReadWrite", "Files.ReadWrite.All",
          "Sites.Read.All", "Sites.ReadWrite.All"]

# 微软账号授权代码
authorization_code = None
# 多租户或个人账号令牌根节点
access_token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token?"
# 多租户或个人账号鉴权根节点
access_authorize_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?"
# 授权令牌
token = None


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
        global authorization_code
        global token
        config = ConfigInit.config_init()
        token = ConfigInit.load_token()
        # 如果刷新令牌为空，则重新登录获取令牌
        if token is None:
            # step 1.1 获取授权代码
            print("get authorization code...")
            authorization_url = f"{access_authorize_url}" \
                                f"&client_id={config.user_setting.client_id}" \
                                f"&response_type={response_type}" \
                                f"&scope={Authorization.get_scope()}" \
                                f"&response_mode={response_mode}" \
                                f"&redirect_uri={redirect_uri}"
            print(authorization_url)
            webbrowser.open_new(authorization_url)
            while True:
                if authorization_code is not None:
                    break
                time.sleep(5)
            # step 1.2 用授权代码获取访问令牌
            print("get access token...")
            global scopes
            authorization_code_body = {
                "tenant": config.user_setting.tenant_id,
                "client_id": config.user_setting.client_id,
                "grant_type": "authorization_code",
                "scope": scopes,
                "code": authorization_code,
                "redirect_uri": redirect_uri,
                "client_secret": config.user_setting.client_secret,
            }
            token = requests.post(access_token_url, data=authorization_code_body).json()
            token["expires_time"] = time.time() + token["expires_in"] - 20
            ConfigInit.dump_token(token)

        # 已有token但已经过期,通过refresh_token换取新的令牌
        if time.time() > token["expires_time"]:
            print("renew access token...")
            token = Authorization.renew_token()
            ConfigInit.dump_token(token)
        print("finish authorization init...")

    @staticmethod
    def renew_token():
        global token
        config = ConfigInit.config_init()
        refresh_token_body = {
            "tenant": config.user_setting.tenant_id,
            "client_id": config.user_setting.client_id,
            "grant_type": "refresh_token",
            "refresh_token": token["refresh_token"],
            "client_secret": config.user_setting.client_secret,
        }
        token = requests.post(access_token_url, data=refresh_token_body).json()
        token["expires_time"] = time.time() + token["expires_in"] - 20
        return token

# 用户配置信息
import json
import time

import requests

from src.authorization import Authorization

import authorization
from src.util.config_init import ConfigInit

# OneDrive 当前登录用户根节点
onedrive_root = "https://graph.microsoft.com/v1.0/me/drive"
# up method only supports files up to 250 MB in size.
threshold_size = 245


class OneDrive:
    # 根据 refresh_token 获取 access_token
    @staticmethod
    def get_header():
        if time.time() > authorization.token["expires_time"]:
            token = Authorization.renew_token()
            ConfigInit.dump_token(token)
        header = {
            "Authorization": "bearer " + authorization.token["access_token"]
        }
        return header

    @staticmethod
    def get_item_id(item_path: str):
        url = onedrive_root + f"/root:/{item_path}"
        response = requests.get(url=url, headers=OneDrive.get_header()).json()
        return response["id"]

    @staticmethod
    def check_exist_item(item_id: str, filename: str) -> bool:
        url = onedrive_root + f"/items/{item_id}/children"
        response = requests.get(url=url, headers=OneDrive.get_header()).json()
        for item in response["value"]:
            if filename == item["name"]:
                return True
        return False

    @staticmethod
    def create_folder(item_path: str, foldername: str) -> bool:
        data = json.dumps(
            {
                "name": foldername,
                "folder": {},
                "@microsoft.graph.conflictBehavior": "rename"
            }
        )
        header = OneDrive.get_header()
        header["Content-Type"] = "application/json"
        url = onedrive_root + f"/{item_path}/children"
        response = requests.post(url=url, headers=header, data=data)
        return response.ok

    @staticmethod
    def create_file(item_path: str, filename: str) -> bool:
        data = b""
        header = OneDrive.get_header()
        header["Content-Type"] = "text/plain"
        url = onedrive_root + f"/{item_path}/{filename}:/content"
        response = requests.put(url=url, headers=header, data=data)
        return response.ok

    @staticmethod
    def get_content(item_path: str):
        url = onedrive_root + f"/root:/{item_path}:/content"
        response = requests.get(url=url, headers=OneDrive.get_header())
        return response.text

    @staticmethod
    def update_file(item_id: str, content: str):
        url = onedrive_root + f"/items/{item_id}/content"
        data = content.encode("utf-8")
        header = OneDrive.get_header()
        header["Content-Type"] = "text/plain"
        response = requests.put(url=url, headers=header, data=data)
        return response.ok

    @staticmethod
    def get_item_size(item_id: str) -> int:
        """

        :param item_id: DriveItem id
        :return: file size (MB)
        """
        url = onedrive_root + f"/items/{item_id}"
        response = requests.get(url=url, headers=OneDrive.get_header()).json()
        return response["size"] / 1024 / 1024

    @staticmethod
    def delete_item(item_id: str) -> bool:
        """

        :param item_id:
        :return: False or True
        """
        url = onedrive_root + f"/items/{item_id}"
        response = requests.delete(url=url, headers=OneDrive.get_header())
        return response.ok

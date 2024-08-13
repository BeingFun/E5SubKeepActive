import json
import time
import requests

from src.authorization import Authorization
from src.constants.constants import Constants

# OneDrive 当前登录用户根节点
onedrive_root = "https://graph.microsoft.com/v1.0/me/drive"


class OneDrive:
    # 根据 refresh_token 获取 access_token
    @staticmethod
    def get_header():
        if time.time() > Constants.get_value("token")["expires_time"]:
            Authorization.renew_token()
        header = {
            "Authorization": "bearer " + Constants.get_value("token")["access_token"]
        }
        return header

    @staticmethod
    def get_item_id(item_path: str):
        """
        feature: 通过文件/文件夹路径获取到 item_id
        :param item_path: 文件夹或文件的绝对路径
        :return: 文件夹或文件的 item_id
        """
        url = onedrive_root + f"/{item_path}"
        response = requests.get(url=url, headers=OneDrive.get_header(), proxies={"http": None, "https": None}).json()
        return response["id"]

    @staticmethod
    def check_exist_item(item_path: str, filename: str) -> bool:
        """
        使用父级文件夹的路径,检索父级文件夹下是否存在 待检索的文件或文件夹
        :param item_path: 父级文件夹的绝对路径
        :param filename: 待检索的文件或文件夹名
        :return:
        """
        item_id = OneDrive.get_item_id(item_path=item_path)
        url = onedrive_root + f"/items/{item_id}/children"
        response = requests.get(url=url, headers=OneDrive.get_header(), proxies={"http": None, "https": None}).json()
        for item in response["value"]:
            if filename == item["name"]:
                return True
        return False

    @staticmethod
    def create_folder(item_path: str, foldername: str):
        """
        feature: 在父级目录 item_path 下创建文件夹 foldername
        :param item_path: 待创建文件夹的父级绝对路径
        :param foldername: 创建文件夹的名称
        :return:
        """
        if not OneDrive.check_exist_item(item_path=item_path, filename=foldername):
            data = json.dumps(
                {
                    "name": foldername,
                    "folder": {},
                    "@microsoft.graph.conflictBehavior": "rename"
                }
            )
            header = OneDrive.get_header()
            header["Content-Type"] = "application/json"
            parent_id = OneDrive.get_item_id(item_path)
            url = onedrive_root + f"/items/{parent_id}/children"
            response = requests.post(url=url, headers=header, data=data, proxies={"http": None, "https": None})
            return response.ok
        print(f"info: the folder {foldername} already exist in the {item_path}")

    @staticmethod
    def create_file(item_path: str, filename: str) -> bool:
        """
        feature: 在父级文件夹路径下创建文件
        :param item_path: 父级文件夹绝对路径
        :param filename: 文件名
        :return:
        """
        if not OneDrive.check_exist_item(item_path=item_path, filename=filename):
            data = b""
            header = OneDrive.get_header()
            header["Content-Type"] = "text/plain"
            parent_id = OneDrive.get_item_id(item_path)
            url = onedrive_root + f"/items/{parent_id}:/{filename}:/content"
            response = requests.put(url=url, headers=header, data=data, proxies={"http": None, "https": None})
            return response.ok
        print(f"info: the file {filename} already exist in the {item_path}")

    @staticmethod
    def get_content(item_id: str):
        """
        feature: 使用 item_id 获取 DriveItem 的内容
        :param item_id: DriveItem id
        :return: file content
        """
        url = onedrive_root + f"/items/{item_id}/content"
        response = requests.get(url=url, headers=OneDrive.get_header(), proxies={"http": None, "https": None})
        return response.text

    @staticmethod
    def update_file(item_id: str, content: str):
        """
        feature: 使用 item_id 更新 DriveItem 的内容
        :param item_id: DriveItem id
        :param content: 待上传的内容
        :return:
        """
        url = onedrive_root + f"/items/{item_id}/content"
        data = content.encode("utf-8")
        header = OneDrive.get_header()
        header["Content-Type"] = "text/plain"
        response = requests.put(url=url, headers=header, data=data, proxies={"http": None, "https": None})
        return response.ok

    @staticmethod
    def get_item_size(item_id: str) -> int:
        """
        feature: 获取 DriveItem 的文件大小
        :param item_id: DriveItem id
        :return: file size (MB)
        """
        url = onedrive_root + f"/items/{item_id}"
        response = requests.get(url=url, headers=OneDrive.get_header(), proxies={"http": None, "https": None}).json()
        return response["size"] / 1024 / 1024

    @staticmethod
    def delete_item(item_id: str) -> bool:
        """
        feature: use item_id 删除 DriveItem
        :param item_id:
        :return: False or True
        """
        url = onedrive_root + f"/items/{item_id}"
        response = requests.delete(url=url, headers=OneDrive.get_header(), proxies={"http": None, "https": None})
        return response.ok

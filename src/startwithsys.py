# import winreg
import sys

if sys.platform == 'win32':
  import _winreg
elif sys.platform == 'cygwin':
  import cygwinreg as _winreg

from src.constants.constants import Constants
from src.util.config_init import ConfigInit

program_name = "E5KeepActive"
program_path = Constants.get_value("root_path") + r"\bin\E5KeepActive.exe"
program_para = "-hidden"
value = ConfigInit.config_init().base_setting.start_with_sys


class WithSysInit:

  @staticmethod
  def init():
    """
        设置开机自启

        Parameters:
        - program_name: 注册表中程序的名称，建议用程序名填入
        - program_path: 启动的程序路径，若有启动参数填入
        - program_para: 启动程序的参数，可选
        - value: 是否开机自启

        Returns:
        - None
        """
    print("start with sys init...")
    program = program_path + f" {program_para}"
    if value:
      try:
        WithSysInit.add_with_sys(program_name, program)
      except BaseException as e:
        print("开机自启设置失败")
        print(e)
      finally:
        print("finish with sys init...")
    else:
      try:
        WithSysInit.delete_with_sys(program_name)
      except BaseException as e:
        print("关闭开机自启设置失败")
        print(e)
      finally:
        print("finish with sys init...")

  # 设置要添加到注册表中的键值对
  @staticmethod
  def add_with_sys(value_name: str, value: str):
    """
        添加开机启动注册表值

        Parameters:
        - value_name: 程序名称
        - value: 启动程序路径及其参数

        Returns:
        - None
        """

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_ALL_ACCESS,
    )
    winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value)
    winreg.CloseKey(key)

  @staticmethod
  def delete_with_sys(value_name: str):
    """
        删除开机启动注册表值

        Parameters:
        - value_name: 程序名称

        Returns:
        - None
        """
    # 注册表键的句柄
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_ALL_ACCESS,
    )

    # 获取句柄下的值数量
    num_values = winreg.QueryInfoKey(key)[1]
    value_list = [
        item[0]
        for item in [winreg.EnumValue(key, i) for i in range(num_values)]
    ]
    if value_name in [value_list]:
      winreg.DeleteValue(key, value_name)

    winreg.CloseKey(key)

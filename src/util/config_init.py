import configparser
import json
import os.path
import random
import chardet

from src.constants.constants import Constants


class UserSetting:

  def __init__(self, client_id, client_secret):
    self.client_id = client_id
    self.client_secret = client_secret


class BasicSetting:

  def __init__(self, start_with_sys, call_func_period, log_size):
    self.start_with_sys = start_with_sys
    self.call_func_period = call_func_period
    self.log_size = log_size


class Setting:

  def __init__(self, base_setting: BasicSetting, user_setting: UserSetting):
    self.base_setting = base_setting
    self.user_setting = user_setting


class ConfigInit:

  @staticmethod
  def config_init() -> Setting:
    print("start config init...")
    # Read the configuration file information
    config = configparser.ConfigParser(allow_no_value=False)
    configfile = Constants.get_value("root_path") + r"/config/config.ini"
    with open(configfile, "rb") as file:
      content = file.read()
      encoding = chardet.detect(content)["encoding"]

    # Reopen the file using the detected encoding format and read the content
    with open(configfile, encoding=encoding) as file:
      config.read_file(file)

    dict_config = dict(config)

    start_with_sys = dict_config["BASIC_SETTING"].getboolean(
        "start_with_system")
    period_arr = (dict_config["BASIC_SETTING"].get("call_func_period").strip(
        "[]").replace(" ", "").split(","))
    period_min = int(period_arr[0]) * 60
    period_max = int(period_arr[1]) * 60
    call_func_period = random.randint(period_min, period_max)
    log_size = dict_config["BASIC_SETTING"].getint("log_size")

    base_setting = BasicSetting(start_with_sys=start_with_sys,
                                call_func_period=call_func_period,
                                log_size=log_size)

    client_id = dict_config["USER_SETTING"].get("client_id")
    client_secret = dict_config["USER_SETTING"].get("client_secret")

    user_setting = UserSetting(client_id=client_id,
                               client_secret=client_secret)

    setting = Setting(base_setting=base_setting, user_setting=user_setting)
    print("finish config init...")
    return setting

  @staticmethod
  def load_token():
    token_path = Constants.get_value("root_path") + "/config/token.json"
    if not os.path.exists(token_path):
      with open(token_path, "w"):
        pass
      print(f"Empty file '{token_path}' has been created.")
    if os.stat(token_path).st_size == 0:
      return None
    with open(token_path, "r") as file:
      token = json.load(file)
    return token

  @staticmethod
  def dump_token(token: json):
    token_path = Constants.get_value("root_path") + "/config/token.json"
    with open(token_path, "w") as file:
      json.dump(token, file)

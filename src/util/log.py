import os
from datetime import datetime

from src.constants.constants import Constants


class Log:
    @staticmethod
    def save_log(content: str = ""):
        file_path = Constants.ROOT_PATH + r"\Error.log"
        if not os.path.exists(file_path):
            with open(file_path, "x"):
                pass

        with open(file_path, "a") as file:
            time = "{} {}: \n".format(datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S"))
            exception = "\texception:\n\t\t" + content.split("split_symb")[0] + "\n"
            traceback = "\ttraceback:\n"
            traceback_lines = content.split("split_symb")[1].split("\n")
            for line in traceback_lines:
                traceback = traceback + "\t\t" + line + "\n"
            file.write(time + exception + traceback)

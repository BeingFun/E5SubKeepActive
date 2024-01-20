import os
from datetime import datetime


class Log:
    @staticmethod
    def save_log(file_path: str = r"../Error.log", content: str = ""):
        if not os.path.exists(file_path):
            with open(file_path, "w"):
                pass

        with open(file_path, "a") as file:
            time = "{} {}: \n".format(datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S"))
            exception = "\texception:\n\t\t" + content.split("split_symb")[0] + "\n"
            traceback = "\ttraceback:\n"
            traceback_lines = content.split("split_symb")[1].split("\n")
            for line in traceback_lines:
                traceback = traceback + "\t\t" + line + "\n"
            file.write(time + exception + traceback)

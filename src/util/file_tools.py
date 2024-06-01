import shutil
import os


class FileTools:
    # 安全删除文件
    @staticmethod
    def remove_s(file):
        if os.path.exists(file):
            os.remove(file)

    # 安全删除文件夹
    @staticmethod
    def rmdir_s(path):
        if not os.listdir(path):
            os.rmdir(path)
        else:
            shutil.rmtree(path)

    # 安全删除文件或文件夹
    @staticmethod
    def delete_file_or_folder(path):
        if os.path.exists(path):
            if os.path.isfile(path):
                # 如果是文件，则直接删除
                os.remove(path)
            elif os.path.isdir(path):
                FileTools.rmdir_s(path)

    # 安全创建文件
    @staticmethod
    def make_file_s(file):
        FileTools.remove_s(file)
        if not os.path.exists((os.path.dirname(file))):
            os.mkdir(os.path.dirname(file))
        open(file, "x").close()

    @staticmethod
    def clear_file(file_path: str):
        print(f"start clear {file_path}...")
        if os.path.exists(file_path):
            if not os.listdir(file_path):
                os.rmdir(file_path)
            else:
                shutil.rmtree(file_path)
        os.mkdir(file_path)
        print(f"finish clear {file_path}...")

    # def generate_file(self, basic_setting: BasicSetting):
    #     print("start generate file...")
    #     os.chdir(basic_setting.file_path)
    #     text = basic_setting.file_content
    #     text_size_bytes = len(text.encode("utf-8"))  # 每个重复的文本的大小（以字节为单位)
    #     # 需要分割为多少个文件
    #     file_num = basic_setting.file_size // 100  # 每个文件 100 MB
    #     file_remainder = basic_setting.file_size % 100  # 剩余文件的大小
    #
    #     # 日志
    #     with open("log.log", "w") as file:
    #         file.write(
    #             "# file time: {} {}\n".format(
    #                 datetime.datetime.now().strftime("%Y:%m:%d"),
    #                 datetime.datetime.now().strftime("%H:%M:%S"),
    #             )
    #         )
    #         file.write("# file size: {} MB\n".format(basic_setting.file_size))
    #
    #     for _ in range(file_num):
    #         repetitions = 1024 * 1024 * 100 // text_size_bytes  # 需要重复的次数
    #         remainder = 1024 * 1024 * 100 % text_size_bytes  # 剩余的字节数
    #         with open("tmp-{}.txt".format(uuid.uuid1()), "w") as file:
    #             for _ in range(repetitions):
    #                 file.write(text)
    #
    #             if remainder > 0:
    #                 file.write(text[:remainder])
    #
    #     if file_remainder > 0:
    #         repetitions = file_remainder * 1024 * 1024 // text_size_bytes  # 需要重复的次数
    #         remainder = file_remainder * 1024 * 1024 % text_size_bytes  # 剩余的字节数
    #         with open("tmp-{}.txt".format(uuid.uuid1()), "w") as file:
    #             for _ in range(repetitions):
    #                 file.write(text)
    #
    #             if remainder > 0:
    #                 file.write(text[:remainder])
    #     os.chdir(ROOT_PATH)
    #     print("finish generate file...")

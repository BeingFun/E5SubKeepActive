import os
import shutil
import sys
import zipfile

FROZEN = getattr(sys, "frozen", False)

# 获取当前文件所在目录的路径
if FROZEN:
    # 如果是可执行文件，则用 compass 获取可执行文件的目录
    _CUR_PATH = os.path.dirname(os.path.abspath(sys.executable))
else:
    # 否则，从 __file__ 中获取当前文件的路径，并取其所在目录作为当前目录
    _CUR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    print("#" * 60)
    print("start deploy...")
    # 创建 package_folder
    package_folder = "E5KeepActive"
    need_copy_folder = ['bin', 'config']
    need_copy_file = ['README.md', 'Changelog.md']

    # 切换到根目录
    os.chdir(_CUR_PATH)

    # 将bin、config文件夹中所有内容拷贝到 E5KeepActive 中
    for folder in need_copy_folder:
        src = os.path.join('.', folder)
        dst = os.path.join(package_folder, folder)
        shutil.copytree(src, dst)

    for file in need_copy_file:
        shutil.copy2(file, package_folder)

    # 将 Threewords 文件夹压缩为 Threewords.zip
    with zipfile.ZipFile(package_folder + '.zip', 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 遍历文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(package_folder):
            for file in files:
                # 构造文件的完整路径
                file_path = os.path.join(root, file)
                # 将文件添加到 ZIP 文件中
                zip_file.write(file_path)
                print("    add " + file_path + " to zip")

    # 打包完成之后清理文件夹
    shutil.rmtree(package_folder)
    print("finish deploy...")
    print("#" * 60)

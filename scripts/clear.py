import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.util.file_tools import FileTools

print("#" * 100)
print("Start clear...")

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(CUR_PATH)

build_path = CUR_PATH + r'\E5KeepActive_build'
spec_path = CUR_PATH + r'\E5KeepActive.spec'
bin_path = ROOT_PATH + r'\bin'
logs_path = ROOT_PATH + r'\Error.log'
run_logs_path = ROOT_PATH + r'\E5KeepActive.log'
token_path = ROOT_PATH + r'\config\token.json'
zip_path = ROOT_PATH + r'\E5KeepActive.zip'

files_list = [build_path, spec_path, bin_path, logs_path, run_logs_path, token_path, zip_path]

for path in files_list:
    FileTools.delete_file_or_folder(path)
    print(f"    removing {path}")

print("Finish clear...")
print("#" * 100)

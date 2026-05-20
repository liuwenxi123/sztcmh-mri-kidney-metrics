import os
import shutil

# 1级目录
def extract_mre1_files(source_dir, destination_dir):
    # 遍历源目录下的文件
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)

        # 检查是否是文件
        if os.path.isfile(file_path):
            # 检查文件名是否包含 "MRE1"
            if "MRE2" in file_name:
                # 构造目标文件路径
                destination_file = os.path.join(destination_dir, file_name)

                # 复制文件到目标文件路径
                shutil.copy(file_path, destination_file)

# 示例目录路径
source_directory = r"D:\508\zhongyiyuan\measure10M\measure\HV1-10\original"
destination_directory = r"D:\508\zhongyiyuan\measure10M\measure\HV1-10\original2"

# 提取含有 "MRE1" 的文件到目标目录
extract_mre1_files(source_directory, destination_directory)

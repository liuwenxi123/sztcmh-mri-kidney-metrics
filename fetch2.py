import os
import shutil

# 2级目录:label-23
def extract_cortex_files(source_dir, destination_dir):
    # 遍历源目录下的子文件夹
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)

        # 检查是否是文件夹
        if os.path.isdir(folder_path):
            # 遍历文件夹中的文件
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                print(file_path)
                # 检查文件名是否包含 "cortex"
                if "cortex" in file_name:
                    # 复制文件到目标目录
                    shutil.copy(file_path, destination_dir)

# 示例目录路径
source_directory = r"D:\508\zhongyiyuan\measure10M\measure\CKD23-36\lable"
destination_directory = r"D:\508\zhongyiyuan\measure10M\measure\CKD23-36\cortex"

# 提取含有 "cortex" 的文件到目标目录
extract_cortex_files(source_directory, destination_directory)

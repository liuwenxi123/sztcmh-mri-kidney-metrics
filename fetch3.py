import os
import shutil

# 3级目录：label-01-MRE1
def extract_cortex_files(source_dir, destination_dir):
    # 遍历源目录下的子文件夹
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)

        # 检查是否是文件夹
        if os.path.isdir(folder_path):
            # 查找子文件夹 MRE1
            mre1_folder = os.path.join(folder_path, 'label')

            # 检查 MRE1 文件夹是否存在
            if os.path.exists(mre1_folder) and os.path.isdir(mre1_folder):
                # 遍历 MRE1 文件夹中的文件
                for file_name in os.listdir(mre1_folder):
                    file_path = os.path.join(mre1_folder, file_name)

                    # 检查文件名是否包含 "cortex"
                    if "MRE_medulla" in file_name:
                        # 构造目标文件路径
                        destination_file = os.path.join(destination_dir, file_name)

                        # 复制文件到目标文件路径
                        shutil.copy(file_path, destination_file)

# 示例目录路径
source_directory = r"D:\508\zhongyiyuan\APP\37_57\37_57"
destination_directory = r"D:\508\zhongyiyuan\APP\37_57\medulla"

# 提取含有 "cortex" 的文件到目标目录
extract_cortex_files(source_directory, destination_directory)

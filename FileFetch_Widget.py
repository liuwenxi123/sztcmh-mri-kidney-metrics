import sys
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFrame,
                             QRadioButton, QGroupBox, QFileDialog, QMessageBox)

class FileFetch_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.source_folder = None

        source_title = QLabel('源路径:')
        self.source_path = QLabel(self)
        source_bt = QPushButton('Folder')
        source_bt.clicked.connect(self.open_source_folder)
        source_layout = QHBoxLayout()
        source_layout.addWidget(source_title)
        source_layout.addWidget(self.source_path)
        source_layout.addWidget(source_bt)

        save_title = QLabel('保存路径:')
        self.save_path = QLabel(self)
        save_bt = QPushButton('Folder')
        save_bt.clicked.connect(self.open_save_folder)
        save_layout = QHBoxLayout()
        save_layout.addWidget(save_title)
        save_layout.addWidget(self.save_path)
        save_layout.addWidget(save_bt)

        key1_title = QLabel('文件夹のkey：')
        self.key1_edit = QLineEdit()
        key1_layout = QHBoxLayout()
        key1_layout.addWidget(key1_title)
        key1_layout.addWidget(self.key1_edit)

        key2_title = QLabel('文件のkey：')
        self.key2_edit = QLineEdit()
        key2_layout = QHBoxLayout()
        key2_layout.addWidget(key2_title)
        key2_layout.addWidget(self.key2_edit)

        # key3_title = QLabel('关键字3')
        # self.key3_edit = QLineEdit()
        # key1_layout = QHBoxLayout()
        # key1_layout.addWidget(key1_title)
        # key1_layout.addWidget(self.key1_edit)

        key_layout = QHBoxLayout()
        key_layout.addLayout(key1_layout)
        key_layout.addLayout(key2_layout)

        self.type_bt1 = QRadioButton('直接抓取')
        self.type_bt2 = QRadioButton('1级抓取')
        self.type_bt3 = QRadioButton('2级抓取')
        self.type_bt1.setChecked(True)
        self.fetch_bt = QPushButton('抓取')
        self.fetch_bt.clicked.connect(self.extract_files_1)
        self.fetch_bt.clicked.connect(self.extract_files_2)
        self.fetch_bt.clicked.connect(self.extract_files_3)
        typebt_layout = QHBoxLayout()
        typebt_layout.addWidget(self.type_bt1)
        typebt_layout.addWidget(self.type_bt2)
        typebt_layout.addWidget(self.type_bt3)
        typebt_layout.addWidget(self.fetch_bt)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        fetch_layout = QVBoxLayout()
        folder_layout = QHBoxLayout()
        folder_layout.addLayout(source_layout)
        folder_layout.addLayout(save_layout)
        # fetch_layout.addLayout(source_layout)
        # fetch_layout.addLayout(save_layout)4
        fetch_layout.addLayout(folder_layout)
        fetch_layout.addLayout(key_layout)
        fetch_layout.addLayout(typebt_layout)

        fetch_groupbox = QGroupBox('文件抓取')
        fetch_groupbox.setLayout(fetch_layout)

        Fetchlayout = QVBoxLayout()
        Fetchlayout.addWidget(fetch_groupbox)
        Fetchlayout.addWidget(line)

        self.setLayout(Fetchlayout)

    def open_source_folder(self):
        """打开源文件文件夹"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.source_folder = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if self.source_folder:
            folder_name = os.path.basename(self.source_folder)
            parent_directory = os.path.basename(os.path.dirname(self.source_folder))
            display_path = os.path.join("…", parent_directory, folder_name)
            self.source_path.setText(display_path)

    def open_save_folder(self):
        """导入保存路径"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.save_folder = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

        if self.source_folder:
            folder_name = os.path.basename(self.save_folder)
            parent_directory = os.path.basename(os.path.dirname(self.save_folder))
            display_path = os.path.join("…", parent_directory, folder_name)
            self.save_path.setText(display_path)

    def extract_files_1(self):
        """直接抓取文件"""
        if not self.type_bt1.isChecked():
            return
        for file_name in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, file_name)
            # 检查是否是文件
            if os.path.isfile(file_path):
                # 检查文件名是否包含 "MRE1"
                if self.key2_edit.text() in file_name:
                    # 构造目标文件路径
                    destination_file = os.path.join(self.save_folder, file_name)
                    # 复制文件到目标文件路径
                    if os.path.isfile(file_path):
                        shutil.copy(file_path, destination_file)

        success_message = QMessageBox()
        success_message.setIcon(QMessageBox.Information)
        success_message.setWindowTitle('Success')
        success_message.setText('直接抓取完成')
        success_message.exec_()

    def extract_files_2(self):
        """1级抓取文件"""
        if not self.type_bt2.isChecked():
            return
        # 遍历源目录下的子文件夹
        for folder_name in os.listdir(self.source_folder):
            folder_path = os.path.join(self.source_folder, folder_name)

            # 检查是否是文件夹
            if os.path.isdir(folder_path):
                # 遍历文件夹中的文件
                for file_name in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file_name)
                    print(file_path)
                    # 检查文件名是否包含 "cortex"
                    if self.key2_edit.text() in file_name:
                        # 复制文件到目标目录
                        if os.path.isfile(file_path):
                            shutil.copy(file_path, self.save_folder)

        success_message = QMessageBox()
        success_message.setIcon(QMessageBox.Information)
        success_message.setWindowTitle('Success')
        success_message.setText('1级抓取完成')
        success_message.exec_()

    def extract_files_3(self):
        if not self.type_bt3.isChecked():
            return
        # 遍历源目录下的子文件夹
        for folder_name in os.listdir(self.source_folder):
            folder_path = os.path.join(self.source_folder, folder_name)

            # 检查是否是文件夹
            if os.path.isdir(folder_path):
                # 查找子文件夹 MRE1
                mre1_folder = os.path.join(folder_path, self.key1_edit.text())

                # 检查 MRE1 文件夹是否存在
                if os.path.exists(mre1_folder) and os.path.isdir(mre1_folder):
                    # 遍历 MRE1 文件夹中的文件
                    for file_name in os.listdir(mre1_folder):
                        file_path = os.path.join(mre1_folder, file_name)

                        # 检查文件名是否包含 "cortex"
                        if self.key2_edit.text() in file_name:
                            # 构造目标文件路径
                            destination_file = os.path.join(self.save_folder, file_name)
                            if os.path.isfile(file_path):
                                # 复制文件到目标文件路径
                                shutil.copy(file_path, destination_file)

        success_message = QMessageBox()
        success_message.setIcon(QMessageBox.Information)
        success_message.setWindowTitle('Success')
        success_message.setText('2级抓取完成')
        success_message.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = FileFetch_Widget()
    widget.show()
    sys.exit(app.exec_())
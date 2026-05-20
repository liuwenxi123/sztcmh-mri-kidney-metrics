import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFrame,
                             QRadioButton, QGroupBox, QFileDialog, QMessageBox, QSizePolicy)

class Rename_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.rename_folder = None
        """改名模块的布局"""
        rename_layout = QVBoxLayout()
        rename_groupbox = QGroupBox('批量改名')
        rename_groupbox.setLayout(rename_layout)
        rename_path_title = QLabel('待改名路径:')
        self.rename_path = QLabel(self)
        self.rename_path_bt = QPushButton('Folder')
        self.rename_path_bt.clicked.connect(self.open_rename_folder)
        self.rename_bt = QPushButton('执行改名')
        self.rename_bt.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.rename_bt.clicked.connect(self.rename_function)
        original_title = QLabel('原始のkey:')
        self.original_key = QLineEdit(self)
        rename_title = QLabel('替换のkey:')
        self.rename_key = QLineEdit(self)

        layout1 = QHBoxLayout()  # 原始关键字布局
        layout1.addWidget(original_title)
        layout1.addWidget(self.original_key)
        layout2 = QHBoxLayout()  # 替换关键字布局
        layout2.addWidget(rename_title)
        layout2.addWidget(self.rename_key)
        layout3 = QHBoxLayout()  # 路径输入布局
        layout3.addWidget(rename_path_title)
        layout3.addWidget(self.rename_path)
        layout3.addWidget(self.rename_path_bt)
        layout4 = QVBoxLayout()
        layout4.addLayout(layout1)
        layout4.addLayout(layout2)
        layout5 = QHBoxLayout()
        layout5.addLayout(layout4)
        layout5.addWidget(self.rename_bt)
        rename_layout.addLayout(layout3)
        rename_layout.addLayout(layout5)

        self.setLayout(rename_layout)

    def open_rename_folder(self):
        """导入改名路径"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.rename_folder = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

        if self.rename_folder:
            folder_name = os.path.basename(self.rename_folder)
            parent_directory = os.path.basename(os.path.dirname(self.rename_folder))
            display_path = os.path.join("…", parent_directory, folder_name)
            self.rename_path.setText(display_path)

    def rename_function(self):
        if self.rename_folder is None or self.rename_folder == '':
            success_message = QMessageBox()
            success_message.setIcon(QMessageBox.Information)
            success_message.setWindowTitle('呜呼')
            success_message.setText('未装载路径')
            success_message.exec_()
            return
        directory = self.rename_folder
        for filename in os.listdir(directory):
            original_key = self.original_key.text()
            rename_key = self.rename_key.text()
            # 检查文件是否含有"text"
            if original_key in filename:
                # 将含有"text"的文件名改为"line"
                new_filename = filename.replace(original_key, rename_key)
                # 构建文件的完整路径
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_filename)
                # 重命名文件
                os.rename(old_path, new_path)
                # print(f"Renamed {filename} to {new_filename}")
            else:
                success_message = QMessageBox()
                success_message.setIcon(QMessageBox.Information)
                success_message.setWindowTitle('呜呼')
                success_message.setText('改名失败!')
                success_message.exec_()

        success_message = QMessageBox()
        success_message.setIcon(QMessageBox.Information)
        success_message.setWindowTitle('Success')
        success_message.setText('改名成功!')
        success_message.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Rename_Widget()
    widget.show()
    sys.exit(app.exec_())


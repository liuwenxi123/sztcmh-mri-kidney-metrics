import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFrame,
                             QRadioButton, QGroupBox, QFileDialog, QMessageBox, QSizePolicy)
import nibabel as nib

class ConvNII_Widget(QWidget):
    def __init__(self):
        super().__init__()
        """nii转nii.gz及其逆过程"""
        conv_layout = QHBoxLayout()
        conv_title = QLabel('格式转换路径：')
        self.conv_path = QLabel(self)
        self.conv_path_bt = QPushButton('Folder')
        self.nii_to_gz = QPushButton('nii转nii.gz')
        self.gz_to_nii = QPushButton('nii.gz转nii')
        conv_groupbox = QGroupBox('格式转换')
        conv_groupbox.setLayout(conv_layout)
        conv_layout.addWidget(conv_title)
        conv_layout.addWidget(self.conv_path)
        conv_layout.addWidget(self.conv_path_bt)
        conv_layout.addWidget(self.nii_to_gz)
        conv_layout.addWidget(self.gz_to_nii)

        # 槽函数
        self.conv_path_bt.clicked.connect(self.open_conv_folder)
        self.gz_to_nii.clicked.connect(self.gz_to_nii_function)
        self.nii_to_gz.clicked.connect(self.nii_to_gz_function)

        self.setLayout(conv_layout)

    def open_conv_folder(self):
        """导入改名路径"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.conv_folder = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

        if self.conv_folder:
            folder_name = os.path.basename(self.conv_folder)
            parent_directory = os.path.basename(os.path.dirname(self.conv_folder))
            display_path = os.path.join("…", parent_directory, folder_name)
            self.conv_path.setText(display_path)

    def gz_to_nii_function(self):
        # 指定源文件夹路径
        if not self.conv_folder:
            return

        src_dir = self.conv_folder

        # 遍历文件夹下所有.nii.gz文件
        for filename in os.listdir(src_dir):
            if filename.endswith(".nii.gz"):
                # 打开nii.gz文件
                img = nib.load(os.path.join(src_dir, filename))

                # 获取nii.gz文件的原始数据和 affine 参数
                data = img.get_fdata()
                affine = img.affine

                # 创建一个新的nii文件，并保存
                new_img = nib.Nifti1Image(data, affine)
                new_filename = os.path.splitext(filename)[0]  # 去掉.gz扩展名
                nib.save(new_img, os.path.join(src_dir, new_filename))

                # 删除原来的nii.gz文件
                os.remove(os.path.join(src_dir, filename))

        success_message = QMessageBox()
        success_message.setIcon(QMessageBox.Information)
        success_message.setWindowTitle('Success')
        success_message.setText('转换完成!')
        success_message.exec_()

    def nii_to_gz_function(self):
        if not self.conv_folder:
            return

        src_dir = self.conv_folder

        # 遍历目录下的所有.nii文件
        for filename in os.listdir(src_dir):
            if filename.endswith(".nii"):
                src_file_path = os.path.join(src_dir, filename)
                dst_file_path = os.path.join(src_dir, filename.replace('.nii', '.nii.gz'))

                # 加载原始NIfTI文件
                img = nib.load(src_file_path)

                # 将图像数据保存为gzipped NIfTI文件
                nib.save(img, dst_file_path)

                # 删除原始.nii文件
                os.remove(src_file_path)

        success_message = QMessageBox()
        success_message.setIcon(QMessageBox.Information)
        success_message.setWindowTitle('Success')
        success_message.setText('转换完成!')
        success_message.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ConvNII_Widget()
    widget.show()
    sys.exit(app.exec_())


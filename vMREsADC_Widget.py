import sys
import os
import pandas as pd
import numpy as np
import nibabel as nib
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QRadioButton, QGroupBox, QFileDialog, QMessageBox, QCheckBox)

class vMREsADC_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.folder_path1 = None
        self.folder_path2 = None
        self.folder_path3 = None
        self.selected_file1 = None
        self.selected_file2 = None
        self.selected_file3 = None

        self.initUI()
        self.slot_function()
        self.show()
    def initUI(self):
        mainlayout = QVBoxLayout(self)

        label11 = QLabel('vMRE图像路径：')
        self.edit11 = QLabel(self)
        self.edit11.setFixedWidth(150)  # 设置宽度为200像素
        self.edit11.setFixedHeight(20)  # 设置高度为20像素
        self.button_vMREimage_folder = QPushButton('文件夹')
        layout11 = QHBoxLayout()
        layout11.addWidget(label11)
        layout11.addWidget(self.edit11)
        layout11.addWidget(self.button_vMREimage_folder)
        label12 = QLabel('vMRE图像文件：')
        self.edit12 = QLabel(self)
        self.edit12.setFixedWidth(150)  # 设置宽度为200像素
        self.edit12.setFixedHeight(20)  # 设置高度为20像素
        self.button_vMREimage_file = QPushButton('文件')
        layout12 = QHBoxLayout()
        layout12.addWidget(label12)
        layout12.addWidget(self.edit12)
        layout12.addWidget(self.button_vMREimage_file)
        layout1 = QHBoxLayout()
        layout1.addLayout(layout11)
        layout1.addLayout(layout12)

        label21 = QLabel('vMRE标签路径：')
        self.edit21 = QLabel(self)
        self.edit21.setFixedWidth(150)  # 设置宽度为200像素
        self.edit21.setFixedHeight(20)  # 设置高度为20像素
        self.button_vMRElabel_folder = QPushButton('文件夹')
        layout21 = QHBoxLayout()
        layout21.addWidget(label21)
        layout21.addWidget(self.edit21)
        layout21.addWidget(self.button_vMRElabel_folder)
        label22 = QLabel('vMRE标签文件：')
        self.edit22 = QLabel(self)
        self.edit22.setFixedWidth(150)  # 设置宽度为200像素
        self.edit22.setFixedHeight(20)  # 设置高度为20像素
        self.button_vMRElabel_file = QPushButton('文件')
        layout22 = QHBoxLayout()
        layout22.addWidget(label22)
        layout22.addWidget(self.edit22)
        layout22.addWidget(self.button_vMRElabel_file)
        layout2 = QHBoxLayout()
        layout2.addLayout(layout21)
        layout2.addLayout(layout22)

        label31 = QLabel('sADC图像路径：')
        self.edit31 = QLabel(self)
        self.edit31.setFixedWidth(150)  # 设置宽度为200像素
        self.edit31.setFixedHeight(20)  # 设置高度为20像素
        self.button_sADCimage_folder = QPushButton('文件夹')
        layout31 = QHBoxLayout()
        layout31.addWidget(label31)
        layout31.addWidget(self.edit31)
        layout31.addWidget(self.button_sADCimage_folder)
        label32 = QLabel('sADC图像文件：')
        self.edit32 = QLabel(self)
        self.edit32.setFixedWidth(150)  # 设置宽度为200像素
        self.edit32.setFixedHeight(20)  # 设置高度为20像素
        self.button_sADCimage_file = QPushButton('文件')
        layout32 = QHBoxLayout()
        layout32.addWidget(label32)
        layout32.addWidget(self.edit32)
        layout32.addWidget(self.button_sADCimage_file)
        layout3 = QHBoxLayout()
        layout3.addLayout(layout31)
        layout3.addLayout(layout32)

        label41 = QLabel('阈值下限：')
        self.edit_threshold = QLineEdit(self)
        layout41 = QHBoxLayout()
        layout41.addWidget(label41)
        layout41.addWidget(self.edit_threshold)
        label42 = QLabel('模式选择：')
        self.button_folder = QRadioButton('文件夹')
        self.button_file = QRadioButton('文件')
        layout42 = QHBoxLayout()
        # layout42.addWidget(label42)
        layout42.addWidget(self.button_folder)
        layout42.addWidget(self.button_file)
        label43 = QLabel('b值组合:')
        self.cbutton200_800 = QCheckBox('200-800')
        self.cbutton200_1000 = QCheckBox('200-1000')
        self.cbutton200_1200 = QCheckBox('200-1200')
        self.cbutton200_1500 = QCheckBox('200-1500')
        self.cbutton200_2000 = QCheckBox('200-2000')
        self.cbutton400_1200 = QCheckBox('400-1200')
        self.cbutton400_1500 = QCheckBox('400-1500')
        self.cbutton200_800.setChecked(True)
        self.cbutton200_1000.setChecked(True)
        self.cbutton200_1200.setChecked(True)
        self.cbutton200_1500.setChecked(True)
        self.cbutton200_2000.setChecked(True)
        self.cbutton400_1200.setChecked(True)
        self.cbutton400_1500.setChecked(True)
        layout43 = QHBoxLayout()
        layout43.addWidget(label43)
        layout43.addWidget(self.cbutton200_800)
        layout43.addWidget(self.cbutton200_1000)
        layout43.addWidget(self.cbutton200_1200)
        layout43.addWidget(self.cbutton200_1500)
        layout43.addWidget(self.cbutton200_2000)
        layout43.addWidget(self.cbutton400_1200)
        layout43.addWidget(self.cbutton400_1500)
        layout4 = QHBoxLayout()
        layout4.addLayout(layout41)
        layout4.addLayout(layout43)

        self.origin_vMRE = HorizontalLayout_Widget('原始vMRE均值：', '1')
        self.origin_sADC = HorizontalLayout_Widget('原始sADC均值：', '1')
        self.new_vMRE = HorizontalLayout_Widget('新sADC均值：', '4')
        self.new_sADC = HorizontalLayout_Widget('新sADC均值：', '5')
        self.rest_num = HorizontalLayout_Widget('总点数：', '1')
        self.sift_num = HorizontalLayout_Widget('被筛点数：', '4')
        layout51 = QVBoxLayout()
        layout51.addWidget(self.origin_vMRE)
        layout51.addWidget(self.origin_sADC)
        layout52 = QVBoxLayout()
        layout52.addWidget(self.new_vMRE)
        layout52.addWidget(self.new_sADC)
        layout53 = QVBoxLayout()
        layout53.addWidget(self.rest_num)
        layout53.addWidget(self.sift_num)
        layout5 = QHBoxLayout()
        layout5.addLayout(layout51)
        layout5.addLayout(layout52)
        layout5.addLayout(layout53)

        self.label61 = QLabel('导出路径：')
        self.edit61 = QLabel(self)
        self.edit61.setFixedWidth(150)
        self.edit61.setFixedHeight(20)
        self.button_export_folder = QPushButton('文件夹')
        layout61 = QHBoxLayout()
        layout61.addWidget(self.label61)
        layout61.addWidget(self.edit61)
        layout61.addWidget(self.button_export_folder)
        self.label62 = QLabel('文件名称：')
        self.name_edit = QLineEdit(self)
        layout62 = QHBoxLayout()
        layout62.addWidget(self.label62)
        layout62.addWidget(self.name_edit)
        layout6 = QHBoxLayout()
        layout6.addLayout(layout61)
        layout6.addLayout(layout62)

        self.button_cal = QPushButton('单项计算')
        self.button_exp = QPushButton('批量导出')
        layout7 = QHBoxLayout()
        layout7.addWidget(self.button_cal)
        layout7.addWidget(self.button_exp)

        mainlayout.addLayout(layout42)
        mainlayout.addLayout(layout1)
        mainlayout.addLayout(layout2)
        mainlayout.addLayout(layout3)
        mainlayout.addLayout(layout4)
        mainlayout.addLayout(layout5)
        mainlayout.addLayout(layout6)
        mainlayout.addLayout(layout7)

    def slot_function(self):
        self.button_vMREimage_folder.clicked.connect(self.open_vMRE_imagefolder)
        self.button_vMREimage_file.clicked.connect(self.open_vMRE_imagefile)
        self.button_vMRElabel_folder.clicked.connect(self.open_vMRE_imagefolder)
        self.button_vMRElabel_file.clicked.connect(self.open_vMRE_imagefile)
        self.button_sADCimage_folder.clicked.connect(self.open_vMRE_imagefolder)
        self.button_sADCimage_file.clicked.connect(self.open_vMRE_imagefile)

    def open_vMRE_imagefile(self):
        """打开vMRE图像文件"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("NIfTI Files (*.nii *.nii.gz);;All Files (*)")

        if file_dialog.exec_() == QFileDialog.Accepted:
            self.selected_file1 = file_dialog.selectedFiles()[0]
            # 获取文件名
            self.base_name1 = os.path.basename(self.selected_file1)
            self.edit12.setText(self.base_name1)

    def open_vMRE_labelfile(self):
        """打开vMRE标签文件"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("NIfTI Files (*.nii *.nii.gz);;All Files (*)")

        if file_dialog.exec_() == QFileDialog.Accepted:
            self.selected_file2 = file_dialog.selectedFiles()[0]
            # 获取文件名
            self.base_name2 = os.path.basename(self.selected_file2)
            self.edit22.setText(self.base_name2)

    def open_sADC_imagefile(self):
        """打开sADC图像文件"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("NIfTI Files (*.nii *.nii.gz);;All Files (*)")

        if file_dialog.exec_() == QFileDialog.Accepted:
            self.selected_file3 = file_dialog.selectedFiles()[0]
            # 获取文件名
            self.base_name3 = os.path.basename(self.selected_file3)
            self.edit32.setText(self.base_name3)

    def open_vMRE_imagefolder(self):
        """打开vMRE图像文件夹"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.folder_path1 = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if self.folder_path1:
            """打印文件夹名称"""
            folder_name = os.path.basename(self.folder_path1)
            parent_directory = os.path.basename(os.path.dirname(self.folder_path1))
            display_path = os.path.join("…", parent_directory, folder_name)
            self.edit11.setText(display_path)

    def open_vMRE_labelfolder(self):
        """打开vMRE标签文件夹"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.folder_path2 = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if self.folder_path2:
            """打印文件夹名称"""
            folder_name = os.path.basename(self.folder_path2)
            parent_directory = os.path.basename(os.path.dirname(self.folder_path2))
            display_path = os.path.join("…", parent_directory, folder_name)
            self.edit21.setText(display_path)

    def open_sADC_imagefolder(self):
        """打开sADC图像文件夹"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.folder_path3 = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if self.folder_path3:
            """打印文件夹名称"""
            folder_name = os.path.basename(self.folder_path3)
            parent_directory = os.path.basename(os.path.dirname(self.folder_path3))
            display_path = os.path.join("…", parent_directory, folder_name)
            self.edit31.setText(display_path)

    def calculate_folder(self):
        pass





class HorizontalLayout_Widget(QWidget):
    def __init__(self, labels, values):
        super().__init__()

        self.title = QLabel(labels)
        self.value = QLabel(values)
        layout = QHBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.value)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = vMREsADC_Widget()
    widget.show()
    sys.exit(app.exec_())




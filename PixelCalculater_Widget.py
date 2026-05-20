import sys
import os
import pandas as pd
import numpy as np
import nibabel as nib
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QRadioButton, QGroupBox, QFileDialog, QMessageBox)

class PixelCalculater_Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.folder_path1 = None
        self.folder_path2 = None
        self.selected_file1 = None
        self.selected_file2 = None
        self.base_name1 = None
        self.left_kidney_mean = None
        self.right_kidney_mean = None
        self.overlap_mean = None

        title1 = QLabel("图像文件:")
        self.edit1 = QLabel(self)
        self.edit1.setFixedWidth(150)  # 设置宽度为200像素
        self.edit1.setFixedHeight(20)  # 设置高度为20像素
        self.bt1 = QPushButton('file')
        self.bt1.clicked.connect(self.open_image)
        layout_image = QHBoxLayout()
        layout_image.addWidget(title1)
        layout_image.addWidget(self.edit1)
        layout_image.addWidget(self.bt1)

        title2 = QLabel("标签文件:")
        self.edit2 = QLabel(self)
        self.edit2.setFixedWidth(150)  # 设置宽度为200像素
        self.edit2.setFixedHeight(20)  # 设置高度为20像素
        self.bt2 = QPushButton('file')
        self.bt2.clicked.connect(self.open_label)
        layout_label = QHBoxLayout()
        layout_label.addWidget(title2)
        layout_label.addWidget(self.edit2)
        layout_label.addWidget(self.bt2)

        layout_file = QVBoxLayout()
        layout_file.addLayout(layout_image)
        layout_file.addLayout(layout_label)

        title3 = QLabel('导出文件名称:')
        self.edit3 = QLineEdit("result.xlsx")
        layout_ex = QHBoxLayout()
        layout_ex.addWidget(title3)
        layout_ex.addWidget(self.edit3)

        title5 = QLabel("图像路径:")
        self.edit5 = QLabel(self)
        self.edit5.setFixedWidth(150)  # 设置宽度为200像素
        self.edit5.setFixedHeight(20)  # 设置高度为20像素
        self.bt5 = QPushButton('folder')
        self.bt5.clicked.connect(self.open_image_folder)
        layout_imagefolder = QHBoxLayout()
        layout_imagefolder.addWidget(title5)
        layout_imagefolder.addWidget(self.edit5)
        layout_imagefolder.addWidget(self.bt5)

        title6 = QLabel("标签路径:")
        self.edit6 = QLabel(self)
        self.edit6.setFixedWidth(150)  # 设置宽度为200像素
        self.edit6.setFixedHeight(20)  # 设置高度为20像素
        self.bt6 = QPushButton('folder')
        self.bt6.clicked.connect(self.open_label_folder)
        layout_labelfolder = QHBoxLayout()
        layout_labelfolder.addWidget(title6)
        layout_labelfolder.addWidget(self.edit6)
        layout_labelfolder.addWidget(self.bt6)

        self.filebt = QRadioButton('单独计算')
        self.folderbt = QRadioButton('批量计算')
        self.filebt.setChecked(True)
        self.filebt.toggled.connect(self.filebt_toggled)
        self.folderbt.toggled.connect(self.folderbt_toggled)
        layout_ffbt = QVBoxLayout()
        layout_ffbt.addWidget(self.filebt)
        layout_ffbt.addWidget(self.folderbt)
        groupbox_ffbt = QGroupBox('模式选择')
        groupbox_ffbt.setLayout(layout_ffbt)

        layout_folder = QVBoxLayout()
        layout_folder.addLayout(layout_imagefolder)
        layout_folder.addLayout(layout_labelfolder)

        self.all_volume = HorizontalLayoutWidget('全层体积', '1')
        self.all_mean = HorizontalLayoutWidget('全层均值', '5')
        # self.all_volume3 = HorizontalLayoutWidget('三层体积', '1')
        # self.all_mean3 = HorizontalLayoutWidget('三层均值', '5')
        self.all_radiobt = QRadioButton('参与导出')
        # self.all_radiobt3 = QRadioButton('导出三层结果')
        self.all_radiobt.setChecked(True)
        all_layout = QVBoxLayout()
        all_layout.addWidget(self.all_volume)
        all_layout.addWidget(self.all_mean)
        # all_layout.addWidget(self.all_volume3)
        # all_layout.addWidget(self.all_mean3)
        all_layout.addWidget(self.all_radiobt)
        # all_layout.addWidget(self.all_radiobt3)
        all_box = QGroupBox('全肾')
        all_box.setLayout(all_layout)

        self.left_volume = HorizontalLayoutWidget('全层体积', '1')
        self.left_mean = HorizontalLayoutWidget('全层均值', '1')
        # self.left_volume3 = HorizontalLayoutWidget('三层体积', '1')
        # self.left_mean3 = HorizontalLayoutWidget('三层均值', '1')
        self.left_radiobt = QRadioButton('参与导出')
        # self.left_radiobt3 = QRadioButton('导出三层结果')
        self.left_radiobt.setChecked(True)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.left_volume)
        left_layout.addWidget(self.left_mean)
        # left_layout.addWidget(self.left_volume3)
        # left_layout.addWidget(self.left_mean3)
        left_layout.addWidget(self.left_radiobt)
        # left_layout.addWidget(self.left_radiobt3)
        left_box = QGroupBox('右肾')
        left_box.setLayout(left_layout)

        self.right_volume = HorizontalLayoutWidget('全层体积', '4')
        self.right_mean = HorizontalLayoutWidget('全层均值', '4')
        # self.right_volume3 = HorizontalLayoutWidget('三层体积', '4')
        # self.right_mean3 = HorizontalLayoutWidget('三层均值', '4')
        self.right_radiobt = QRadioButton('参与导出')
        # self.right_radiobt3 = QRadioButton('导出三层结果')
        self.right_radiobt.setChecked(True)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.right_volume)
        right_layout.addWidget(self.right_mean)
        # right_layout.addWidget(self.right_volume3)
        # right_layout.addWidget(self.right_mean3)
        right_layout.addWidget(self.right_radiobt)
        # right_layout.addWidget(self.right_radiobt3)
        right_box = QGroupBox('左肾')
        right_box.setLayout(right_layout)

        layout_results = QHBoxLayout()
        layout_results.addWidget(all_box)
        layout_results.addWidget(left_box)
        layout_results.addWidget(right_box)

        self.calculate_bt = QPushButton('计算')
        self.calculate_bt.clicked.connect(self.calculate_pixel_mean_and_volume)
        self.exporting_bt = QPushButton('导出')
        self.exporting_bt.clicked.connect(self.exporting_data)
        self.bulkexport_bt = QPushButton('批量导出全层结果')
        self.bulkexport_bt3 = QPushButton('批量导出三层结果')
        self.bulkexport_bt.clicked.connect(self.calculate_pixel_mean_for_all_patients)
        self.bulkexport_bt3.clicked.connect(self.calculate_pixel_mean_for_all_patients3)

        bt_layout = QHBoxLayout()
        bt_layout.addWidget(self.calculate_bt)
        bt_layout.addWidget(self.exporting_bt)
        bt_layout.addWidget(self.bulkexport_bt)
        bt_layout.addWidget(self.bulkexport_bt3)

        sublayout = QHBoxLayout()
        sublayout.addLayout(layout_file)
        sublayout.addLayout(layout_folder)
        # sublayout.addLayout(layout_ffbt)
        sublayout.addWidget(groupbox_ffbt)

        layout = QVBoxLayout()
        layout.addLayout(sublayout)
        layout.addLayout(layout_results)
        layout.addLayout(layout_ex)
        layout.addLayout(bt_layout)

        self.filebt_toggled()

        self.setLayout(layout)

    def open_image(self):
        """打开图像文件或文件夹"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("NIfTI Files (*.nii *.nii.gz);;All Files (*)")

        if file_dialog.exec_() == QFileDialog.Accepted:
            self.selected_file1 = file_dialog.selectedFiles()[0]

            # 获取文件名
            self.base_name1 = os.path.basename(self.selected_file1)
            self.edit1.setText(self.base_name1)

    def open_label(self):
        """打开标签文件"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("NIfTI Files (*.nii *.nii.gz);;All Files (*)")

        if file_dialog.exec_() == QFileDialog.Accepted:
            self.selected_file2 = file_dialog.selectedFiles()[0]
            # print("Selected File:", self.selected_file2)

            # 获取文件名
            self.base_name2 = os.path.basename(self.selected_file2)
            self.edit2.setText(self.base_name2)

    def open_image_folder(self):
        """打开图像文件夹"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.folder_path1 = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

        if self.folder_path1:
            """打印文件夹名称"""
            folder_name = os.path.basename(self.folder_path1)
            parent_directory = os.path.basename(os.path.dirname(self.folder_path1))
            display_path = os.path.join("…", parent_directory, folder_name)
            self.edit5.setText(display_path)

            print("Folder Name:", folder_name)
            print("Parent Directory:", parent_directory)

    def open_label_folder(self):
        """打开标签文件夹"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.folder_path2 = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

        if self.folder_path2:
            """打印文件夹名称"""
            folder_name = os.path.basename(self.folder_path2)
            parent_directory = os.path.basename(os.path.dirname(self.folder_path2))
            display_path = os.path.join("…", parent_directory, folder_name)
            self.edit6.setText(display_path)

            print("Folder Name:", folder_name)
            print("Parent Directory:", parent_directory)

    def calculate_pixel_mean_and_volume(self):
        """计算标签覆盖范围下，图像像素的均值和体积"""
        if not self.selected_file1 or not self.selected_file2:
            return
        img = nib.load(self.selected_file1)
        label = nib.load(self.selected_file2)
        if img.shape != label.shape:
            QMessageBox.critical(self, "Error", "Image and label dimensions do not match.")
            return
        image_data = img.get_fdata()
        label_data = label.get_fdata()

        overlapping_pixels = image_data[label_data.nonzero()]
        self.overlap_mean = np.mean(overlapping_pixels)
        self.overlap_volume = np.sum(label_data > 0)

        midline_index = image_data.shape[0] // 2

        # Left kidney
        left_kidney_pixels = image_data[:midline_index, :, :][label_data[:midline_index, :, :] > 0]
        self.left_kidney_mean = np.mean(left_kidney_pixels)
        self.left_kidney_volume = np.sum(label_data[:midline_index, :, :] > 0)

        # Right kidney
        right_kidney_pixels = image_data[midline_index:, :, :][label_data[midline_index:, :, :] > 0]
        self.right_kidney_mean = np.mean(right_kidney_pixels)
        self.right_kidney_volume = np.sum(label_data[midline_index:, :, :] > 0)

        self.all_volume.value.setText(str(self.overlap_volume))
        self.all_mean.value.setText(str(self.overlap_mean))
        self.left_volume.value.setText(str(self.left_kidney_volume))
        self.left_mean.value.setText(str(self.left_kidney_mean))
        self.right_volume.value.setText(str(self.right_kidney_volume))
        self.right_mean.value.setText(str(self.right_kidney_mean))

    def exporting_data(self):
        # if not self.base_name1:
        #     return
        self.data_dict = {
            "PatientID": [self.base_name1],
            # "label": [self.base_name2],
        }
        if self.right_radiobt.isChecked():
            self.data_dict["Right Mean"] = [self.right_kidney_mean]
        if self.left_radiobt.isChecked():
            self.data_dict["Left Mean"] = [self.left_kidney_mean]
        if self.all_radiobt.isChecked():
            self.data_dict["All Mean"] = [self.overlap_mean]

        # 将数据添加到 DataFrame
        df = pd.DataFrame(self.data_dict)

        # 读取 Excel 文件，如果文件不存在，则创建一个新的
        excel_file_path = self.edit3.text()
        try:
            existing_df = pd.read_excel(excel_file_path)
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass
        df.to_excel(excel_file_path, index=False)

        success_message = QMessageBox()
        success_message.setIcon(QMessageBox.Information)
        success_message.setWindowTitle('Success')
        success_message.setText('生成成功!')
        success_message.exec_()

    def calculate_pixel_mean_for_all_patients(self):
        """批量计算"""
        if not self.folder_path1 or not self.folder_path2:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("警告")
            msg_box.setText("文件夹打开错误")
            msg_box.exec_()
            return

        image_files = sorted([f for f in os.listdir(self.folder_path1) if f.endswith(".nii.gz") or f.endswith(".nii")])
        label_files = sorted([f for f in os.listdir(self.folder_path2) if f.endswith(".nii.gz") or f.endswith(".nii")])
        results = []

        if len(image_files) != len(label_files):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("警告")
            msg_box.setText("图像和标签的数量不匹配")
            msg_box.exec_()
            return

        for i in range(len(image_files)):
            image_file_path = os.path.join(self.folder_path1, image_files[i])
            label_file_path = os.path.join(self.folder_path2, label_files[i])

            if not os.path.exists(image_file_path) or not os.path.exists(label_file_path):
                print(f"Error: Image or label file does not exist for {image_files[i]}")
                continue

            # Load image and label data
            img = nib.load(image_file_path)
            label = nib.load(label_file_path)

            # Check if dimensions match
            if img.shape != label.shape:
                print(f"Error: Dimensions do not match for {image_files[i]}")
                continue

            image_data = img.get_fdata()
            label_data = label.get_fdata()

            # Calculate mean pixel value for the overlap region
            overlapping_pixels = image_data[label_data.nonzero()]
            mean_pixel_value = np.mean(overlapping_pixels) if overlapping_pixels.size > 0 else np.nan

            midline_index = image_data.shape[0] // 2

            left_kidney_pixels = image_data[:midline_index, :, :][label_data[:midline_index, :, :] > 0]
            left_kidney_mean = np.mean(left_kidney_pixels) if left_kidney_pixels.size > 0 else np.nan

            right_kidney_pixels = image_data[midline_index:, :, :][label_data[midline_index:, :, :] > 0]
            right_kidney_mean = np.mean(right_kidney_pixels) if right_kidney_pixels.size > 0 else np.nan

            # Get patient ID from the file name (assuming file names are in the format "PatientID...")
            patient_id = os.path.splitext(image_files[i])[0]

            # Append the result to the list
            results.append({"PatientID": patient_id,
                            "all": mean_pixel_value,
                            "right": left_kidney_mean,
                            "left": right_kidney_mean})

        # Convert list to DataFrame
        self.results = pd.DataFrame(results)

        # Save results to Excel file
        output_file = self.edit3.text()
        self.results.to_excel(output_file, index=False)
        success_message = QMessageBox()
        success_message.setIcon(QMessageBox.Information)
        success_message.setWindowTitle('Success')
        success_message.setText('生成成功!')
        success_message.exec_()

    def calculate_pixel_mean_for_all_patients3(self):
        """批量计算3"""
        if not self.folder_path1 or not self.folder_path2:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("警告")
            msg_box.setText("文件夹打开错误")
            msg_box.exec_()
            return

        image_files = sorted([f for f in os.listdir(self.folder_path1) if f.endswith(".nii.gz") or f.endswith(".nii")])
        label_files = sorted([f for f in os.listdir(self.folder_path2) if f.endswith(".nii.gz") or f.endswith(".nii")])
        self.results = pd.DataFrame(columns=["PatientID", "all", "right", "left"])

        if len(image_files) != len(label_files):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("警告")
            msg_box.setText("图像和标签的数量不匹配")
            msg_box.exec_()
            return

        result_df = pd.DataFrame(columns=['Image_File', 'Kidney_Mean', 'Right_Mean', 'Left_Mean'])

        length = len(image_files)

        for i in range(length):
            image_file_path = os.path.join(self.folder_path1, image_files[i])
            label_file_path = os.path.join(self.folder_path2, label_files[i])

            if not os.path.exists(image_file_path) or not os.path.exists(label_file_path):
                print(f"Error: Image or label file does not exist for {image_files[i]}")
                continue

            image_data = nib.load(image_file_path).get_fdata()
            label_data = nib.load(label_file_path).get_fdata()

            # Check if dimensions match
            if image_data.shape != label_data.shape:
                print(f"Error: Dimensions do not match for {image_files[i]}")
                continue

            first_non_zero_page = None
            last_non_zero_page = None
            first_left_non_zero_page = None
            last_left_non_zero_page = None
            first_right_non_zero_page = None
            last_right_non_zero_page = None

            midline_index = image_data.shape[0] // 2  # 矢状面分界线

            for z in range(label_data.shape[2]):
                # 检查当前冠状面是否有非零标签
                if np.any(label_data[:, :, z] > 0):  # 全肾
                    if first_non_zero_page is None:
                        first_non_zero_page = z
                    last_non_zero_page = z
                if np.any(label_data[:midline_index, :, z] > 0):  # 左肾
                    if first_left_non_zero_page is None:
                        first_left_non_zero_page = z
                    last_left_non_zero_page = z
                if np.any(label_data[midline_index:, :, z] > 0):  # 右肾
                    if first_right_non_zero_page is None:
                        first_right_non_zero_page = z
                    last_right_non_zero_page = z

            mid_index = (first_non_zero_page + last_non_zero_page) / 2
            mid_left_index = (first_left_non_zero_page + last_left_non_zero_page) / 2
            mid_right_index = (first_right_non_zero_page + last_right_non_zero_page) / 2

            # print(mid_index, mid_left_index, mid_right_index)

            # coronal_middle_slices = slice(image_data.shape[2] // 3, (image_data.shape[2] // 3) * 2 + 1)  # 中间三层
            coronal_middle_slices = slice(int(mid_index - 1), int(mid_index + 1))  # 中间三层
            coronal_left_middle_slices = slice(int(mid_left_index - 1), int(mid_left_index + 1))  # 中间三层
            coronal_right_middle_slices = slice(int(mid_right_index - 1), int(mid_right_index + 1))  # 中间三层

            # 全肾
            all_kidney_pixels = image_data[:, :, coronal_middle_slices][
                label_data[:, :, coronal_middle_slices] > 0]
            all_kidney_mean = np.mean(all_kidney_pixels) if len(all_kidney_pixels) > 0 else None

            # 左肾
            left_kidney_pixels = image_data[:midline_index, :, coronal_left_middle_slices][
                label_data[:midline_index, :, coronal_left_middle_slices] > 0]
            left_kidney_mean = np.mean(left_kidney_pixels) if len(left_kidney_pixels) > 0 else None

            # 右肾
            right_kidney_pixels = image_data[midline_index:, :, coronal_right_middle_slices][
                label_data[midline_index:, :, coronal_right_middle_slices] > 0]
            right_kidney_mean = np.mean(right_kidney_pixels) if len(right_kidney_pixels) > 0 else None

            result_df = pd.concat([result_df, pd.DataFrame({'Image_File': [image_files[i]],
                                                            'Kidney_Mean': [all_kidney_mean],
                                                            'Right_Mean': [left_kidney_mean],
                                                            'Left_Mean': [right_kidney_mean]})])

        output_file = self.edit3.text()
        result_df.to_excel(output_file, index=False)
        success_message = QMessageBox()
        success_message.setIcon(QMessageBox.Information)
        success_message.setWindowTitle('Success')
        success_message.setText('生成成功!')
        success_message.exec_()

    def filebt_toggled(self):
        """单个计算和导出"""
        self.bt1.setEnabled(True)
        self.bt2.setEnabled(True)
        self.calculate_bt.setEnabled(True)
        self.exporting_bt.setEnabled(True)
        self.bt5.setEnabled(False)
        self.bt6.setEnabled(False)
        self.bulkexport_bt.setEnabled(False)
        self.bulkexport_bt3.setEnabled(False)

    def folderbt_toggled(self):
        """批量计算和导出"""
        self.bt1.setEnabled(False)
        self.bt2.setEnabled(False)
        self.calculate_bt.setEnabled(False)
        self.exporting_bt.setEnabled(False)
        self.bt5.setEnabled(True)
        self.bt6.setEnabled(True)
        self.bulkexport_bt.setEnabled(True)
        self.bulkexport_bt3.setEnabled(True)


class HorizontalLayoutWidget(QWidget):
    def __init__(self, labels, values):
        super().__init__()

        self.title = QLabel(labels)
        self.value = QLabel(values)
        layout = QHBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PixelCalculater_Widget()
    widget.show()
    sys.exit(app.exec_())

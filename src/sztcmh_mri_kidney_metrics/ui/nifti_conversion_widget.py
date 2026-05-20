from __future__ import annotations

from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from sztcmh_mri_kidney_metrics.services.nifti_conversion import convert_directory_from_gz, convert_directory_to_gz
from sztcmh_mri_kidney_metrics.ui.shared import pick_directory, short_display, show_error, show_info


class NiftiConversionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.directory = ''
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        group = QGroupBox('NIfTI 格式转换')
        group_layout = QVBoxLayout(group)
        self.path_label = QLabel('')
        choose_button = QPushButton('选择目录')
        choose_button.clicked.connect(self._choose_directory)
        path_row = QHBoxLayout()
        path_row.addWidget(QLabel('目录:'))
        path_row.addWidget(self.path_label)
        path_row.addWidget(choose_button)
        button_row = QHBoxLayout()
        to_gz = QPushButton('nii -> nii.gz')
        to_gz.clicked.connect(self._to_gz)
        from_gz = QPushButton('nii.gz -> nii')
        from_gz.clicked.connect(self._from_gz)
        button_row.addWidget(to_gz)
        button_row.addWidget(from_gz)
        group_layout.addLayout(path_row)
        group_layout.addLayout(button_row)
        layout.addWidget(group)

    def _choose_directory(self):
        self.directory = pick_directory(self, '选择转换目录')
        self.path_label.setText(short_display(self.directory))

    def _to_gz(self):
        if not self.directory:
            show_error(self, '请先选择目录。')
            return
        converted = convert_directory_to_gz(self.directory)
        show_info(self, f'转换完成，共处理 {len(converted)} 个文件。')

    def _from_gz(self):
        if not self.directory:
            show_error(self, '请先选择目录。')
            return
        converted = convert_directory_from_gz(self.directory)
        show_info(self, f'转换完成，共处理 {len(converted)} 个文件。')

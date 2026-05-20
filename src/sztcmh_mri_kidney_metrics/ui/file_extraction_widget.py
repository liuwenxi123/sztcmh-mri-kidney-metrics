from __future__ import annotations

from PyQt5.QtWidgets import QButtonGroup, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QVBoxLayout, QWidget

from sztcmh_mri_kidney_metrics.services.file_extraction import ExtractionMode, extract_matching_files
from sztcmh_mri_kidney_metrics.ui.shared import pick_directory, short_display, show_error, show_info


class FileExtractionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.source_dir = ''
        self.destination_dir = ''
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        group = QGroupBox('文件抓取')
        group_layout = QVBoxLayout(group)
        self.source_label = QLabel('')
        self.destination_label = QLabel('')
        source_button = QPushButton('选择源目录')
        destination_button = QPushButton('选择保存目录')
        source_button.clicked.connect(self._choose_source)
        destination_button.clicked.connect(self._choose_destination)
        source_row = QHBoxLayout()
        source_row.addWidget(QLabel('源目录:'))
        source_row.addWidget(self.source_label)
        source_row.addWidget(source_button)
        destination_row = QHBoxLayout()
        destination_row.addWidget(QLabel('保存目录:'))
        destination_row.addWidget(self.destination_label)
        destination_row.addWidget(destination_button)
        self.nested_key_edit = QLineEdit()
        self.filename_key_edit = QLineEdit()
        form = QFormLayout()
        form.addRow('二级目录 key:', self.nested_key_edit)
        form.addRow('文件名 key:', self.filename_key_edit)
        self.direct_button = QRadioButton('直接抓取')
        self.first_button = QRadioButton('一级抓取')
        self.second_button = QRadioButton('二级抓取')
        self.direct_button.setChecked(True)
        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.direct_button)
        self.mode_group.addButton(self.first_button)
        self.mode_group.addButton(self.second_button)
        mode_row = QHBoxLayout()
        mode_row.addWidget(self.direct_button)
        mode_row.addWidget(self.first_button)
        mode_row.addWidget(self.second_button)
        run_button = QPushButton('开始抓取')
        run_button.clicked.connect(self._run)
        group_layout.addLayout(source_row)
        group_layout.addLayout(destination_row)
        group_layout.addLayout(form)
        group_layout.addLayout(mode_row)
        group_layout.addWidget(run_button)
        layout.addWidget(group)

    def _choose_source(self):
        self.source_dir = pick_directory(self, '选择源目录')
        self.source_label.setText(short_display(self.source_dir))

    def _choose_destination(self):
        self.destination_dir = pick_directory(self, '选择保存目录')
        self.destination_label.setText(short_display(self.destination_dir))

    def _mode(self) -> ExtractionMode:
        if self.first_button.isChecked():
            return ExtractionMode.FIRST_LEVEL
        if self.second_button.isChecked():
            return ExtractionMode.SECOND_LEVEL
        return ExtractionMode.DIRECT

    def _run(self):
        if not self.source_dir or not self.destination_dir:
            show_error(self, '请先选择源目录和保存目录。')
            return
        copied = extract_matching_files(self.source_dir, self.destination_dir, self.nested_key_edit.text(), self.filename_key_edit.text(), self._mode())
        show_info(self, f'抓取完成，共复制 {len(copied)} 个文件。')

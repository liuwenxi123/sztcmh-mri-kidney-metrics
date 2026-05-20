from __future__ import annotations

from PyQt5.QtWidgets import QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from sztcmh_mri_kidney_metrics.services.export_service import export_rows_to_excel
from sztcmh_mri_kidney_metrics.services.vmre_workflows import calculate_directory_threshold_metrics, calculate_single_threshold_metrics
from sztcmh_mri_kidney_metrics.ui.shared import pick_directory, pick_file, short_display, show_error, show_info


class VmreSadcWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.vmre_file = ''
        self.label_file = ''
        self.sadc_file = ''
        self.vmre_dir = ''
        self.label_dir = ''
        self.sadc_dir = ''
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        group = QGroupBox('vMRE / sADC 分析')
        group_layout = QVBoxLayout(group)
        self.vmre_file_label = QLabel('')
        self.label_file_label = QLabel('')
        self.sadc_file_label = QLabel('')
        self.vmre_dir_label = QLabel('')
        self.label_dir_label = QLabel('')
        self.sadc_dir_label = QLabel('')
        self.threshold_edit = QLineEdit('0')
        self.output_edit = QLineEdit('vmre_sadc_result.xlsx')
        rows = [
            ('vMRE 文件:', self.vmre_file_label, self._choose_vmre_file),
            ('标签文件:', self.label_file_label, self._choose_label_file),
            ('sADC 文件:', self.sadc_file_label, self._choose_sadc_file),
            ('vMRE 目录:', self.vmre_dir_label, self._choose_vmre_dir),
            ('标签目录:', self.label_dir_label, self._choose_label_dir),
            ('sADC 目录:', self.sadc_dir_label, self._choose_sadc_dir),
        ]
        for title, label, handler in rows:
            row = QHBoxLayout()
            row.addWidget(QLabel(title))
            row.addWidget(label)
            button = QPushButton('选择')
            button.clicked.connect(handler)
            row.addWidget(button)
            group_layout.addLayout(row)
        form = QFormLayout()
        form.addRow('阈值:', self.threshold_edit)
        form.addRow('导出文件:', self.output_edit)
        group_layout.addLayout(form)
        single_button = QPushButton('单文件计算')
        single_button.clicked.connect(self._run_single)
        batch_button = QPushButton('批量导出')
        batch_button.clicked.connect(self._run_batch)
        button_row = QHBoxLayout()
        button_row.addWidget(single_button)
        button_row.addWidget(batch_button)
        group_layout.addLayout(button_row)
        layout.addWidget(group)

    def _choose_vmre_file(self):
        self.vmre_file = pick_file(self, '选择 vMRE 文件')
        self.vmre_file_label.setText(short_display(self.vmre_file))

    def _choose_label_file(self):
        self.label_file = pick_file(self, '选择标签文件')
        self.label_file_label.setText(short_display(self.label_file))

    def _choose_sadc_file(self):
        self.sadc_file = pick_file(self, '选择 sADC 文件')
        self.sadc_file_label.setText(short_display(self.sadc_file))

    def _choose_vmre_dir(self):
        self.vmre_dir = pick_directory(self, '选择 vMRE 目录')
        self.vmre_dir_label.setText(short_display(self.vmre_dir))

    def _choose_label_dir(self):
        self.label_dir = pick_directory(self, '选择标签目录')
        self.label_dir_label.setText(short_display(self.label_dir))

    def _choose_sadc_dir(self):
        self.sadc_dir = pick_directory(self, '选择 sADC 目录')
        self.sadc_dir_label.setText(short_display(self.sadc_dir))

    def _threshold(self) -> float:
        return float(self.threshold_edit.text() or '0')

    def _run_single(self):
        if not self.vmre_file or not self.label_file or not self.sadc_file:
            show_error(self, '请先选择单文件输入。')
            return
        row = calculate_single_threshold_metrics(self.vmre_file, self.label_file, self.sadc_file, self._threshold())
        export_rows_to_excel([row], self.output_edit.text())
        show_info(self, f'单文件结果已导出到 {self.output_edit.text()}')

    def _run_batch(self):
        if not self.vmre_dir or not self.label_dir or not self.sadc_dir:
            show_error(self, '请先选择批量目录输入。')
            return
        rows = calculate_directory_threshold_metrics(self.vmre_dir, self.label_dir, self.sadc_dir, self._threshold())
        export_rows_to_excel(rows, self.output_edit.text())
        show_info(self, f'批量结果已导出到 {self.output_edit.text()}')

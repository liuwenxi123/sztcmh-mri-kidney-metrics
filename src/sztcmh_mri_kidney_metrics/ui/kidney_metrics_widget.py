from __future__ import annotations

from PyQt5.QtWidgets import QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QVBoxLayout, QWidget

from sztcmh_mri_kidney_metrics.services.export_service import export_rows_to_excel
from sztcmh_mri_kidney_metrics.services.metric_workflows import calculate_batch_metric_rows, calculate_batch_middle_slice_rows, calculate_single_pair_metrics
from sztcmh_mri_kidney_metrics.ui.shared import pick_directory, pick_file, short_display, show_error, show_info


class KidneyMetricsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.image_file = ''
        self.label_file = ''
        self.image_dir = ''
        self.label_dir = ''
        self.last_summary = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        group = QGroupBox('肾脏像素统计')
        group_layout = QVBoxLayout(group)
        self.image_label = QLabel('')
        self.label_label = QLabel('')
        self.image_dir_label = QLabel('')
        self.label_dir_label = QLabel('')
        self.output_edit = QLineEdit('result.xlsx')
        rows = [
            ('图像文件:', self.image_label, self._choose_image),
            ('标签文件:', self.label_label, self._choose_label),
            ('图像目录:', self.image_dir_label, self._choose_image_dir),
            ('标签目录:', self.label_dir_label, self._choose_label_dir),
        ]
        for title, label, handler in rows:
            row = QHBoxLayout()
            row.addWidget(QLabel(title))
            row.addWidget(label)
            button = QPushButton('选择')
            button.clicked.connect(handler)
            row.addWidget(button)
            group_layout.addLayout(row)
        self.single_mode = QRadioButton('单独计算')
        self.batch_mode = QRadioButton('批量整层导出')
        self.middle_mode = QRadioButton('批量中层导出')
        self.single_mode.setChecked(True)
        mode_row = QHBoxLayout()
        mode_row.addWidget(self.single_mode)
        mode_row.addWidget(self.batch_mode)
        mode_row.addWidget(self.middle_mode)
        group_layout.addLayout(mode_row)
        result_form = QFormLayout()
        self.all_mean_label = QLabel('-')
        self.left_mean_label = QLabel('-')
        self.right_mean_label = QLabel('-')
        self.all_volume_label = QLabel('-')
        self.left_volume_label = QLabel('-')
        self.right_volume_label = QLabel('-')
        result_form.addRow('全肾均值:', self.all_mean_label)
        result_form.addRow('左肾均值:', self.left_mean_label)
        result_form.addRow('右肾均值:', self.right_mean_label)
        result_form.addRow('全肾体素数:', self.all_volume_label)
        result_form.addRow('左肾体素数:', self.left_volume_label)
        result_form.addRow('右肾体素数:', self.right_volume_label)
        result_form.addRow('导出文件名:', self.output_edit)
        group_layout.addLayout(result_form)
        button_row = QHBoxLayout()
        calculate_button = QPushButton('执行')
        calculate_button.clicked.connect(self._run)
        export_button = QPushButton('导出当前结果')
        export_button.clicked.connect(self._export_current)
        button_row.addWidget(calculate_button)
        button_row.addWidget(export_button)
        group_layout.addLayout(button_row)
        layout.addWidget(group)

    def _choose_image(self):
        self.image_file = pick_file(self, '选择图像文件')
        self.image_label.setText(short_display(self.image_file))

    def _choose_label(self):
        self.label_file = pick_file(self, '选择标签文件')
        self.label_label.setText(short_display(self.label_file))

    def _choose_image_dir(self):
        self.image_dir = pick_directory(self, '选择图像目录')
        self.image_dir_label.setText(short_display(self.image_dir))

    def _choose_label_dir(self):
        self.label_dir = pick_directory(self, '选择标签目录')
        self.label_dir_label.setText(short_display(self.label_dir))

    def _run(self):
        try:
            if self.single_mode.isChecked():
                if not self.image_file or not self.label_file:
                    show_error(self, '请先选择图像和标签文件。')
                    return
                self.last_summary = calculate_single_pair_metrics(self.image_file, self.label_file)
                self.all_mean_label.setText(str(self.last_summary.all_region.mean))
                self.left_mean_label.setText(str(self.last_summary.left_region.mean))
                self.right_mean_label.setText(str(self.last_summary.right_region.mean))
                self.all_volume_label.setText(str(self.last_summary.all_region.volume))
                self.left_volume_label.setText(str(self.last_summary.left_region.volume))
                self.right_volume_label.setText(str(self.last_summary.right_region.volume))
                show_info(self, '单文件计算完成。')
                return
            if not self.image_dir or not self.label_dir:
                show_error(self, '请先选择图像目录和标签目录。')
                return
            rows = calculate_batch_metric_rows(self.image_dir, self.label_dir) if self.batch_mode.isChecked() else calculate_batch_middle_slice_rows(self.image_dir, self.label_dir)
            export_rows_to_excel(rows, self.output_edit.text())
            show_info(self, f'批量结果已导出到 {self.output_edit.text()}')
        except Exception as exc:
            show_error(self, str(exc))

    def _export_current(self):
        if self.last_summary is None:
            show_error(self, '当前没有可导出的单文件结果。')
            return
        rows = [{'PatientID': self.image_label.text(), 'All Mean': self.last_summary.all_region.mean, 'Left Mean': self.last_summary.left_region.mean, 'Right Mean': self.last_summary.right_region.mean, 'All Volume': self.last_summary.all_region.volume, 'Left Volume': self.last_summary.left_region.volume, 'Right Volume': self.last_summary.right_region.volume}]
        export_rows_to_excel(rows, self.output_edit.text())
        show_info(self, f'当前结果已导出到 {self.output_edit.text()}')

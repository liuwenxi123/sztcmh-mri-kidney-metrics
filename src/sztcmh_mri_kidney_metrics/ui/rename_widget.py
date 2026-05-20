from __future__ import annotations

from PyQt5.QtWidgets import QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from sztcmh_mri_kidney_metrics.services.rename_service import apply_rename_plan, build_rename_plan
from sztcmh_mri_kidney_metrics.ui.shared import pick_directory, short_display, show_error, show_info


class RenameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.directory = ''
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        group = QGroupBox('批量改名')
        group_layout = QVBoxLayout(group)
        self.path_label = QLabel('')
        choose_button = QPushButton('选择目录')
        choose_button.clicked.connect(self._choose_directory)
        path_row = QHBoxLayout()
        path_row.addWidget(QLabel('目标目录:'))
        path_row.addWidget(self.path_label)
        path_row.addWidget(choose_button)
        self.original_edit = QLineEdit()
        self.replace_edit = QLineEdit()
        form = QFormLayout()
        form.addRow('原始 key:', self.original_edit)
        form.addRow('替换 key:', self.replace_edit)
        run_button = QPushButton('执行改名')
        run_button.clicked.connect(self._run)
        group_layout.addLayout(path_row)
        group_layout.addLayout(form)
        group_layout.addWidget(run_button)
        layout.addWidget(group)

    def _choose_directory(self):
        self.directory = pick_directory(self, '选择改名目录')
        self.path_label.setText(short_display(self.directory))

    def _run(self):
        if not self.directory:
            show_error(self, '请先选择目录。')
            return
        plan = build_rename_plan(self.directory, self.original_edit.text(), self.replace_edit.text())
        apply_rename_plan(plan)
        show_info(self, f'改名完成，共处理 {len(plan)} 个文件。')

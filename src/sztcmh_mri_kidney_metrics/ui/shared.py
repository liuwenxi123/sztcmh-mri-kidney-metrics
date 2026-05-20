from __future__ import annotations

from pathlib import Path

from PyQt5.QtWidgets import QFileDialog, QMessageBox


def pick_file(parent, title: str) -> str:
    path, _ = QFileDialog.getOpenFileName(parent, title, '', 'NIfTI Files (*.nii *.nii.gz);;All Files (*)')
    return path


def pick_directory(parent, title: str) -> str:
    return QFileDialog.getExistingDirectory(parent, title)


def short_display(path: str) -> str:
    if not path:
        return ''
    value = Path(path)
    if value.parent == value:
        return str(value)
    return str(Path(value.parent.name) / value.name)


def show_info(parent, text: str) -> None:
    QMessageBox.information(parent, '提示', text)


def show_error(parent, text: str) -> None:
    QMessageBox.critical(parent, '错误', text)

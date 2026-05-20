from __future__ import annotations

from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QWidget

from sztcmh_mri_kidney_metrics.ui.file_extraction_widget import FileExtractionWidget
from sztcmh_mri_kidney_metrics.ui.kidney_metrics_widget import KidneyMetricsWidget
from sztcmh_mri_kidney_metrics.ui.nifti_conversion_widget import NiftiConversionWidget
from sztcmh_mri_kidney_metrics.ui.rename_widget import RenameWidget
from sztcmh_mri_kidney_metrics.ui.vmre_sadc_widget import VmreSadcWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('sztcmh-mri-kidney-metrics')
        self.resize(1100, 760)
        self._build_ui()

    def _build_ui(self):
        central = QWidget(self)
        self.setCentralWidget(central)
        navigation = QVBoxLayout()
        stack = QStackedWidget()
        pages = [('文件抓取', FileExtractionWidget()), ('像素统计', KidneyMetricsWidget()), ('批量改名', RenameWidget()), ('NIfTI 转换', NiftiConversionWidget()), ('vMRE-sADC', VmreSadcWidget())]
        for index, (label, widget) in enumerate(pages):
            button = QPushButton(label)
            button.clicked.connect(lambda _checked=False, value=index: stack.setCurrentIndex(value))
            navigation.addWidget(button)
            stack.addWidget(widget)
        navigation.addStretch(1)
        layout = QHBoxLayout(central)
        nav_widget = QWidget()
        nav_widget.setLayout(navigation)
        layout.addWidget(nav_widget)
        layout.addWidget(stack, 1)

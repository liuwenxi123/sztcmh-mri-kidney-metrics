from __future__ import annotations

import sys

from PyQt5.QtWidgets import QApplication

from sztcmh_mri_kidney_metrics.app.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == '__main__':
    raise SystemExit(main())

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from FileFetch_Widget import FileFetch_Widget
from PixelCalculater_Widget import PixelCalculater_Widget
from Rename_Widget import Rename_Widget
from ConvNII_Widget import ConvNII_Widget
from vMREsADC_Widget import vMREsADC_Widget

class PixelCalculater(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.folder_path1 = None
        self.folder_path2 = None
        self.selected_file1 = None
        self.selected_file2 = None
        self.base_name1 = None
        self.left_kidney_mean = None
        self.right_kidney_mean = None
        self.overlap_mean = None

    def init_ui(self):
        # 设置窗口属性
        self.setWindowTitle('像素均值计算器')
        self.setGeometry(300, 300, 400, 300)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        icon_path = '黑暗派蒙.jpg'  # 替换为您的图标文件路径
        self.setWindowIcon(QIcon(icon_path))

        FileFecthWidget = FileFetch_Widget()
        PixelCalculaterWidget = PixelCalculater_Widget()
        RenameWidget = Rename_Widget()
        ConvNIIWidget = ConvNII_Widget()
        vMREsADCWidget = vMREsADC_Widget()

        navigation_bar = QWidget()  # 导航栏
        navigation_bar.setStyleSheet("background-color: rgb(200, 200, 200);")
        # navigation_bar.setFixedHeight(50)
        button_FetchFile = QPushButton('文件抓取')
        button_PixelCalculater = QPushButton('数值计算')
        button_Rename = QPushButton('文件改名')
        button_ConvNii = QPushButton('NII转换')
        button_vMREsADC = QPushButton('vMRE-sADC')
        spacer_item = QSpacerItem(30, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        button_layout = QVBoxLayout(navigation_bar)
        button_layout.addWidget(button_FetchFile)
        button_layout.addWidget(button_PixelCalculater)
        button_layout.addWidget(button_Rename)
        button_layout.addWidget(button_ConvNii)
        button_layout.addWidget(button_vMREsADC)
        button_layout.addItem(spacer_item)

        function_zone = QStackedWidget()
        function_zone.addWidget(FileFecthWidget)
        function_zone.addWidget(PixelCalculaterWidget)
        function_zone.addWidget(RenameWidget)
        function_zone.addWidget(ConvNIIWidget)
        function_zone.addWidget(vMREsADCWidget)

        layout = QHBoxLayout(central_widget)
        layout.addWidget(navigation_bar)
        layout.addWidget(function_zone)

        button_FetchFile.clicked.connect(lambda: function_zone.setCurrentIndex(0))
        button_PixelCalculater.clicked.connect(lambda: function_zone.setCurrentIndex(1))
        button_Rename.clicked.connect(lambda: function_zone.setCurrentIndex(2))
        button_ConvNii.clicked.connect(lambda: function_zone.setCurrentIndex(3))
        button_vMREsADC.clicked.connect(lambda: function_zone.setCurrentIndex(4))


        # self.filebt_toggled()

        # 显示窗口
        self.show()




class HorizontalLayoutWidget(QWidget):
    def __init__(self, labels, values):
        super().__init__()

        self.title = QLabel(labels)
        self.value = QLabel(values)
        layout = QHBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PixelCalculater()
    sys.exit(app.exec_())

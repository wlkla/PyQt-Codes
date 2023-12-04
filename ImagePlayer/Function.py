import os
import json
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QFileDialog, QLabel, QMessageBox, QListWidget, QListWidgetItem, QDialog, QVBoxLayout, \
    QProgressDialog, QApplication
from Entrance import mainwindow


class Controller:
    def __init__(self):
        super().__init__()
        self.InitUi()
        self.InitParameter()
        self.InitFunction()

    def InitUi(self):
        self.ui = mainwindow()
        self.ui.show()
        self.ui.horizontalSlider.hide()
        self.ui.resized.connect(self.handleResizeEvent)

    def InitParameter(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.play)
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.Carousel)
        self.image_index = 0
        self.labels = []

    def InitFunction(self):
        self.ui.pushButton.clicked.connect(self.selectFolder)
        self.ui.pushButton_2.clicked.connect(self.timerStart)
        self.ui.pushButton_3.clicked.connect(self.clear)
        self.ui.pushButton_4.clicked.connect(self.history)
        self.ui.pushButton_5.clicked.connect(self.feedback)
        self.ui.horizontalSlider.valueChanged.connect(self.play_timer.stop)

    def selectFolder(self):
        folder = QFileDialog.getExistingDirectory(self.ui, '选择文件夹', 'E:\Picture Files')
        if folder:
            self.ui.lineEdit.setText(folder)
            self.image_folder = folder
            self.image = [os.path.join(self.image_folder, file) for file in os.listdir(self.image_folder) if
                          file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
            self.timer.start(2)

            history = []
            history_file = 'history.json'
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history = json.load(f)
            history.append(folder)
            with open(history_file, 'w') as f:
                json.dump(history, f)

    def play(self):
        progress_dialog = QProgressDialog("正在加载图片...", "取消", 0, len(self.image), self.ui)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        for self.image_index in range(len(self.image)):
            if progress_dialog.wasCanceled():
                break

            height = int((self.ui.height() - 170))
            label = QLabel()
            label.setScaledContents(True)
            picture = QPixmap(self.image[self.image_index])
            label.setPixmap(picture)
            label.setStyleSheet("QLabel{\n"
                                "border:15px solid white;\n"
                                "border-radius:10px;\n"
                                "}\n"
                                "QLabel:hover{\n"
                                "border:15px solid black;\n"
                                "border-radius:10px;\n"
                                "}")
            label.setFixedSize(int(picture.width() * (height / picture.height())), height)
            self.ui.horizontalLayout_5.addWidget(label)
            self.labels.append(label)

            progress_dialog.setValue(self.image_index + 1)
            QApplication.processEvents()

        if self.image_index == len(self.image) - 1:
            QMessageBox.information(self.ui, '完成', '图片读取完成！')
            self.timer.stop()

    def handleResizeEvent(self):
        height = int((self.ui.height() - 170))
        for label in self.labels:
            picture = label.pixmap()
            label.setFixedSize(int(picture.width() * (height / picture.height())), height)

    def timerStart(self):
        if self.play_timer.isActive():
            self.play_timer.stop()
            self.ui.horizontalSlider.hide()
        else:
            self.ui.horizontalSlider.show()
            self.play_timer.start(3)

    def Carousel(self):
        bar = self.ui.scrollArea.horizontalScrollBar()
        bar.setSliderPosition(bar.sliderPosition() + int(self.ui.horizontalSlider.value() * 0.1) + 1)

    def clear(self):
        self.ui.lineEdit.clear()
        for label in self.labels:
            self.ui.horizontalLayout_5.removeWidget(label)
            label.deleteLater()
        self.labels.clear()
        self.image.clear()
        self.image_index = 0

    def history(self):
        # 从文件中读取历史记录
        history = []
        history_file = 'history.json'
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)

        # 创建一个新的窗口来显示历史记录
        dialog = QDialog(self.ui)
        dialog.setWindowTitle('历史记录')
        layout = QVBoxLayout(dialog)

        list_widget = QListWidget(dialog)
        for folder in history:
            item = QListWidgetItem(folder)
            list_widget.addItem(item)
        list_widget.itemDoubleClicked.connect(self.useFolder)

        layout.addWidget(list_widget)
        dialog.setLayout(layout)
        dialog.exec_()

    def useFolder(self, item):
        folder = item.text()
        self.ui.lineEdit.setText(folder)
        self.image_folder = folder
        self.image = [os.path.join(self.image_folder, file) for file in os.listdir(self.image_folder) if
                      file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
        self.timer.start(2)
        item.listWidget().window().close()

    def feedback(self):
        pass

    def seecode(self):
        pass
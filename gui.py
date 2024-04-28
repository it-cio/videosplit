import os
import sys
import threading

import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QProgressBar, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QMessageBox, QMainWindow, QApplication

from main import Divider


class VideoMixer(QWidget):
    def __init__(self):
        super().__init__()

        # self.video_path = ""
        self.video_race = ""
        self.video_pilot = ""
        self.music_path = "D:/Divider/data/music/"
        self.logo_path = "D:/Divider/data/logo/logo.png"
        self.end_logo_path = "D:/Divider/data/logo/last.jpg"
        self.save_path = ""
        self.temp_path = "D:/Divider/data/temp/"
        self.video_length = 57
        self.cut_length = 3

        self.input_frame = QLabel()
        self.input_frame.setMinimumSize(600, 350)
        h_box = QHBoxLayout()
        h_box.addStretch()

        # self.input_video_path = QPushButton("Исходники")
        # self.input_video_path.clicked.connect(self.get_video_path)
        # h_box.addWidget(self.input_video_path)
        # h_box.addStretch()

        self.input_video_race = QPushButton("Трасса")
        self.input_video_race.clicked.connect(self.get_video_race)
        h_box.addWidget(self.input_video_race)
        h_box.addStretch()

        self.input_video_pilot = QPushButton("Пилот")
        self.input_video_pilot.clicked.connect(self.get_video_pilot)
        h_box.addWidget(self.input_video_pilot)
        h_box.addStretch()

        self.input_progress = QProgressBar()
        self.input_progress.setMaximum(100)
        h_box.addWidget(self.input_progress)
        h_box.addStretch()

        self.input_cut = QPushButton("Старт 🏁")
        self.input_cut.clicked.connect(self.cut)
        h_box.addWidget(self.input_cut)
        h_box.addStretch()

        v_box = QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(self.input_frame)
        v_box.addStretch()
        v_box.addLayout(h_box)
        v_box.addStretch()
        self.setLayout(v_box)

    # def get_video_path(self):
    #     self.video_path = QFileDialog.
    #     getExistingDirectory(self, "Выберите папку с исходниками", os.getenv("HOME", '/GoPro'))
    #     if self.video_path != "":
    #         self.input_video_path.setText(self.video_path.split("/")[-1])
    #         self.save_path = f"{self.video_path}/SiriusAutodrom.mp4"

    def get_video_race(self):
        self.video_race = QFileDialog.getOpenFileName(self, "Select Video File", os.getenv("HOME", '/YandexDisk/GoPro'),
                                                      "Video files (*.mp4 *.avi *.wmv *.mov *.mkv)")[0]
        if self.video_race != "":
            self.input_video_race.setText(self.video_race.split("/")[-1])

    def get_video_pilot(self):
        self.video_pilot = QFileDialog.getOpenFileName(self, "Select Video File", os.getenv("HOME", '/YandexDisk/GoPro'),
                                                       "Video files (*.mp4 *.avi *.wmv *.mov *.mkv)")[0]
        if self.video_pilot != "":
            self.input_video_pilot.setText(self.video_pilot.split("/")[-1])

    def cut(self):
        if (self.video_race.split(f"{self.video_race.split('/')[-1]}")[0] ==
                self.video_pilot.split(f"{self.video_pilot.split('/')[-1]}")[0]):
            self.save_path = self.video_race.split(f"{self.video_race.split('/')[-1]}")[0] + "SiriusAutodrom.mp4"
        else:
            QMessageBox.about(self, "Info", "Видео трассы и пилотов из разных заездов!")

        if (self.video_race != ""
                and self.video_pilot != ""
                and self.music_path != ""
                and self.logo_path != ""
                and self.end_logo_path != ""
                and self.save_path != ""
                and self.temp_path != ""):
            # and self.input_video_length.value() > 0
            # and self.input_cut_length.value() > 0):

            # if self.save_path.split(".")[-1].lower() != "mp4":
            #     self.save_path = self.save_path + ".mp4"

            cutter = threading.Thread(target=StartProgress, args=(
                self.video_race,
                self.video_pilot,
                self.music_path,
                self.logo_path,
                self.end_logo_path,
                self.save_path,
                self.temp_path,
                self.video_length,
                self.cut_length))

            cutter.start()
            self.input_cut.setEnabled(False)
            self.input_progress.setValue(0)
            self.input_progress.resetFormat()

        else:
            QMessageBox.about(self, "Info", "Не выбраны видео трассы или пилота!")

    def open_video_box(self):
        button_reply = QMessageBox.question(self, "Operation Complete", "Do you want to open the video clip?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if button_reply == QMessageBox.Yes:
            os.startfile(self.save_path)

    def not_available(self):
        QMessageBox.about(self, "Information!", "Not Available Now...")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = VideoMixer()
        self.setCentralWidget(self.window)
        self.setWindowTitle("Видео-миксер")
        self.show()


class StartProgress(Divider):
    def display_progress(self):
        super().display_progress()
        main_window.window.input_progress.setValue(self.progress)
        frame = self.frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixel_map = QPixmap.fromImage(img)
        pixel_map = pixel_map.scaled(600, 338, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        main_window.window.input_frame.setPixmap(pixel_map)

    def video_processing(self):
        main_window.window.input_progress.setFormat("Обработка...")
        super().video_processing()

    def run_operations(self):
        super().run_operations()
        main_window.window.input_progress.setFormat("Завершено")
        main_window.window.open_video_box()
        main_window.window.input_cut.setEnabled(True)


app = QApplication(sys.argv)

app.setStyle("Fusion")


def create_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(50, 50, 50))
    palette.setColor(QPalette.WindowText, Qt.darkGray)
    palette.setColor(QPalette.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.AlternateBase, QColor(50, 50, 50))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(50, 50, 50))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(40, 130, 220))
    palette.setColor(QPalette.Highlight, QColor(40, 130, 220))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    return palette


app.setPalette(create_palette())
main_window = MainWindow()
sys.exit(app.exec_())

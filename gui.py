import os
import sys
import threading

import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QDoubleSpinBox, QProgressBar, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QMessageBox, QMainWindow, QApplication

from main import Divider


class VideoMixer(QWidget):
    def __init__(self):
        super().__init__()

        self.video_path = ""
        self.music_path = ""
        self.logo_path = ""
        self.save_path = ""

        self.input_frame = QLabel()
        self.input_frame.setMinimumSize(600, 400)
        v_box = QVBoxLayout()
        v_box.addStretch()

        v_box.addWidget(QLabel("Video file:"))
        self.input_video_path = QPushButton("Select Video File")
        self.input_video_path.clicked.connect(self.get_video_path)
        v_box.addWidget(self.input_video_path)
        v_box.addStretch()

        v_box.addWidget(QLabel("Test file:"))
        self.input_test_path = QPushButton("Select test File")
        self.input_test_path.clicked.connect(self.not_available)
        v_box.addWidget(self.input_test_path)
        v_box.addStretch()

        v_box.addWidget(QLabel("Music file:"))
        self.input_music_path = QPushButton("Select Music File")
        self.input_music_path.clicked.connect(self.get_music_path)
        v_box.addWidget(self.input_music_path)
        v_box.addStretch()

        v_box.addWidget(QLabel("Logo file:"))
        self.input_logo_path = QPushButton("Select Logo File")
        self.input_logo_path.clicked.connect(self.get_logo_path)
        v_box.addWidget(self.input_logo_path)
        v_box.addStretch()

        v_box.addWidget(QLabel("Save location:"))
        self.input_save_path = QPushButton("Select Save Location")
        self.input_save_path.clicked.connect(self.get_save_path)
        v_box.addWidget(self.input_save_path)
        v_box.addStretch()

        v_box.addWidget(QLabel("Video length(sec):"))
        self.input_video_length = QDoubleSpinBox()
        self.input_video_length.setDecimals(1)
        self.input_video_length.setMaximum(86400)
        self.input_video_length.valueChanged.connect(self.check_cut_length_value)
        v_box.addWidget(self.input_video_length)
        v_box.addStretch()

        v_box.addWidget(QLabel("Cut length(sec):"))
        self.input_cut_length = QDoubleSpinBox()
        self.input_cut_length.setDecimals(1)
        self.input_cut_length.setMaximum(86400)
        self.input_cut_length.valueChanged.connect(self.check_cut_length_value)
        v_box.addWidget(self.input_cut_length)
        v_box.addStretch()

        self.input_progress = QProgressBar()
        self.input_progress.setMaximum(100)
        v_box.addWidget(self.input_progress)
        v_box.addStretch()

        self.input_cut = QPushButton("Start 🏁")
        self.input_cut.clicked.connect(self.cut)
        v_box.addWidget(self.input_cut)
        v_box.addStretch()

        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.input_frame)
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()
        self.setLayout(h_box)

    def check_cut_length_value(self):
        if self.input_cut_length.value() > self.input_video_length.value():
            self.input_cut_length.setValue(self.input_video_length.value())

    def get_video_path(self):
        self.video_path = QFileDialog.getOpenFileName(self, "Select Video File", os.getenv("HOME"),
                                                      "Video files (*.mp4 *.avi *.wmv *.mov *.mkv)")[0]
        if self.video_path != "":
            self.input_video_path.setText(self.video_path.split("/")[-1])

    def get_music_path(self):
        self.music_path = QFileDialog.getOpenFileName(self, "Select Music File", os.getenv("HOME"),
                                                      "Audio files (*.mp3 *.wav *.ogg *.m4a)")[0]
        if self.music_path != "":
            self.input_music_path.setText(self.music_path.split("/")[-1])

    def get_logo_path(self):
        self.logo_path = QFileDialog.getOpenFileName(self, "Select Logo File", os.getenv("HOME"),
                                                     "Logo files (*.png)")[0]
        if self.logo_path != "":
            self.input_logo_path.setText(self.logo_path.split("/")[-1])

    def get_save_path(self):
        self.save_path = \
            QFileDialog.getSaveFileName(self, "Select Save File Path", os.getenv("HOME"), "Video files (*.mp4)")[0]

        if self.save_path != "":
            self.input_save_path.setText(self.save_path.split("/")[-1])

    def cut(self):
        if (self.video_path != ""
                and self.music_path != ""
                and self.logo_path != ""
                and self.save_path != ""
                and self.input_video_length.value() > 0
                and self.input_cut_length.value() > 0):

            if self.save_path.split(".")[-1].lower() != "mp4":
                self.save_path = self.save_path + ".mp4"

            cutter = threading.Thread(target=StartProgress, args=(
                self.video_path,
                self.music_path,
                self.logo_path,
                self.save_path,
                self.input_video_length.value(),
                self.input_cut_length.value()))

            cutter.start()
            self.input_cut.setEnabled(False)
            self.input_progress.setValue(0)
            self.input_progress.resetFormat()

        else:
            QMessageBox.about(self, "Info", "Not all parameters are set")

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
        self.setWindowTitle("Kart Video Mixer")
        self.show()


class StartProgress(Divider):
    def display_progress(self):
        super().display_progress()
        main_window.window.input_progress.setValue(self.progress)
        frame = self.frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixel_map = QPixmap.fromImage(img)
        pixel_map = pixel_map.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        main_window.window.input_frame.setPixmap(pixel_map)

    def add_music(self):
        main_window.window.input_progress.setFormat("Adding music...")
        super().add_music()

    def add_logo(self):
        main_window.window.input_progress.setFormat("Adding logo...")
        super().add_logo()

    def run_operations(self):
        super().run_operations()
        main_window.window.input_progress.setFormat("Completed")
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

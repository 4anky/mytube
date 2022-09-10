from collections import namedtuple
from pathlib import Path

from PyQt6.QtWidgets import (
    QComboBox, QFileDialog, QLineEdit, QPushButton, QWidget
)
from pytube import YouTube
from pytube.exceptions import RegexMatchError


class Sizes:
    __sizes = namedtuple("sizes", "width height")

    main_window = __sizes(640, 240)
    url_line = __sizes(500, 30)
    info_btn = __sizes(80, 30)
    qualities_box = __sizes(300, 30)
    file_dialog = __sizes(100, 30)
    path_line = __sizes(450, 30)
    path_btn = __sizes(130, 30)
    download_btn = __sizes(600, 90)


class MyTubeWindow(QWidget):
    def __init__(self, version: str):
        super().__init__()

        self._version = version

        self.setWindowTitle(f"Загрузка видео с YouTube [v. {self._version}]")
        self.setFixedSize(
            Sizes.main_window.width,
            Sizes.main_window.height
        )

        self.url_line = self.__place_line_edit()

        self.info_btn = self.__place_info_btn()
        self.info_btn.clicked.connect(self.get_video_versions_info)

        self.qualities_box = self.__place_combo_box()

        self.path_line = self.__place_path_line()
        self.path_btn = self.__place_path_btn()
        self.path_btn.clicked.connect(self.open_dir_dialog)

        self.download_btn = self.__place_download_btn()
        self.download_btn.clicked.connect(self.download_video)

        self.qualities = None

    def __place_line_edit(self):
        url_line = QLineEdit("", self)
        url_line.setPlaceholderText("Вставьте сюда ссылку на видео...")
        url_line.resize(
            Sizes.url_line.width,
            Sizes.url_line.height
        )
        url_line.move(20, 20)
        return url_line

    def __place_info_btn(self):
        info_btn = QPushButton("Инфо", self)
        info_btn.resize(
            Sizes.info_btn.width,
            Sizes.info_btn.height
        )
        info_btn.move(
            Sizes.url_line.width + 20 * 2,
            20
        )
        return info_btn

    def __place_combo_box(self):
        qualities_box = QComboBox(self)
        qualities_box.setPlaceholderText("Выберите качество...")
        qualities_box.resize(
            Sizes.qualities_box.width,
            Sizes.qualities_box.height
        )
        qualities_box.move(
            10,
            Sizes.url_line.height + 30
        )
        return qualities_box

    def __place_path_line(self):
        path_line = QLineEdit(str(Path.home()), self)
        path_line.resize(
            Sizes.path_line.width,
            Sizes.path_line.height
        )
        path_line.move(
            20,
            Sizes.url_line.height + Sizes.qualities_box.height + 40
        )
        return path_line

    def __place_path_btn(self):
        info_btn = QPushButton("Выбрать папку ...", self)
        info_btn.resize(
            Sizes.path_btn.width,
            Sizes.path_btn.height
        )
        info_btn.move(
            Sizes.path_line.width + 20 * 2,
            Sizes.url_line.height + Sizes.qualities_box.height + 40
        )
        return info_btn

    def __place_download_btn(self):
        download_btn = QPushButton("Загрузить видео!", self)
        download_btn.resize(
            Sizes.download_btn.width,
            Sizes.download_btn.height
        )
        download_btn.move(
            20,
            Sizes.url_line.height + Sizes.qualities_box.height + 80
        )
        return download_btn

    def open_dir_dialog(self):
        path_to_save = QFileDialog.getExistingDirectory(
            self,
            "Сохранить в ...",
            str(Path.home())
        )
        self.path_line.setText(path_to_save)

    def get_video_versions_info(self) -> YouTube.streams:
        try:
            yt = YouTube(self.url_line.text())
        except RegexMatchError:
            print("Введён некорректный адрес видео")
            return
        else:
            videos = yt.streams.filter(
                type="video",
                progressive=True
            ).order_by(
                attribute_name="resolution"
            ).desc()

        self.qualities = {(
            f"  {video.mime_type} | {video.resolution} | "
            f"{video.fps} fps | {round(video.filesize / 1_000_000, 1)} Mb"
        ): video for video in videos}
        self.qualities_box.clear()
        self.qualities_box.addItems(self.qualities)

    def download_video(self):
        quality = self.qualities_box.currentText()
        path_to_save = self.path_line.text()

        required_stream = self.qualities[quality]
        required_stream.download(
            output_path=path_to_save,
        )

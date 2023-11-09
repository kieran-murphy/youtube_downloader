import sys
import os
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QFont


class MyApplication(QApplication):
    def applicationSupportsSecureRestorableState(self):
        return True


def download_audio(url, path):
    yt = YouTube(url)

    # Get the highest quality audio stream (typically in MP4 format)
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Download the audio stream
    audio_stream.download(output_path=path, filename="temp.mp4")

    # Load the downloaded audio
    audio = AudioFileClip(path + "temp.mp4")

    # Get the title of the YouTube video
    video_title = yt.title

    # Write the audio as an MP3 file with the video title as the filename
    audio.write_audiofile(path + video_title + ".mp3")

    # Remove the temporary MP4 file
    os.remove(path + "temp.mp4")


def log_text():
    text = text_input.text()
    download_audio(text, "downloads/")
    text_input.clear()  # Clear the text input


app = MyApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Youtube downloader")

central_widget = QWidget()
window.setCentralWidget(central_widget)

layout = QVBoxLayout()

# Create a label with better styling
label = QLabel("Enter video URL:")
label.setMargin(10)
layout.addWidget(label)

# Create a text input widget with the custom style
text_input = QLineEdit()
font = QFont()
font.setPointSize(12)
text_input.setFont(font)
layout.addWidget(text_input)

# Create a button with a different color and styling
log_button = QPushButton("Download")
font = QFont()
font.setPointSize(12)
log_button.setFont(font)
log_button.setStyleSheet("background-color: green;")
log_button.clicked.connect(log_text)
layout.addWidget(log_button)

central_widget.setLayout(layout)

window.resize(400, 200)
window.show()

sys.exit(app.exec_())

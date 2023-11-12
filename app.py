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


def download_video(url, path):
    yt = YouTube(url)

    # Get the highest quality video-only stream
    video_stream = (
        yt.streams.filter(adaptive=True, file_extension="mp4", only_video=True)
        .order_by("resolution")
        .desc()
        .first()
    )

    # Get the highest quality audio stream
    audio_stream = yt.streams.filter(only_audio=True).order_by("abr").desc().first()

    # Download video and audio streams
    video_filename = video_stream.download(output_path=path, filename_prefix="video_")
    audio_filename = audio_stream.download(output_path=path, filename_prefix="audio_")

    # Load the downloaded video and audio
    video_clip = VideoFileClip(video_filename)
    audio_clip = AudioFileClip(audio_filename)

    # Set the audio of the video clip
    final_clip = video_clip.set_audio(audio_clip)

    # Write the final clip
    final_clip.write_videofile(path + yt.title + ".mp4")

    # Remove the temporary files
    os.remove(video_filename)
    os.remove(audio_filename)


def download_audio_action():
    sys.stdout = open(os.devnull, "w")
    text = text_input.text()
    download_audio(text, "downloads/")
    text_input.clear()  # Clear the text input
    sys.stdout = sys.__stdout__


def download_video_action():
    text = text_input.text()
    download_video(text, "downloads/")
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
log_button = QPushButton("Download Audio")
font = QFont()
font.setPointSize(12)
log_button.setFont(font)
log_button.setStyleSheet("background-color: green;")
log_button.clicked.connect(download_audio_action)
layout.addWidget(log_button)

download_video_button = QPushButton("Download Video")
download_video_button.setFont(font)
download_video_button.setStyleSheet("background-color: blue;")
download_video_button.clicked.connect(download_video_action)
layout.addWidget(download_video_button)

central_widget.setLayout(layout)

window.resize(400, 200)
window.show()


sys.exit(app.exec_())

from pytube import YouTube
from moviepy.editor import *


def download_audio(url, path):
    yt = YouTube(url)

    # Get the highest quality audio stream (typically in MP4 format)
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Download the audio stream
    audio_stream.download(output_path=path, filename="temp")

    # Convert the downloaded audio to MP3
    video = VideoFileClip(path + "temp.mp4")
    video.audio.write_audiofile(path + "output.mp3")

    # Remove the temporary MP4 file
    os.remove(path + "temp.mp4")


url = ""  # Replace this with your YouTube URL
download_path = "downloads"  # Replace this with your desired path
download_audio(url, download_path)

from moviepy.editor import *


def convert_to_mp3(video_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_path, codec="libmp3lame")
    audio_clip.close()
    video_clip.close()


video_file_path = "/Users/kieranmurphy/Documents/Python/youtube_downloader/New Seiko Nautilus MOD with leather strap automatic watch - Custom build.mp4"  # Replace with the path to your downloaded video
output_mp3_path = ""  # Replace with your desired output MP3 path
convert_to_mp3(video_file_path, output_mp3_path)

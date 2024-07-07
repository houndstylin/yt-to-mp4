from pytube import YouTube
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import logging
from proglog import ProgressBarLogger

class CustomLogger(ProgressBarLogger):
    def callback(self, **changes):
        pass

    def bars_callback(self, bar, attr, value, old_value=None):
        pass

def download_youtube_video(url, output_path='.', resolution='1080p'):
    
    yt = YouTube(url)

    
    video_stream = yt.streams.filter(res=resolution, mime_type="video/mp4").first()
    audio_stream = yt.streams.filter(only_audio=True, mime_type="audio/mp4").first()

    if not video_stream:
        raise Exception(f"No video stream found with resolution {resolution}")

    if not audio_stream:
        raise Exception("No audio stream found")

    video_path = os.path.join(output_path, "video.mp4")
    audio_path = os.path.join(output_path, "audio.mp4")
    output_file = os.path.join(output_path, f"{yt.title}.mp4")
 
    print("[/] Downloading video...")
    video_stream.download(output_path=output_path, filename="video.mp4")
    print("[/] Downloading audio...")
    audio_stream.download(output_path=output_path, filename="audio.mp4")

    print("[/] Merging video and audio...")
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_file, codec='libx264', logger=CustomLogger())

    os.remove(video_path)
    os.remove(audio_path)
    print(f"[+] Downloaded video!")

if __name__ == '__main__':
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_url = input("Enter the YouTube url: ")
    try:
        download_youtube_video(video_url, current_dir)
    except Exception as e:
        print(f"An error occurred: {e}")

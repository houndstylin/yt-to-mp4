import os
import logging
import warnings
from moviepy.editor import VideoFileClip, AudioFileClip
import yt_dlp as youtube_dl

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore", category=UserWarning, module='moviepy')

def download_youtube_video(url, output_path='.'):
    class MyLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            logger.error(msg)

    ydl_opts_video = {
        'format': 'bestvideo',
        'outtmpl': os.path.join(output_path, 'video.%(ext)s'),
        'logger': MyLogger(),
        'quiet': True
    }
    ydl_opts_audio = {
        'format': 'bestaudio',
        'outtmpl': os.path.join(output_path, 'audio.%(ext)s'),
        'logger': MyLogger(),
        'quiet': True
    }

    # download vid
    logger.info("[/] Downloading video...")
    with youtube_dl.YoutubeDL(ydl_opts_video) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_ext = info_dict['ext']

    # download aoudio
    logger.info("[/] Downloading audio...")
    with youtube_dl.YoutubeDL(ydl_opts_audio) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_ext = info_dict['ext']
        video_title = info_dict['title']

    video_path = os.path.join(output_path, f'video.{video_ext}')
    audio_path = os.path.join(output_path, f'audio.{audio_ext}')
    output_file = os.path.join(output_path, f"{video_title}.mp4")

    # merge
    logger.info("[/] Merging video and audio...")
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_file, codec='libx264', logger=None)
    os.remove(video_path)
    os.remove(audio_path)
    logger.info(f"[+] Downloaded '{video_title}' successfully!")

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_url = input("Enter the YouTube video URL: ")
    try:
        download_youtube_video(video_url, current_dir)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

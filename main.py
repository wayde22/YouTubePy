import os
import sys
from pathlib import Path
from timeit import default_timer as timer

try:
    from yt_dlp import DownloadError, YoutubeDL
except ImportError:
    print("Missing dependency: yt-dlp")
    print("Install it with: python -m pip install yt-dlp")
    sys.exit(1)


destination = Path("D:/Video Capture/Youtube Videos")

# Colors for the terminal
OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"


def clear_bash_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def get_download_options():
    destination.mkdir(parents=True, exist_ok=True)
    return {
        "format": "best[ext=mp4]/best",
        "noplaylist": True,
        "outtmpl": str(destination / "%(title)s.%(ext)s"),
        "quiet": True,
        "noprogress": True,
    }


def get_video_info(link):
    with YoutubeDL(get_download_options()) as ydl:
        return ydl.extract_info(link, download=False)


def download_video(link):
    try:
        info = get_video_info(link)
        title = info.get("title", "video")
        print(f'\nGetting {BOLD}{WARNING}"{title}"{ENDC} video...')
        print(f'Attempting to download {BOLD}{OKBLUE}"{title}"{ENDC}...\n')

        with YoutubeDL(get_download_options()) as ydl:
            ydl.download([link])

        end_timer = timer()
        print(
            f'{BOLD}{OKGREEN}"{title}"{ENDC} download completed successfully in '
            f"{end_timer - start_timer:.4f} seconds!"
        )
        print(f"Saved to: {destination}")
    except DownloadError as exc:
        print(f"{FAIL}Download failed:{ENDC} {exc}")
    except Exception as exc:
        print(f"{FAIL}An unexpected error occurred:{ENDC} {exc}")


if __name__ == "__main__":
    clear_bash_terminal()
    youtube_link = input("Enter the YouTube video URL: ").strip()
    start_timer = timer()
    download_video(youtube_link)

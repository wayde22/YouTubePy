import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from timeit import default_timer as timer

try:
    import yt_dlp  # noqa: F401
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


def can_reach_youtube(host="www.youtube.com", port=443, timeout=5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def wait_for_youtube_connection(attempts=3, delay_seconds=10):
    for attempt in range(1, attempts + 1):
        if can_reach_youtube():
            return True

        if attempt < attempts:
            print(
                f"{WARNING}Could not reach YouTube.{ENDC} "
                f"Retrying in {delay_seconds} seconds "
                f"({attempt}/{attempts})..."
            )
            time.sleep(delay_seconds)

    return False


def get_download_options():
    destination.mkdir(parents=True, exist_ok=True)
    return {
        "format": "best[ext=mp4]/best",
        "output": str(destination / "%(title)s.%(ext)s"),
    }


def build_yt_dlp_command(link):
    options = get_download_options()
    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--no-playlist",
        "--format",
        options["format"],
        "--output",
        options["output"],
    ]

    if shutil.which("node"):
        command.extend(["--js-runtimes", "node"])

    command.append(link)
    return command


def download_video(link):
    print(f"\n{BOLD}{WARNING}Starting download...{ENDC}\n")

    result = subprocess.run(build_yt_dlp_command(link), check=False)

    if result.returncode == 0:
        end_timer = timer()
        print(
            f"{BOLD}{OKGREEN}Download completed successfully{ENDC} in "
            f"{end_timer - start_timer:.4f} seconds!"
        )
        print(f"Saved to: {destination}")
        return

    print(
        f"{FAIL}Download failed.{ENDC} yt-dlp exited with status "
        f"{result.returncode}."
    )


if __name__ == "__main__":
    clear_bash_terminal()
    youtube_link = input("Enter the YouTube video URL: ").strip()
    if not wait_for_youtube_connection():
        print(
            f"{FAIL}Cannot reach YouTube right now.{ENDC} "
            "Checked 3 times over 30 seconds. Please check your internet or DNS "
            "connection and try again."
        )
        sys.exit(1)

    start_timer = timer()
    download_video(youtube_link)

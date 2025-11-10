import argparse
import logging
import os
import sys
from datetime import datetime
import yt_dlp
from colorama import init, Fore, Style
from io import StringIO
import contextlib

# Initialize colorama
init(autoreset=True)

class CustomFormatter(logging.Formatter):
    """Custom formatter to add colors and custom log levels."""
    LOG_SYMBOLS = {
        logging.INFO: f"{Fore.GREEN}[+]{Style.RESET_ALL}",
        logging.WARNING: f"{Fore.YELLOW}[*]{Style.RESET_ALL}",
        logging.ERROR: f"{Fore.RED}[-]{Style.RESET_ALL}",
    }

    def format(self, record):
        log_symbol = self.LOG_SYMBOLS.get(record.levelno, "")
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {log_symbol} {record.getMessage()}"

def setup_logging():
    """Sets up the logging configuration."""
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)

def progress_hook(d):
    """Progress hook for yt-dlp to display a custom progress bar."""
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes')
        if total_bytes and downloaded_bytes:
            percent = downloaded_bytes / total_bytes * 100
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)
            
            speed_str = f'{speed/1024/1024:.2f}MB/s' if speed else 'N/A'
            eta_str = f'{int(eta)}s' if eta else 'N/A'
            
            bar_length = 20
            filled_len = int(bar_length * downloaded_bytes // total_bytes)
            bar = '█' * filled_len + '-' * (bar_length - filled_len)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_symbol = f"{Fore.GREEN}[+]{Style.RESET_ALL}"
            
            sys.stdout.write(f'\r[{timestamp}] {log_symbol} Downloading: |{bar}| {percent:.1f}% at {speed_str}, ETA: {eta_str}  ')
            sys.stdout.flush()
    elif d['status'] == 'finished':
        sys.stdout.write('\n')

def download_video(url, save_path, format_code):
    """Downloads a video from a given URL."""
    logging.info(f"Starting video download for format '{format_code}'...")
    try:
        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.f%(format_id)s.%(ext)s'),
            'format': format_code,
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [progress_hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logging.info(f"Video download finished for format '{format_code}'.")
    except Exception as e:
        logging.error(f"Error downloading video for format '{format_code}': {e}")

def interactive_format_selection(url):
    """Allows the user to interactively select video formats to download."""
    logging.info("Fetching available video formats...")
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])

        video_formats = []
        for f in formats:
            if f.get('vcodec') != 'none':
                filesize = f.get('filesize') or f.get('filesize_approx')
                filesize_str = f"{filesize / (1024*1024):.2f}MB" if filesize else "N/A"
                resolution = f.get('resolution') or f"{f.get('width')}x{f.get('height')}"
                
                video_formats.append({
                    'id': f['format_id'],
                    'ext': f['ext'],
                    'resolution': resolution,
                    'filesize': filesize_str,
                    'note': f.get('format_note', ''),
                    'vcodec': f.get('vcodec'),
                    'acodec': f.get('acodec'),
                })

        if not video_formats:
            logging.error("No video formats found.")
            return []

        print("\nAvailable video formats:")
        for i, f in enumerate(video_formats):
            acodec_str = "" if f['acodec'] == 'none' else f"({f['acodec']})"
            print(f"  [{i+1}] {f['resolution']:<15} {f['ext']:<5} {f['filesize']:>10} {acodec_str} - {f['note']}")

        while True:
            try:
                choice_str = input("\nEnter the numbers of the formats to download (comma-separated), or 'q' to quit: ")
                if choice_str.lower() == 'q':
                    return []
                
                choices = [int(c.strip()) for c in choice_str.split(',')]
                selected_codes = [video_formats[choice-1]['id'] for choice in choices if 1 <= choice <= len(video_formats)]
                
                if len(selected_codes) != len(choices):
                    raise ValueError
                
                return selected_codes
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid input. Please enter numbers from the list.{Style.RESET_ALL}")

    except Exception as e:
        logging.error(f"Could not fetch formats: {e}")
        return []

def download_subtitle(url, save_path, langs, sub_format):
    """Downloads subtitles from a given URL."""
    logging.info(f"Starting subtitle download for language(s): {', '.join(langs)}...")
    try:
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': langs,
            'subtitlesformat': sub_format,
            'skip_download': True,
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logging.info("Subtitle download finished.")
    except Exception as e:
        logging.error(f"Error downloading subtitle: {e}")

def download_thumbnail(url, save_path):
    """Downloads a thumbnail from a given URL using yt-dlp."""
    logging.info("Starting thumbnail download...")
    try:
        ydl_opts = {
            'writethumbnail': True,
            'skip_download': True,
            'outtmpl': os.path.join(save_path, '%(title)s'),
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logging.info("Thumbnail download finished.")
    except Exception as e:
        logging.error(f"Error downloading thumbnail: {e}")

def list_formats(url):
    """Lists available formats for a given URL, ensuring all output is formatted."""
    logging.info("Listing available formats for the URL...")
    try:
        buffer_out = StringIO()
        buffer_err = StringIO()
        with contextlib.redirect_stdout(buffer_out), contextlib.redirect_stderr(buffer_err):
            with yt_dlp.YoutubeDL({'listformats': True}) as ydl:
                try:
                    ydl.download([url])
                except yt_dlp.utils.DownloadError:
                    pass
        
        output = buffer_out.getvalue()
        errors = buffer_err.getvalue()

        for line in errors.split('\n'):
            if line.strip() and 'WARNING' in line:
                logging.warning(line.replace('WARNING:', '').strip())

        for line in output.split('\n'):
            if line.strip() and ('[info]' in line or 'ID' in line or (line.strip() and line.strip()[0].isdigit())):
                cleaned_line = line.replace('[info]', '').strip()
                if cleaned_line:
                    logging.info(cleaned_line)
    except Exception as e:
        logging.error(f"Error listing formats: {e}")

def list_subtitles(url):
    """Lists available subtitles for a given URL, ensuring all output is formatted."""
    logging.info("Listing available subtitles for the URL...")
    try:
        buffer_out = StringIO()
        buffer_err = StringIO()
        with contextlib.redirect_stdout(buffer_out), contextlib.redirect_stderr(buffer_err):
            with yt_dlp.YoutubeDL({'listsubtitles': True}) as ydl:
                try:
                    ydl.download([url])
                except yt_dlp.utils.DownloadError:
                    pass
        
        output = buffer_out.getvalue()
        errors = buffer_err.getvalue()

        for line in errors.split('\n'):
            if line.strip() and 'WARNING' in line:
                logging.warning(line.replace('WARNING:', '').strip())

        for line in output.split('\n'):
            if line.strip() and ('[info]' in line or 'Language' in line):
                cleaned_line = line.replace('[info]', '').strip()
                if cleaned_line:
                    logging.info(cleaned_line)
    except Exception as e:
        logging.error(f"Error listing subtitles: {e}")

def download_playlist(url, save_path):
    """Handles the playlist download workflow."""
    logging.info("Fetching playlist videos...")
    try:
        ydl_opts = {'extract_flat': True, 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_dict = ydl.extract_info(url, download=False)
            entries = playlist_dict.get('entries', [])

        if not entries:
            logging.error("No videos found in the playlist.")
            return

        print("\nAvailable videos in the playlist:")
        for i, entry in enumerate(entries):
            print(f"  [{i+1}] {entry['title']}")

        while True:
            try:
                choice_str = input(f"\nEnter video numbers to download (e.g., 1-5,8,10), '0' for all, or 'q' to quit: ")
                if choice_str.lower() == 'q':
                    return

                if choice_str.strip() == '0':
                    selected_indices = range(len(entries))
                    break

                selected_indices = set()
                parts = choice_str.split(',')
                for part in parts:
                    part = part.strip()
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        for i in range(start, end + 1):
                            if 1 <= i <= len(entries):
                                selected_indices.add(i - 1)
                    else:
                        index = int(part)
                        if 1 <= index <= len(entries):
                            selected_indices.add(index - 1)
                
                if not selected_indices:
                    raise ValueError

                selected_indices = sorted(list(selected_indices))
                break
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid input. Please enter numbers from the list.{Style.RESET_ALL}")
        
        if not selected_indices:
            logging.warning("No videos selected.")
            return

        selected_videos = [entries[i] for i in selected_indices]
        
        # Use the first selected video to determine the format for all
        first_video_url = selected_videos[0]['url']
        logging.info(f"Fetching formats for the first selected video: {selected_videos[0]['title']}")
        selected_formats = interactive_format_selection(first_video_url)

        if not selected_formats:
            logging.warning("No format selected. Aborting playlist download.")
            return

        logging.info(f"Will download {len(selected_videos)} video(s) with format(s): {', '.join(selected_formats)}")

        for i, video in enumerate(selected_videos):
            logging.info(f"Downloading video {i+1} of {len(selected_videos)}: {video['title']}")
            for format_code in selected_formats:
                download_video(video['url'], save_path, format_code)

    except Exception as e:
        logging.error(f"An error occurred during playlist processing: {e}")


def main():
    """Main function to parse arguments and initiate downloads."""
    parser = argparse.ArgumentParser(description="YouTube Downloader", add_help=True)
    parser.add_argument("-u", "--url", required=True, help="YouTube video or playlist URL")
    parser.add_argument("--video", action="store_true", help="Download video")
    parser.add_argument("--playlist", action="store_true", help="Download videos from a playlist")
    parser.add_argument("--subtitle", action="store_true", help="Download subtitle")
    parser.add_argument("--thumbnail", action="store_true", help="Download thumbnail")
    parser.add_argument("--list-formats", action="store_true", help="List available video formats")
    parser.add_argument("--list-subs", action="store_true", help="List available subtitles")
    parser.add_argument("--save-dir", default=os.path.expanduser('~/Videos'), help="Directory to save files")
    parser.add_argument("--save-folder", help="Folder to save files in")
    parser.add_argument("--save-sub-lang", default="en", help="Subtitle language(s) to download (comma-separated)")
    parser.add_argument("--sub-style", default="srt", help="Subtitle format (e.g., srt, vtt)")
    parser.add_argument("--format", help="Video format code to download (skip for interactive selection)")

    args = parser.parse_args()

    setup_logging()

    logging.info(f"Checking url: {args.url}")

    save_path = os.path.join(args.save_dir, args.save_folder) if args.save_folder else args.save_dir
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        logging.info(f"Created directory: {save_path}")

    if args.list_formats:
        list_formats(args.url)
        return

    if args.list_subs:
        list_subtitles(args.url)
        return

    if args.playlist:
        download_playlist(args.url, save_path)
        return

    if not (args.video or args.subtitle or args.thumbnail):
        logging.warning("No download option selected. Use --video, --subtitle, or --thumbnail.")
        return

    if args.video:
        if args.format:
            download_video(args.url, save_path, args.format)
        else:
            selected_formats = interactive_format_selection(args.url)
            if selected_formats:
                for format_code in selected_formats:
                    download_video(args.url, save_path, format_code)
            else:
                logging.warning("No formats selected. Skipping video download.")

    if args.subtitle:
        langs = [lang.strip() for lang in args.save_sub_lang.split(',')]
        download_subtitle(args.url, save_path, langs, args.sub_style)

    if args.thumbnail:
        download_thumbnail(args.url, save_path)

if __name__ == "__main__":
    main()

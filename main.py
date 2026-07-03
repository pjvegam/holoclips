from datetime import datetime, timedelta
from config import Config
from channel_repository import ChannelRepository
from api_service import HolodexApiService
from clip_service import ClipService
from playlist_generator import PlaylistGenerator
import argparse
import logging
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Find top YouTube clips for specific channels")
    parser.add_argument("num_clips", type=int, nargs='?', default=5, help="Number of clips to include")
    parser.add_argument("-f", "--fecha", type=str, help="Date in format YYYY.MM.DD")
    parser.add_argument("-d", "--delay", type=int, help="Days ago")

    return parser.parse_args()

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    args = parse_args()

    if args.fecha:
        year, month, day = args.fecha.split(".")
        target_date = datetime(int(year), int(month), int(day))
    else:
        target_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=2)

    if args.delay:
        target_date = target_date - timedelta(days=args.delay)

    num_clips = args.num_clips

    api_key = Config.API_KEY1 if target_date.day % 2 == 0 else Config.API_KEY2

    channel_repo = ChannelRepository()
    api_service = HolodexApiService(api_key)
    clip_service = ClipService(api_service, channel_repo)
    playlist_generator = PlaylistGenerator()

    # Get clips and calculate metrics
    logging.info(f"Fetching clips for {target_date.date()}")
    clips = clip_service.fetch_clips_for_date(target_date)

    if not clips:
        logging.warning(f"No clips found for {target_date.date()}")
        return

    logging.info(f"Found {len(clips)} clips, fetching view counts...")
    clip_service.enrich_clips_with_views(clips)

    # Get top N clips
    top_clips = clip_service.get_top_clips(clips, num_clips)

    if not top_clips:
        logging.warning("No valid clips found after filtering")
        return

    # Generate playlist
    playlist_path = playlist_generator.create_playlist(top_clips)
    logging.info(f"Created playlist with {len(top_clips)} clips at {playlist_path}")

    # Open with mpv
    try:
        #subprocess.run(['mpv', playlist_path])
        os.system(f'mpv "{playlist_path}"')
    except Exception as e:
        logging.error(f"Failed to open mpv: {str(e)}")


if __name__ == "__main__":
    main()
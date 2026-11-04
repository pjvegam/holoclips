import argparse
import logging
import sys
from datetime import datetime, timedelta

from api_service import HolodexApiError, HolodexApiService
from channel_repository import ChannelRepository
from clip_service import ClipService
from config import Config
from output import open_in_browser, play_with_mpv, print_top_clips_table
from playlist_generator import PlaylistGenerator
from youtube_service import YouTubeApiError, YouTubeService


def parse_args():
    parser = argparse.ArgumentParser(description="Find top YouTube clips for specific channels")
    parser.add_argument(
        "num_clips", type=int, nargs="?", default=5, help="Number of clips to include"
    )
    parser.add_argument("-f", "--fecha", type=str, help="Date in format YYYY.MM.DD")
    parser.add_argument("-d", "--delay", type=int, help="Days ago")
    parser.add_argument(
        "--mpv",
        action="store_true",
        help="Reproducir el top con mpv en vez de abrirlo en el navegador",
    )

    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    args = parse_args()

    if args.fecha:
        year, month, day = args.fecha.split(".")
        target_date = datetime(int(year), int(month), int(day))
    else:
        target_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
            days=2
        )

    if args.delay:
        target_date = target_date - timedelta(days=args.delay)

    num_clips = args.num_clips

    if not Config.HOLODEX_API_KEY:
        logging.error("Falta HOLODEX_API_KEY en el .env")
        sys.exit(1)

    if not Config.YOUTUBE_API_KEY:
        logging.error("Falta YOUTUBE_API_KEY en el .env")
        sys.exit(1)

    channel_repo = ChannelRepository()
    api_service = HolodexApiService(Config.HOLODEX_API_KEY)
    youtube_service = YouTubeService(Config.YOUTUBE_API_KEY)
    clip_service = ClipService(api_service, channel_repo, youtube_service)
    playlist_generator = PlaylistGenerator()

    # Get clips and calculate metrics
    logging.info(f"Fetching clips for {target_date.date()}")
    try:
        clips = clip_service.fetch_clips_for_date(target_date)
    except HolodexApiError as e:
        logging.error(f"No se pudieron obtener los clips, no se genera el top: {e}")
        sys.exit(1)

    if not clips:
        logging.warning(f"No clips found for {target_date.date()}")
        return

    logging.info(f"Found {len(clips)} clips, fetching view counts...")
    try:
        clip_service.enrich_clips_with_views(clips)
    except YouTubeApiError as e:
        logging.error(f"No se pudieron obtener las vistas, no se genera el top: {e}")
        sys.exit(1)

    # Get top N clips
    top_clips = clip_service.get_top_clips(clips, num_clips)

    if not top_clips:
        logging.warning("No valid clips found after filtering")
        return

    # Mostrar la tabla del ranking antes de reproducir/abrir en el navegador
    print_top_clips_table(top_clips)

    # Generate playlist
    playlist_path = playlist_generator.create_playlist(top_clips)
    logging.info(f"Created playlist with {len(top_clips)} clips at {playlist_path}")

    # Con --mpv se reproduce el top con mpv. Por defecto se abren TODOS los top
    # clips en el navegador.
    # top_clips viene ordenado ascendente por score, asi que el mejor queda al final.
    if args.mpv:
        if not play_with_mpv(playlist_path):
            logging.error("No se encontró mpv en el PATH")
            sys.exit(1)
        return

    open_in_browser(top_clips)


if __name__ == "__main__":
    main()

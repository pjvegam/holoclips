from datetime import datetime, timedelta
from config import Config
from channel_repository import ChannelRepository
from api_service import HolodexApiService
from clip_service import ClipService
from playlist_generator import PlaylistGenerator
import argparse
import logging
import os
import time
import webbrowser

def parse_args():
    parser = argparse.ArgumentParser(description="Find top YouTube clips for specific channels")
    parser.add_argument("num_clips", type=int, nargs='?', default=5, help="Number of clips to include")
    parser.add_argument("-f", "--fecha", type=str, help="Date in format YYYY.MM.DD")
    parser.add_argument("-d", "--delay", type=int, help="Days ago")
    parser.add_argument(
        "--mpv",
        action="store_true",
        help="Reproducir el top con mpv en vez de abrirlo en el navegador (comportamiento por defecto)",
    )

    return parser.parse_args()

def print_top_clips_table(top_clips):
    """Imprime una tabla con el ranking del top de clips antes de reproducir/abrir."""
    # top_clips viene ordenado ascendente por views_per_hour; el ranking va del mejor al peor.
    ranked = sorted(top_clips, key=lambda c: c.views_per_hour, reverse=True)

    print()
    print("=" * 96)
    print(f" TOP {len(ranked)} CLIPS")
    print("=" * 96)
    print(f"{'#':<3}{'Vistas':>9}  {'V/hora':>9}  {'Peso':>5}  {'Dur':>5}  Título")
    print("-" * 96)
    for i, clip in enumerate(ranked, start=1):
        title = clip.title if len(clip.title) <= 55 else clip.title[:54] + "…"
        mins, secs = divmod(int(clip.duration), 60)
        print(
            f"{i:<3}{clip.views:>9,}  {clip.views_per_hour:>9.1f}  "
            f"{clip.channel_weight:>5.2f}  {mins:>2}:{secs:02d}  {title}"
        )
    print("=" * 96)
    print()


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

    # Mostrar la tabla del ranking antes de reproducir/abrir en el navegador
    print_top_clips_table(top_clips)

    # Generate playlist
    playlist_path = playlist_generator.create_playlist(top_clips)
    logging.info(f"Created playlist with {len(top_clips)} clips at {playlist_path}")

    # Con --mpv se reproduce el top con mpv. Por defecto se abren TODOS los top
    # clips en el navegador (vistas reales que ayudan al clipper).
    # top_clips viene ordenado ascendente por views_per_hour, asi que el mejor queda al final.
    if args.mpv:
        try:
            #subprocess.run(['mpv', playlist_path])
            os.system(f'mpv "{playlist_path}"')
        except Exception as e:
            logging.error(f"Failed to open mpv: {str(e)}")
        return

    # Abrir en el navegador (comportamiento por defecto)
    for i, clip in enumerate(top_clips):
        url = f"https://www.youtube.com/watch?v={clip.id}"
        logging.info(f"Abriendo en el navegador: {clip.title} ({url})")
        webbrowser.open_new_tab(url)
        # Pequeño delay entre pestañas: sin esto el navegador las abre en
        # paralelo y no respeta el orden. No dormir tras la ultima.
        if i < len(top_clips) - 1:
            time.sleep(0.8)


if __name__ == "__main__":
    main()
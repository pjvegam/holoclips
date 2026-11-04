import logging
import shutil
import subprocess
import time
import webbrowser

from models import Clip


def print_top_clips_table(top_clips: list[Clip]) -> None:
    """Imprime una tabla con el ranking del top de clips antes de reproducir/abrir."""
    # top_clips viene ordenado ascendente por score; el ranking va del mejor al peor.
    ranked = sorted(top_clips, key=lambda c: c.score, reverse=True)

    print()
    print("=" * 107)
    print(f" TOP {len(ranked)} CLIPS")
    print("=" * 107)
    print(f"{'#':<3}{'Vistas':>9}  {'V/hora':>9}  {'Peso':>5}  {'Score':>9}  {'Dur':>5}  Título")
    print("-" * 107)
    for i, clip in enumerate(ranked, start=1):
        title = clip.title if len(clip.title) <= 55 else clip.title[:54] + "…"
        mins, secs = divmod(int(clip.duration), 60)
        print(
            f"{i:<3}{clip.views:>9,}  {clip.views_per_hour:>9.1f}  "
            f"{clip.channel_weight:>5.2f}  {clip.score:>9.1f}  {mins:>2}:{secs:02d}  {title}"
        )
    print("=" * 107)
    print()


def play_with_mpv(playlist_path: str) -> bool:
    """Reproduce la playlist con mpv. Devuelve False si mpv no esta instalado."""
    # which() respeta PATHEXT: en Windows elige mpv.com, igual que la consola
    mpv_path = shutil.which("mpv")
    if not mpv_path:
        return False
    subprocess.run([mpv_path, playlist_path], check=False)
    return True


def open_in_browser(clips: list[Clip]) -> None:
    """Abre los clips en el navegador (vistas reales que ayudan al clipper)."""
    for i, clip in enumerate(clips):
        url = f"https://www.youtube.com/watch?v={clip.id}"
        logging.info(f"Abriendo en el navegador: {clip.title} ({url})")
        webbrowser.open_new_tab(url)
        # Pequeño delay entre pestañas: sin esto el navegador las abre en
        # paralelo y no respeta el orden. No dormir tras la ultima.
        if i < len(clips) - 1:
            time.sleep(0.8)

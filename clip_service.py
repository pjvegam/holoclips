from typing import List, Dict
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from models import Clip
from youtube_service import YouTubeService
from channel_repository import ChannelRepository
from api_service import HolodexApiService
import logging

class ClipService:
    def __init__(self, api_service: HolodexApiService, channel_repo: ChannelRepository,
                 youtube_service: YouTubeService):
        self.api_service = api_service
        self.channel_repo = channel_repo
        self.youtube_service = youtube_service

    def fetch_clips_for_date(self, target_date: datetime, max_workers: int = 10) -> Dict[str, Clip]:
        """Fetch all clips for a specific date using parallel processing."""
        from_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        to_date = from_date + timedelta(days=1)

        all_clips = {}
        limit = 100
        max_offset = 500  # Limitar a 500 por seguridad

        # Implementar procesamiento en paralelo como el original
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for offset_value in range(0, max_offset, limit):
                futures.append(executor.submit(
                    self.api_service.get_clips, 
                    from_date, to_date, limit=limit, offset=offset_value
                ))

            for future in as_completed(futures):
                try:
                    clip_data = future.result()
                    if not clip_data:
                        continue

                    # Si recibimos menos resultados que el límite, significa que hemos llegado al final
                    if len(clip_data) < limit:
                        logging.info(f"Reached end of results with {len(clip_data)} clips")

                    # Procesar los clips obtenidos
                    for clip in clip_data:
                        if clip['status'] == "missing":
                            continue
                        self._process_clip(clip, all_clips)

                except Exception as e:
                    logging.error(f"Error obteniendo clips: {str(e)}")

        logging.info(f"Total clips encontrados: {len(all_clips)}")
        return all_clips

    def _process_clip(self, clip_data: dict, clip_collection: Dict[str, Clip]) -> None:
        """Process a clip and add it to the collection if it matches criteria."""
        channel_ids = self.channel_repo.get_all_channel_ids()
        clip_id = clip_data['id']

        duration = clip_data.get('duration', 0)
        if duration < 60 or duration > 600:
            return

        # Find max weight from sources, refers, mentions
        max_weight = 0.0
        for source in clip_data.get('sources', []):
            if source['channel']['id'] in channel_ids:
                max_weight = max(max_weight, self.channel_repo.get_channel_weight(source['channel']['id']))

        for refer in clip_data.get('refers', []):
            if refer['channel']['id'] in channel_ids:
                max_weight = max(max_weight, self.channel_repo.get_channel_weight(refer['channel']['id']))

        for mention in clip_data.get('mentions', []):
            if mention['id'] in channel_ids:
                max_weight = max(max_weight, self.channel_repo.get_channel_weight(mention['id']))

        # Only add clips that reference a tracked channel
        if max_weight == 0.0:
            return

        if clip_id not in clip_collection:
            clip_collection[clip_id] = Clip(
                id=clip_id,
                title=clip_data['title'],
                available_at=datetime.fromisoformat(clip_data['available_at']).replace(tzinfo=None),
                duration=duration,
                channel_weight=max_weight
            )
        else:
            clip_collection[clip_id].channel_weight = max(clip_collection[clip_id].channel_weight, max_weight)

    def enrich_clips_with_views(self, clips: Dict[str, Clip]) -> None:
        """Add view counts to clips, marking the ones without data as unavailable."""
        views = self.youtube_service.get_videos_views(list(clips))
        for clip_id, clip in clips.items():
            clip.views = views.get(clip_id, -1)  # -1 marca como no disponible

        # Sin esto, un top calculado con datos parciales pareceria correcto
        missing = len(clips) - len(views)
        if missing:
            logging.warning(f"{missing}/{len(clips)} clips sin vistas: el top puede estar incompleto")

    def get_top_clips(self, clips: Dict[str, Clip], count: int) -> List[Clip]:
        """Get the top N clips sorted by views per hour, then return them in ascending order."""
        # Filter out invalid views
        valid_clips = [clip for clip in clips.values() if clip.views >= 0]

        # First sort by views per hour (descending) to get top N
        top_clips = sorted(
            valid_clips,
            key=lambda c: c.views_per_hour,
            reverse=True
        )[:count]

        # Then reorder those top N clips in ascending order
        return sorted(top_clips, key=lambda c: c.views_per_hour)
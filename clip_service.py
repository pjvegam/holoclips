import logging
from datetime import datetime, timedelta

from api_service import HolodexApiService
from channel_repository import ChannelRepository
from models import Clip
from youtube_service import YouTubeService


class ClipService:
    def __init__(
        self,
        api_service: HolodexApiService,
        channel_repo: ChannelRepository,
        youtube_service: YouTubeService,
    ):
        self.api_service = api_service
        self.channel_repo = channel_repo
        self.youtube_service = youtube_service

    def fetch_clips_for_date(self, target_date: datetime) -> dict[str, Clip]:
        """Fetch all clips for a specific date, page by page."""
        from_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        to_date = from_date + timedelta(days=1)

        all_clips = {}
        limit = HolodexApiService.MAX_LIMIT
        max_offset = 500  # Limitar a 500 por seguridad

        for offset in range(0, max_offset, limit):
            try:
                clip_data = self.api_service.get_clips(
                    from_date, to_date, limit=limit, offset=offset
                )
            except Exception as e:
                logging.error(f"Error obteniendo clips: {e!s}")
                continue

            for clip in clip_data:
                if clip["status"] == "missing":
                    continue
                self._process_clip(clip, all_clips)

            # Menos resultados que el límite significa que hemos llegado al final
            if len(clip_data) < limit:
                break
        else:
            logging.warning(f"Se alcanzó el tope de {max_offset} clips: puede haber más")

        logging.info(f"Total clips encontrados: {len(all_clips)}")
        return all_clips

    def _process_clip(self, clip_data: dict, clip_collection: dict[str, Clip]) -> None:
        """Process a clip and add it to the collection if it matches criteria."""
        channel_ids = self.channel_repo.get_all_channel_ids()
        clip_id = clip_data["id"]

        duration = clip_data.get("duration", 0)
        if duration < 60 or duration > 600:
            return

        # Find max weight from sources, refers, mentions
        max_weight = 0.0
        for source in clip_data.get("sources", []):
            if source["channel"]["id"] in channel_ids:
                max_weight = max(
                    max_weight, self.channel_repo.get_channel_weight(source["channel"]["id"])
                )

        for refer in clip_data.get("refers", []):
            if refer["channel"]["id"] in channel_ids:
                max_weight = max(
                    max_weight, self.channel_repo.get_channel_weight(refer["channel"]["id"])
                )

        for mention in clip_data.get("mentions", []):
            if mention["id"] in channel_ids:
                max_weight = max(max_weight, self.channel_repo.get_channel_weight(mention["id"]))

        # Only add clips that reference a tracked channel
        if max_weight == 0.0:
            return

        if clip_id not in clip_collection:
            clip_collection[clip_id] = Clip(
                id=clip_id,
                title=clip_data["title"],
                available_at=datetime.fromisoformat(clip_data["available_at"]),
                duration=duration,
                channel_weight=max_weight,
            )
        else:
            clip_collection[clip_id].channel_weight = max(
                clip_collection[clip_id].channel_weight, max_weight
            )

    def enrich_clips_with_views(self, clips: dict[str, Clip]) -> None:
        """Add view counts to clips, marking the ones without data as unavailable."""
        views = self.youtube_service.get_videos_views(list(clips))
        for clip_id, clip in clips.items():
            clip.views = views.get(clip_id, -1)  # -1 marca como no disponible

        # Un fallo de la API ya habria lanzado YouTubeApiError: estos clips existen en
        # Holodex pero YouTube no da sus vistas, asi que el top sigue siendo fiable
        missing = len(clips) - len(views)
        if missing:
            logging.info(
                f"{missing}/{len(clips)} clips sin vistas disponibles "
                "(borrados, privados u ocultos)"
            )

    def get_top_clips(self, clips: dict[str, Clip], count: int) -> list[Clip]:
        """Get the top N clips sorted by score, then return them in ascending order."""
        # Filter out invalid views
        valid_clips = [clip for clip in clips.values() if clip.views >= 0]

        # First sort by score (descending) to get top N
        top_clips = sorted(valid_clips, key=lambda c: c.score, reverse=True)[:count]

        # Then reorder those top N clips in ascending order
        return sorted(top_clips, key=lambda c: c.score)

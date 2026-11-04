# holoclips

> CLI para descubrir los clips más vistos de canales de Hololive Production y generar playlists reproducibles en MPV.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ¿Qué hace?

Consulta la API de [Holodex](https://holodex.net/) para una fecha dada, obtiene los clips subidos ese día de una lista curada de canales de Hololive Production (~60 miembros), enriquece cada clip con su cantidad de views vía YouTube API, ordena por popularidad ponderada según el peso asignado a cada canal, y genera un playlist `.m3u` que abre automáticamente en MPV.

## Uso

```bash
# Top 5 clips de hace 2 días (default)
python main.py

# Top 10 clips de una fecha específica
python main.py 10 --fecha 2025.06.15

# Top 3 clips de 5 días atrás
python main.py 3 --delay 5
```

## Requisitos del sistema

Además de Python 3.12+ y [uv](https://docs.astral.sh/uv/), necesitas estos binarios instalados en el PATH (no vienen por pip):

| Binario | Para qué | Obligatorio |
|---------|----------|-------------|
| **mpv** | Reproductor donde se abre el playlist generado | Sí |
| **yt-dlp** | mpv lo usa internamente para resolver URLs de YouTube | Sí |
| **ffmpeg** | yt-dlp lo usa para combinar streams de audio y video | Recomendado |

```bash
# Windows (winget) — yt-dlp.FFmpeg incluye ambos con parches para yt-dlp
winget install yt-dlp.FFmpeg shinchiro.mpv

# macOS (Homebrew)
brew install ffmpeg mpv yt-dlp

# Linux (Debian/Ubuntu)
sudo apt install ffmpeg mpv
pipx install yt-dlp   # o el método preferido de tu distro
```

> **Manten yt-dlp actualizado**: YouTube cambia seguido la lógica de extracción y rompe el resolver. Si tus playlists dejan de reproducir, actualiza yt-dlp primero.

## Setup

```bash
# Copiar el ejemplo
cp .env.example .env

# Editar .env con tus API keys
# API_KEY1 y API_KEY2 son de Holodex (rotan por paridad del día para evitar rate limits)
# YOUTUBE_API_KEY es de YouTube Data API v3 (para obtener las vistas de los clips)

# Instalar dependencias con uv
uv sync

# Correr
uv run python main.py
```

Requiere API keys de [Holodex](https://holodex.net/api) y de [YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com) (gratis, se crea en Google Cloud).

## Stack

- Python 3.12+
- `requests` para HTTP
- `python-dotenv` para config
- Gestión de dependencias con `uv`

## Estructura

```
holoclips/
├── main.py                # CLI + orquestación
├── api_service.py         # cliente Holodex API
├── channel_repository.py  # lista curada de canales con pesos
├── clip_service.py        # fetching + enrichment + ranking
├── playlist_generator.py  # genera .m3u
├── youtube_service.py     # consultas de view count
├── models.py              # dataclasses
└── config.py              # config desde .env
```

## Decisiones de diseño

- **Weighted ranking**: cada canal tiene un peso asignado (miembros con menos suscriptores tienen peso mayor). Los clips se ordenan por `views × weight`, de modo que canales menos populares no queden siempre invisibles bajo las estrellas.
- **Rotación de API keys por paridad del día**: para no exceder rate limits de Holodex cuando se corre esto diariamente, se alterna entre dos keys según si el día del mes es par o impar.
- **Repository pattern** para canales: la lista curada se mantiene en memoria y se comporta como catálogo consultable, en lugar de estar dispersa en el código.
- **Separación en servicios**: `api_service`, `clip_service`, `youtube_service`, `playlist_generator` — cada uno con una responsabilidad, facilita testear y modificar.

## Estado

Uso personal, no mantenido activamente. Publicado como portfolio.

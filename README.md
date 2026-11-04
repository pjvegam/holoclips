# holoclips

> CLI para descubrir los clips más vistos de canales de Hololive Production, abrirlos en el navegador o reproducirlos en MPV.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ¿Qué hace?

Consulta la API de [Holodex](https://holodex.net/) para una fecha dada, obtiene los clips subidos ese día de una lista curada de canales ([`channels.toml`](channels.toml)), enriquece cada clip con su cantidad de views vía YouTube Data API y los ordena por vistas por hora, ponderadas según el peso de cada canal. Muestra el ranking en una tabla, genera un playlist `.m3u` y abre los clips en el navegador (o en MPV con `--mpv`).

## Uso

```bash
# Top 5 clips de hace 2 días (default)
python main.py

# Top 10 clips de una fecha específica
python main.py 10 --fecha 2025.06.15

# Top 3 clips de 5 días atrás
python main.py 3 --delay 5

# Reproducir el top en MPV en vez de abrirlo en el navegador
python main.py --mpv
```

## Requisitos del sistema

Además de Python 3.12+ y [uv](https://docs.astral.sh/uv/), para usar `--mpv` necesitas estos binarios instalados en el PATH (no vienen por pip). Para abrir los clips en el navegador no hacen falta:

| Binario | Para qué | Con `--mpv` |
|---------|----------|-------------|
| **mpv** | Reproductor donde se abre el playlist generado | Obligatorio |
| **yt-dlp** | mpv lo usa internamente para resolver URLs de YouTube | Obligatorio |
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
# HOLODEX_API_KEY es de Holodex (para listar los clips)
# YOUTUBE_API_KEY es de YouTube Data API v3 (para obtener las vistas de los clips)

# Instalar dependencias con uv
uv sync

# Correr
uv run python main.py
```

Requiere API keys de [Holodex](https://holodex.net/api) y de [YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com) (gratis, se crea en Google Cloud).

## Desarrollo

```bash
uv run pytest             # tests (sin red ni API keys)
uv run ruff check .       # lint
uv run ruff format .      # formato
```

## Stack

- Python 3.12+
- `requests` para HTTP
- `python-dotenv` para config
- Gestión de dependencias con `uv`
- `pytest` y `ruff` para tests y calidad de código

## Estructura

```
holoclips/
├── main.py                # CLI + orquestación
├── channels.toml          # lista curada de canales con pesos
├── channel_repository.py  # carga y consulta de canales
├── api_service.py         # cliente Holodex API
├── youtube_service.py     # vistas vía YouTube Data API
├── clip_service.py        # fetching + enrichment + ranking
├── output.py              # tabla en consola, mpv y navegador
├── playlist_generator.py  # genera .m3u
├── models.py              # dataclasses
├── config.py              # config desde .env
└── tests/
```

## Decisiones de diseño

- **Weighted ranking**: cada canal tiene un peso asignado (miembros con menos suscriptores tienen peso mayor). Los clips se ordenan por `score = vistas por hora × peso`, de modo que canales menos populares no queden siempre invisibles bajo las estrellas. La tabla muestra las vistas por hora reales y el score por separado.
- **Repository pattern** para canales: la lista curada vive en `channels.toml` y se comporta como catálogo consultable, así que agregar un canal no requiere tocar código.
- **Separación en servicios**: `api_service`, `clip_service`, `youtube_service`, `playlist_generator`, `output` — cada uno con una responsabilidad, facilita testear y modificar.
- **Sin top parcial**: si Holodex falla, o YouTube Data API tras los reintentos, el programa termina con error en vez de generar un ranking al que le falten clips.

## Estado

Uso personal, no mantenido activamente. Publicado como portfolio.

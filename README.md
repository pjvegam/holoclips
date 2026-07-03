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

## Setup

```bash
# Copiar el ejemplo (si existe, sino crear .env manualmente)
cp .env.example .env  # o crearlo directo

# Editar .env con tus API keys
# API_KEY1 y API_KEY2 son de Holodex (rotan por paridad del día para evitar rate limits)

# Instalar dependencias con uv
uv sync

# Correr
uv run python main.py
```

Requiere API key de [Holodex](https://holodex.net/api).

## Stack

- Python 3.12+
- `requests` para HTTP
- `python-dotenv` para config
- Gestión de dependencias con `uv`
- **MPV** debe estar en el PATH del sistema

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

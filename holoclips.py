import time
import requests
import argparse
import os
from pytube import YouTube
from channels import channels
from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv
from threading import Thread
from pytubefix.exceptions import (
    VideoPrivate,
    VideoUnavailable,
    VideoRegionBlocked,
    AgeRestrictedError,
    MembersOnly,
    RecordingUnavailable,
)

env_path = os.path.abspath('.venv/.env')
load_dotenv(dotenv_path=env_path)

parser = argparse.ArgumentParser(description="Enviar fecha espefifica o dias atrasados")
parser.add_argument("-f", "--fecha", type=str, help="fecha a,m,d.")
parser.add_argument("-d", "--delay", type=int, help="dias atrasado")

args = parser.parse_args()

# Tu clave de API
api_key1 = os.getenv('API_KEY1')
api_key2 = os.getenv('API_KEY2')
api_key = api_key2

# Fecha que quieres filtrar

if args.fecha is not None:
    anno, mes, dia = args.fecha.split(".")
    fecha_deseada = datetime(int(anno), int(mes), int(dia))
else:
    fecha_deseada = datetime.now().replace(hour=00,minute=0,second=1,microsecond=0) - timedelta(days=2)

if args.delay is not None:
    fecha_deseada = fecha_deseada - temedelta(days=args.delay)


fecha_ahora = datetime.now()

if fecha_deseada.day % 2 == 0:
    api_key = api_key1

# fecha_deseada = datetime.strptime(fecha_deseada, "%Y-%m-%d").date()

# Configurar el encabezado con la clave de API
headers = {
    'X-APIKEY': api_key
}

# URL de la API que deseas consultar
url = 'https://holodex.net/api/v2/videos'

offset = 0
limit = 100
n_clips = 10

BestClips = []
cont = 0
cont = cont + 1

channels_id = list(channels.keys())

params = {
    'lang': 'en,es',
    'type': 'clip',
    'from': fecha_deseada,
    'to': fecha_deseada + timedelta(days=1),
    'include': 'sources,mentions,refers',
    'offset': offset,
    'limit': limit,
}

clips_channel = {}
yt_views = {}
results = {}


def get_clips(url, headers, params, offset):
    params = params.copy()
    params['offset'] += offset
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        msg = "La solicitud no fue exitosa. Código de estado:"
        print(msg, response.status_code, response.json())

    data = response.json()
    results[offset] = len(data)

    for clip in data:
        if clip['status'] != "missing":
            if 'sources' in clip.keys():
                for source in clip['sources']:
                    if source['channel']['id'] in channels_id:
                        if clip['id'] not in clips_channel:
                            clips_channel[clip['id']] = [
                                clip['available_at'],
                                clip['title'],
                                channels[source['channel']['id']][1]
                                ]
                        else:
                            if clips_channel[clip['id']][2] < channels[source['channel']['id']][1]:
                                clips_channel[clip['id']][2] = channels[source['channel']['id']][1]

            if 'refers' in clip.keys():
                for refer in clip['refers']:
                    if refer['channel']['id'] in channels_id:
                        if clip['id'] not in clips_channel:
                            clips_channel[clip['id']] = [
                                    clip['available_at'],
                                    clip['title'],
                                    channels[refer['channel']['id']][1]
                                    ]
                        else:
                            if clips_channel[clip['id']][2] < channels[refer['channel']['id']][1]:
                                clips_channel[clip['id']][2] = channels[refer['channel']['id']][1]

            if 'mentions' in clip.keys():
                for mention in clip['mentions']:
                    if mention['id'] in channels_id:
                        if clip['id'] not in clips_channel:
                            clips_channel[clip['id']] = [
                                    clip['available_at'],
                                    clip['title'],
                                    channels[mention['id']][1]
                                    ]
                        else:
                            if clips_channel[clip['id']][2] < channels[mention['id']][1]:
                                clips_channel[clip['id']][2] = channels[mention['id']][1]



new_offset = 0
gap = 3 * limit
while True:

    threads = []
    # Imprimir los IDs filtrados
    for val in range(new_offset, new_offset + gap + 1, limit):
        # URL del video de YouTube
        process = Thread(target=get_clips, args=[url, headers, params, val])
        process.start()
        threads.append(process)

    for process in threads:
        process.join()

    min_result = min([results[val] for val in results])
    if min_result < limit:
        break

    new_offset += gap


def get_yt_views(id_video):
    video_url = "https://www.youtube.com/watch?v="+id_video
    yt = YouTube(video_url)
    yt_views[id_video] = yt.views

threads = []
# Imprimir los IDs filtrados
for id_filtrado in clips_channel:
    # URL del video de YouTube
    process = Thread(target=get_yt_views, args=[id_filtrado])
    process.start()
    threads.append(process)

for process in threads:
    process.join()

for id_filtrado in clips_channel:
    fecha_disponible = clips_channel[id_filtrado][0]
    title = clips_channel[id_filtrado][1]
    factor = clips_channel[id_filtrado][2]

    fecha_disponible = datetime.fromisoformat(fecha_disponible)
    fecha_disponible = fecha_disponible.replace(tzinfo=None)

    if id_filtrado not in yt_views:
        yt_views[id_filtrado] = -1
        print(f"video {id_filtrado} no disponible")

    views = yt_views[id_filtrado]*factor

    horas_publicada = fecha_ahora - fecha_disponible
    horas_publicada = horas_publicada.total_seconds() / 3600
    viewsaverage = views/horas_publicada

    if len(list(filter(lambda x: x[0] == id_filtrado, BestClips))) == 0:
        if len(BestClips) < n_clips:
            BestClips.append((id_filtrado, viewsaverage, title))
        elif viewsaverage > BestClips[0][1]:
            BestClips[0] = ((id_filtrado, viewsaverage, title))

    BestClips.sort(key=lambda x: x[1])

path = os.path.join(os.getenv('PROJECT_PATH'), "clips.m3u")
file = open(path, "w")
print(f'clips from: {fecha_deseada}\n')

for clip_id, avrg_hours, title in BestClips:
    line = f"https://www.youtube.com/watch?v={clip_id}\n"
    file.write(line)
file.close()

os.system(f'mpv "{path}"')
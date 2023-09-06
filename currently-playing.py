### Eska Rock Rich Presence
## By TheRadziu
# v1.0.2
import requests
import json
from pypresence import Presence
import time
from datetime import datetime,timezone

# SETTINGS #
wait_time = 15 # Conajmniej 15
URL = "https://player.eskarock.pl/api/mobile/station/5980/now_playing/" # Aby zmienić stację na inną podmień jej ID
client_id = "1148784842494988358" # ID Aplikacji, w tym wypadku "Eska Rock"
############

def parse_api():
    r = requests.get(url=URL)
    json_data = json.loads(r.text)
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%H:%M:%S")
    for songs in json_data:
        if current_time > songs['start_time'][11:-6]:
            if songs['thumb'] is None:
                songs['thumb'] = "https://cdn.music.smcloud.net/t/cover/02c59e2d-798d-4e47-9d80-93e451f5b5ed_icon-ROCK-NEW-eska_500x500.png"
            return songs['thumb'], songs['artists'][0]['name'], songs['name']

RPC = Presence(client_id=client_id)
RPC.connect()
start_time=time.time()
last_song = ""

while True:
    if last_song == "" or last_song != parse_api()[2]:
        last_song = parse_api()[2]
        print("Currently playing: "+parse_api()[2]+" by "+parse_api()[1])
        RPC.update(large_image=parse_api()[0],
            details=parse_api()[1],
            state=parse_api()[2],
            start=start_time)
    time.sleep(wait_time)

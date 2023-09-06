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
            return songs['thumb'], songs['artists'][0]['name'], songs['name']

RPC = Presence(client_id=client_id)
RPC.connect()
start_time=time.time()

while 1:
    RPC.update(large_image=parse_api()[0],
            details=parse_api()[1],
            state=parse_api()[2],
            start=start_time)
    #print("Currently playing: "+parse_api()[2]+" by "+parse_api()[1])
    time.sleep(wait_time)

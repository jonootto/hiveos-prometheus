#!/usr/bin/python3
#pip3 install -r requirements.txt

import json
from datetime import datetime, timedelta
from time import sleep
import os
from prometheus_client import Gauge, start_http_server

print("Get Stats")


def time_string():
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    return current_time


def hashrate(rates,total):
    #print(str(len(rates)) + " CARDS")
    for x in range(len(rates)):
        g['hash'].labels(rig=rig,card = x).set(rates[x]*1000)
        g['hash'].labels(rig=rig,card = "total").set(total)


def timetowait():
    delta = timedelta(minutes=1)
    now = datetime.now()
    next_minute = (now + delta).replace(microsecond=0,second=30)
    wait_seconds = (next_minute - now)
    wait_seconds = int((wait_seconds).total_seconds())
    print("    " + time_string() + "   " + str(wait_seconds)+"s until next")
    return(wait_seconds)

def cardstats(ctemps,mtemps,power,fan):
    for x in range(len(ctemps)):
        
        g['coretemp'].labels(rig=rig,card = x).set(ctemps[x])
        g['memtemp'].labels(rig=rig,card = x).set(mtemps[x])
        g['power'].labels(rig=rig,card = x).set(power[x])
        g['fan'].labels(rig=rig,card = x).set(fan[x])


def main():
    print("Main")
    start_http_server(7890)
    while(True):
        with open("/run/hive/last_stat.json") as json_data_file:
            stats = json.load(json_data_file)
            hash = (stats["params"]["miner_stats"]["hs"])
            
            ctemps = (stats["params"]["temp"])
            try:
                mtemps = (stats["params"]["mtemp"])
            except:
                mtemps = [0] * len(hash)
            power = (stats["params"]["power"])
            fan = (stats["params"]["fan"])
            totalhash = (int((stats["params"]["total_khs"]))*1000)
            
        hashrate(hash,totalhash)
        cardstats(ctemps,mtemps,power,fan)
        sleep(timetowait())


rig = os.environ['RIG_NAME']
print(rig)

g = {}
g['hash'] = Gauge('hive_hashrate','Hashrate',['rig','card'])
g['coretemp'] = Gauge('hive_coretemp','GPU Core Temp',['rig','card'])
g['memtemp'] = Gauge('hive_memtemp','GPU Memory Temperature',['rig','card'])
g['power'] = Gauge('hive_power','GPU Power Consumption',['rig','card'])
g['fan'] = Gauge('hive_fan','GPU Fan Speed',['rig','card'])




main()

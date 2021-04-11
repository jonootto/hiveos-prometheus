#!/usr/bin/python3
#pip3 install -r requirements.txt

import json
from influxdb import InfluxDBClient
import requests
from datetime import datetime, timedelta
from time import sleep
import os

print("Get Stats")

def setdb():
    dbname = 'hive'
    makedb = True
    dbs = client.get_list_database()
    for x in dbs:
        if (x['name']) == dbname:
            makedb = False

    if makedb:
        print('making the db')
        client.create_database(dbname)
    else:
        client.switch_database(dbname)

def time_string():
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    return current_time

def toinflux(input):
    client.write_points(input,time_precision='s')

def hashrate(rates,total):
    g0 = rates[0]
    g1 = rates[1]
    g2 = rates[2]
    g3 = rates[3]
    g4 = rates[4]
    g5 = rates[5]
    g6 = rates[6]
    g7 = rates[7]

    json_body = [
    {
        "measurement": "hashrate",
        "tags": {
            "miner" :rig,
            "gpu" : 0
        },
        "time": time_string(),
        "fields": {
            "Hashrate": g0
        }
    },
    {
        "measurement": "hashrate",
        "tags": {
            "miner" :rig,
            "gpu" : 1
        },
        "time": time_string(),
        "fields": {
            "Hashrate": g1
        }
    },
    {
        "measurement": "hashrate",
        "tags": {
            "miner" :rig,
            "gpu" : 2
        },
        "time": time_string(),
        "fields": {
            "Hashrate": g2
        }
    },
    {
        "measurement": "hashrate",
        "tags": {
            "miner" :rig,
            "gpu" : 3
        },
        "time": time_string(),
        "fields": {
            "Hashrate": g3
        }
    },
    {
        "measurement": "hashrate",
        "tags": {
            "miner" :rig,
            "gpu" : 4
        },
        "time": time_string(),
        "fields": {
            "Hashrate": g4
        }
    },
    {
        "measurement": "hashrate",
        "tags": {
            "miner" :rig,
            "gpu" : 5
        },
        "time": time_string(),
        "fields": {
            "Hashrate": g5
        }
    },
    {
        "measurement": "hashrate",
        "tags": {
            "miner" :rig,
            "gpu" : 6
        },
        "time": time_string(),
        "fields": {
            "Hashrate": g6
        }
    },
    {
        "measurement": "hashrate",
        "tags": {
            "miner" :rig,
            "gpu" : 7
        },
        "time": time_string(),
        "fields": {
            "Hashrate": g7
        }
    },
    {
        "measurement": "hashrate",
        "tags": {
            "miner" :rig,
            "gpu" : "total"
        },
        "time": time_string(),
        "fields": {
            "Hashrate": total
        }
    }
    ]
    toinflux(json_body)


def timetowait():
    delta = timedelta(minutes=1)
    now = datetime.now()
    next_minute = (now + delta).replace(microsecond=0,second=30)
    wait_seconds = (next_minute - now)
    wait_seconds = int((wait_seconds).total_seconds())
    print("    " + str(wait_seconds)+"s until next")
    return(wait_seconds)

def cardstats(ctemps,mtemps,power,fan):
    for x in range(len(ctemps)):
        json_body = [
        {
            "measurement": "Cards",
            "tags": {
                "miner" :rig,
                "gpu" : str(x)
            },
            "time": time_string(),
            "fields": {
                "Core Temperature": ctemps[x],
                "Memory Temperature": mtemps[x],
                "Power": power[x],
                "Fan": fan[x]
            }
        }
        ]
        toinflux(json_body)

def main():
    print("Main")
    while(True):
        with open("/run/hive/last_stat.json") as json_data_file:
            stats = json.load(json_data_file)
            hash = (stats["params"]["miner_stats"]["hs"])
            ctemps = (stats["params"]["temp"])
            mtemps = (stats["params"]["mtemp"])
            power = (stats["params"]["power"])
            fan = (stats["params"]["fan"])
            totalhash = (int((stats["params"]["total_khs"]))*1000)
        hashrate(hash,totalhash)
        cardstats(ctemps,mtemps,power,fan)
        sleep(timetowait())


# with open("./settings.json") as json_data_file:
#     settings = json.load(json_data_file)
#     influxip = settings['influx-settings']['host']
#     influxport = settings['influx-settings']['port']
#     influxuser = settings['influx-settings']['username']
#     influspass = settings['influx-settings']['password']
#     rig = settings['influx-settings']['rig']
influxip = os.environ['INFLUX_IP']
influxport = os.environ['INFLUX_PORT']
influxuser = os.environ['INFLUX_USER']
influspass = os.environ['INFLUX_PASS']
rig = os.environ['RIG_NAME']

requests.packages.urllib3.disable_warnings()
client = InfluxDBClient(host=influxip, port=influxport, username=influxuser, password=influspass,ssl=True,verify_ssl=False)

setdb()
main()

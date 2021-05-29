import subprocess
import json
import time
import requests
from config import beacon

j = json.loads(subprocess.check_output("dht-sensor 0 DHT22 json", shell=True))
time.sleep(10)
jj = json.loads(subprocess.check_output("dht-sensor 0 DHT22 json", shell=True))
h1 = j["humidity"]
h2 = jj["humidity"]
t1 = j["temperature"]
t2 = jj["temperature"]
if (
    abs(h1 - h2) > 2
    or abs(t1 - t2) > 2
    or t1 < -200
    or t2 < -200
    or h1 < -200
    or h2 < -200
):
    print("Problem")
else:
    str = json.dumps(jj)
    print(str)
    headers = (
        {
            "Authorization": f"Bearer {beacon}",
            "content-type": "application/json",
        },
    )

    r = requests.post(
        "http://raspberrypi:8123/api/state/sensor.omega2Temperature",
        headers=headers,
        data=json.dumps(
            {
                "state": jj["temperature"],
                "attributes": {"friendly_name": "Temperature"},
            }
        ),
    )
    r = requests.post(
        "http://raspberrypi:8123/api/state/sensor.omega2Humidity",
        headers=headers,
        data=json.dumps(
            {
                "state": jj["humidity"],
                "attributes": {"friendly_name": "Humidity"},
            }
        ),
    )
print(r)

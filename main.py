from machine import freq

"""
An attempt to overclock the Pi Pico for higher responsiveness.
Pi Pico to overclockable safely to 240MHz - 270MHz.
Base clock is 125MHz.
"""
try:
    freq(240000000)
except Exception as e:
    print("Core overclock not applied.")

print(f"-> Current speed is: {(freq()/1000000):.3f} MHZ")



from mm_wlan import connect_to_network
from time import sleep_ms
import ujson as json
from server import app, reset_display

ssid = ''
password = ''

with open ('config.json', 'r') as f:
    data = json.load(f)
    ssid = data['SSID']
    password = data['PASSWORD']
if ssid == '' or password == '':
    print("Please provide SSID and PASSWORD in config.json file.")
    sleep_ms(5000000000)
    raise Exception("SSID and PASSWORD not provided.")

connect_to_network(ssid, password)
reset_display()
app.run(port=80)

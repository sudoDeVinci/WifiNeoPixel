import uasyncio as asyncio
from microdot import Microdot, Response, Request, send_file
from neopixel import NeoPixel
from machine import Pin
from micropython import const
from time import sleep_ms

app = Microdot()
last_value = 0
N = const(300)
DISPLAY = NeoPixel(Pin(16), N, timing = 1)

COLOR_ZERO = const((0, 0, 0))
COLOR_LOW = const((20, 20, 20))
COLOR_MID = const((60, 60, 60))
COLOR_HIGH = const((100, 100, 100))
LEVELS = const((0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300))

def reset_display() -> None:
    global DISPLAY
    for i in range(N): DISPLAY[i] = COLOR_ZERO
    DISPLAY.write()

def fade_in(target_index: int) -> None:
    global DISPLAY
    for i in range(target_index):
        if DISPLAY[i] == COLOR_ZERO:
            
            DISPLAY[i] = COLOR_LOW
            DISPLAY.write()
            sleep_ms(100)

            DISPLAY[i] = COLOR_MID
            DISPLAY.write()
            sleep_ms(100)

            DISPLAY[i] = COLOR_HIGH
            DISPLAY.write()
            sleep_ms(100)

def fade_out(start_index: int, end_index: int) -> None:
    global DISPLAY
    for i in reversed(range(start_index, end_index+1)):
        if DISPLAY[i] == COLOR_HIGH:
            
            DISPLAY[i] = COLOR_MID
            DISPLAY.write()
            sleep_ms(100)
            
            DISPLAY[i] = COLOR_LOW
            DISPLAY.write()
            sleep_ms(100)

            DISPLAY[i] = COLOR_ZERO
            DISPLAY.write()
            sleep_ms(100)
    

@app.route('/favicon.ico')
def favicon(request: Request, path):
    return send_file('/static/favicon.png')

@app.route('/static/<path:path>')
def static(request, path):
    # directory traversal is not allowed
    if '..' in path:
        return 'Not found', 404
    return send_file('static/' + path)

@app.route('/', methods=['GET'])
def index_get(request)-> Response:
    return send_file('static/index.html')

@app.route('/', methods = ['POST'])
def index_post(request) -> None:
    global last_value
    
    level = int(request.json.get('luminance'))
    if 0 > level or level > 300: return

    if last_value > level:
        fade_out(LEVELS[level], LEVELS[last_value])
            
    if last_value < level:
        fade_in(LEVELS[level])
            
    DISPLAY.write()
    last_value = level

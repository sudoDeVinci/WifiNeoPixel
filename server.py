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
COLOR_LOW = const((5, 5, 5))
COLOR_MID = const((10, 10, 10))
COLOR_HIGH = const((15, 15, 15))
COLOR = const((25,25,25))
LEVELS = const((0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300))

BRIGHTNESS = 0.1

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

            DISPLAY[i] = COLOR_MID
            DISPLAY.write()
            
            DISPLAY[i] = COLOR_HIGH
            DISPLAY.write()
            
            DISPLAY[i] = COLOR
            DISPLAY.write()

def fade_out(start_index: int, end_index: int) -> None:
    global DISPLAY
    for i in reversed(range(start_index, end_index)):
        if DISPLAY[i] == COLOR:
            
            DISPLAY[i] = COLOR_MID
            DISPLAY.write()
            
            DISPLAY[i] = COLOR_LOW
            DISPLAY.write()

            DISPLAY[i] = COLOR_ZERO
            DISPLAY.write()
    

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
    
    label = request.json.get('label')
    value = int(request.json.get('value'))
    
    if label == 'level':
        level = value
        if 0 > level or level > 300: return

        if last_value > level:
            fade_out(LEVELS[level], LEVELS[last_value])
                
        if last_value < level:
            fade_in(LEVELS[level])
            
        last_value = level
            
    elif label == 'brightness':
        pass
        
            
    DISPLAY.write()

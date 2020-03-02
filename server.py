"""
Copyright 2020 Gould Southern
Author: Ryan Ledford [ https://github.com/rledford ]
"""

import ledcontroller
import configuration
from logger import logger
from colors import color_map
from flask import Flask, json

settings = configuration.Settings()
settings.load()

led = ledcontroller.LEDController(settings.num_leds);

server = Flask(__name__)

@server.route('/api/led/state/<string:state>', methods=['POST'])
def set_state(state = ''):
  if state == 'on':
    led.on()
  elif state == 'off':
    led.off()
  else:
    return 'Invalid state', 400
  
  return 'OK', 200

@server.route('/api/led/color/<string:color>', methods=['POST'])
def set_color(color = ''):
  if color[0] == '#' and len(color) == 7:
    try:
      led.fill_hex(color)
    except:
      return 'Invalid color', 400
  else:
    try:
        led.fill_hex(color_map[color])
    except Exception as ex:
      logger.error(ex)
      return 'Invalid color', 400

  return 'OK', 200

@server.route('/api/led/blink/<freq>', methods=['POST'])
def set_blink_freq(freq):
  try:
    led.blink_freq_sec = float(freq);
  except Exception as ex:
    logger.error(ex)
    return 'Invalid blink frequency', 400
  
  return 'OK', 200

"""
Copyright 2020 Gould Southern
Author: Ryan Ledford [ https://github.com/rledford ]
"""

import sys
import time
import threading
from logger import logger
from math import ceil
from random import randint

try:
    import spidev
except:
    pass


class _DummySpiDev():
    def __init__(self):
        logger.warn('SPI device (LED controller) unvailable')
        self.max_speed_hz = 0

    def open(self, *args):
        pass

    def close(self):
        pass

    def writebytes(self, *args):
        pass


class LEDController():
    MIN_BRIGHTNESS = 224
    MAX_BRIGHTNESS = 255
    MAX_FREQ_HZ = 8000000

    def __init__(self, num_leds, brightness=230, freq_hz=8000000):
        self._num_leds = num_leds
        self._freq_hz = min(freq_hz, LEDController.MAX_FREQ_HZ)
        self._leds = spidev.SpiDev() if 'spidev' in sys.modules else _DummySpiDev()
        self._brightness = max(LEDController.MIN_BRIGHTNESS, min(
            brightness, LEDController.MAX_BRIGHTNESS))
        self._led_data = [
            self._brightness, 0, 0, 0]*num_leds
        self._running = True
        self._blink_enabled = False
        self._blink_freq_sec = 1.0
        self._blink_phase = 0  # 0 off, 1 on
        self._next_blink_time = 0
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def hex_to_rgb(self, value=''):
        v = value.strip('#')
        r = int(v[0:2], 16)
        g = int(v[2:4], 16)
        b = int(v[4:6], 16)
        return(r, g, b)

    def set_pixel_color(self, pixel, r, g, b):
        """
        Set a single LED to a specific color
        """
        # Store reversed color order (b, g, r) instead of (r, g, b)
        self._led_data[pixel*4+1] = max(0, min(b, 255))  # BLUE
        self._led_data[pixel*4+2] = max(0, min(g, 255))  # GREEN
        self._led_data[pixel*4+3] = max(0, min(r, 255))  # RED

    def set_pixel_color_hex(self, pixel, value=''):
        """
        Set a single LED to a specific hex string color
        """
        r, g, b = self.hex_to_rgb(value)
        self.set_pixel_color(pixel, r, g, b)

    def fill(self, r, g, b):
        """
        Set all LEDs to the same color
        """
        for pixel in range(self._num_leds):
            self.set_pixel_color(pixel, r, g, b)

    def fill_hex(self, value=''):
        """
        Set all LEDs to the same hex string color
        """
        r, g, b = self.hex_to_rgb(value)
        self.fill(r, g, b)

    def update(self):
        """
        Send current LED data to device
        """
        if len(self._led_data) > 0:
            self._leds.writebytes([0]*4)
            self._leds.writebytes(self._led_data)
            self._leds.writebytes([0]*ceil(self._num_leds/16))

    def on(self):
        """
        Turn on all LEDs
        This only changes the LED brightness to the maximum value without affecting the set color values
        """
        for i in range(self._num_leds):
            self._led_data[i*4] = self._brightness

    def off(self):
        """
        Turn off all LEDs
        Changes the LED brightness to the minimum value without affecting the set color values
        """
        for i in range(self._num_leds):
            self._led_data[i*4] = LEDController.MIN_BRIGHTNESS

    @property
    def blink_freq_sec(self):
        return self._blink_freq_sec

    @blink_freq_sec.setter
    def blink_freq_sec(self, blink_freq_sec):
        """
        If blink_freq_sec is greater than 0, the controller handles blinking automatically
        """
        if isinstance(blink_freq_sec, (int, float)) and blink_freq_sec >= 0 and blink_freq_sec != self._blink_freq_sec:
            self._blink_freq_sec = blink_freq_sec
            self._blink_enabled = self._blink_freq_sec > 0
            self._next_blink_time = time.time() + self._blink_freq_sec
            self._blink_phase = 0
            self.on()

    def blink(self):
        """
        Toggles the LEDs on or off each call
        Setting the blink_freq_sec property greater than zero allows the controller to handle blinking automatically
        """
        if self._blink_phase == 0:
            self.off()
        else:
            self.on()
        self._blink_phase = 0 if self._blink_phase == 1 else 1
        self._next_blink_time = time.time() + self._blink_freq_sec

    def _run(self):
        self._leds.open(0, 1)
        self._leds.max_speed_hz = self._freq_hz
        while self._running:
            now = time.time()
            if self._blink_enabled and self._next_blink_time < now:
                self.blink()
            self.update()
            time.sleep(0.02)

    def start(self):
        """
        Start controlling the LEDs
        """
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()

    def stop(self):
        """
        Stop controlling the LEDs - turns all LEDs off
        """
        self._running = False
        try:
            self._thread.join()
        except:
            pass
        self.blink_freq_sec = 0
        self.off()
        self.update()
        self._leds.close()
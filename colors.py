"""
Copyright 2020 Gould Southern
Author: Ryan Ledford [ https://github.com/rledford ]
"""

from random import randint

red = '#C0392B'
green = '#229954'
blue = '#3498DB'
yellow = '#F7DC6F'
orange = '#E67E22'

color_map = {
  'red': red,
  'green': green,
  'blue': blue,
  'yellow': yellow,
  'orange': orange
}
color_values = [red, green, blue, yellow, orange]


def get_random_color():
    return color_values[randint(0, len(color_values) - 1)]
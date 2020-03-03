"""
Copyright 2020 Gould Southern
Author: Ryan Ledford [ https://github.com/rledford ]
"""

from random import randint

red = '#FF0000'
green = '#00FF00'
blue = '#0000FF'
yellow = '#FFFF00'
orange = '#FFA500'

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
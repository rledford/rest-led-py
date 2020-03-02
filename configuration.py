"""
Copyright 2020 Gould Southern
Author: Ryan Ledford [ https://github.com/rledford ]
"""

import os
import json
from logger import logger

DEFAULT_REST_USERNAME = 'admin';
DEFAULT_REST_PASSWORD = 'admindefault';

class Settings():
    def __init__(self):
        self.num_leds = 1
        self.rest_username = DEFAULT_REST_USERNAME;
        self.rest_password = DEFAULT_REST_PASSWORD;

    def serialize(self):
        return {
            "num_leds": self.num_leds,
            "rest_username": self.rest_username,
            "rest_password": self.rest_password
        }

    def load(self):
        try:
            f = open('settings.json', 'r')
            d = json.loads(''.join(f.readlines()))
        except FileNotFoundError:
            logger.error('settings file not found - saving default settings')
            self.save()
        except Exception as ex:
            logger.error('failed to load settings - %s' % str(ex))
        else:
            f.close()
            self.num_leds = d['num_leds']
            self.rest_username = d['rest_username']
            self.rest_password = d['rest_password']

    def save(self):
        try:
            f = open('settings.json', 'w')
            f.write(json.dumps(self.serialize(), indent=2))
        except:
            logger.error('failed to save settings')
        else:
            f.close()
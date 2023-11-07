#!/usr/bin/python

import sys
import pygame
import time

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (255, 0, 0)

resource_path = ''

resource_image = {
    'id_background' : 'image/background.png',
    'id_boom' : 'image/boom.png'
}

resource_sound = {
    'snd_shot' : 'sound/shot.wav',
    'snd_explosion' : 'sound/explosion.wav'
}

def get_img_resource(resource_id) :
    return resource_path + resource_image[resource_id]

def get_snd_resource(resource_id) :
    return resource_path + resource_sound[resource_id]

class game_ctrl :
    def __init__(self) :
        self.surface = None 
        self.width = 640
        self.height = 320

    def set_surface(self, surface) :
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()

    def save_scr_capture(self, prefix) :
        pygame.image.save(self.surface,(prefix + time.strftime('%Y%m%d%H%M%S')+ '.jpg'))

gctrl = game_ctrl()

if __name__ == '__main__' :
    print('game resoure')
#!/usr/bin/python

import sys
import pygame
import random

from gresource import *

class enemy_object :
    global gctrl

    def __init__(self, text) :
        self.text = text

        font = pygame.font.SysFont(None, 25)
        draw_text = font.render(self.text, True, COLOR_BLACK)
        draw_rect = draw_text.get_rect()

        self.x = random.randrange(0, gctrl.width - draw_rect.width)
        self.y = 20

        self.dx = 0
        self.dy = 5
       
    def set_speed(self, del_x, del_y) :
        self.dx = del_x
        self.dy = del_y

    def move(self, del_x = 0, del_y = 0) :
        if del_x == 0 :
            del_x = self.dx
        if del_y == 0 :
            del_y = self.dy

        self.x += del_x
        self.y += del_y

    def draw(self) :
        font = pygame.font.SysFont(None, 25)
        draw_text = font.render(self.text, True, COLOR_BLACK)
        gctrl.surface.blit(draw_text, (self.x, self.y))        

    def is_out_of_range(self) :
        if self.y <= 0 or self.y >= gctrl.height :
            return True
        else :
            return False

class boom_object :
    global gctrl

    def __init__(self, x, y) :
        self.x = x
        self.y = y
        self.count = 10

        self.boom_img = pygame.image.load(get_img_resource('id_boom'))

    def draw(self) :
        self.count -= 1
        if self.count <= 0 :
            return False

        gctrl.surface.blit(self.boom_img, (self.x, self.y))
        return True

if __name__ == '__main__' :
    print('enemy object')
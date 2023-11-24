#!/usr/bin/python

import sys
import pygame
import random

import csv
from io import StringIO

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

DOWN_SPEED = 20
ENEMY_CREATION_SPEED = 80
ENEMY_MAX = 5

test_word_str = 'Acted, Adapted, Combined, Composed, Conceptualized, Condensed, Created, Customized, Designed, Developed, \
                Devised, Directed, Displayed, Entertained, Established, Fashioned, Formulated, Founded, Illustrated, Initiated, \
                Instituted, Integrated, Introduced, Invented, Modeled, Modiﬁed, Originated, Performed, Photographed, Planned, \
                Revised, Revitalized, Shaped, Solve'    

class enemy_group :
    def __init__(self) :
        self.enemies = []
        self.max_enemy = ENEMY_MAX

        self.move_count = 0
        self.enemy_tick = 0

        self.delete_indexes = []

        self.booms = []

        self.test_dic = []
        f = StringIO(test_word_str)
        reader = csv.reader(f, delimiter=',')
        for rows in reader :
            for word in rows :
                word = word.strip()
                word = word.lower()
                self.test_dic.append(word)


    def create(self) :
        self.enemy_tick += 1
        if self.enemy_tick > ENEMY_CREATION_SPEED :
            self.enemy_tick = 0
        
            if len(self.enemies) < self.max_enemy :
                random.shuffle(self.test_dic)
                self.enemies.append(enemy_object(self.test_dic[0]))

    def compare(self, input_string) :
        delete_index = -1
        for index, enemy in enumerate(self.enemies) :
            # print(enemy.text, input_string)
            if enemy.text == input_string :
                delete_index = index
                x = enemy.x
                y = enemy.y
                break
                    
        if delete_index != -1 :
            self.booms.append(boom_object(x, y))
            del self.enemies[index]
            return True
    
        return False

    def move(self) :
        crashed = False

        self.move_count += 1
        if self.move_count > DOWN_SPEED :
            for i, enemy in enumerate(self.enemies) :
                enemy.move()
                if enemy.is_out_of_range() == True :
                    self.delete_indexes.append(i)
                    crashed = True
            self.move_count = 0

        for index in self.delete_indexes :
            del self.enemies[index]

        self.delete_indexes = []        

        return crashed

    def draw(self) :
        for enemy in self.enemies :
            enemy.draw()

        for i in range(len(self.booms)) :
            boom = self.booms.pop(0)
            if boom.draw() == True :
                self.booms.append(boom)

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
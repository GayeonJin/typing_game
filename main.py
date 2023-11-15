#!/usr/bin/python

import sys
import pygame
import random
from time import sleep

import csv
from io import StringIO

from gobject import *
from gresource import *

TITLE_STR = "Typing Game"

SCORE_UNIT = 10
LIFE_COUNT = 3

STATUS_XOFFSET = 10
STATUS_YOFFSET = 5

INPUTTEXT_YOFFSET = 30

DOWN_SPEED = 20
ENEMY_CREATION_SPEED = 80
ENEMY_MAX = 5

test_word_str = 'Acted, Adapted, Combined, Composed, Conceptualized, Condensed, Created, Customized, Designed, Developed, \
                Devised, Directed, Displayed, Entertained, Established, Fashioned, Formulated, Founded, Illustrated, Initiated, \
                Instituted, Integrated, Introduced, Invented, Modeled, Modiﬁed, Originated, Performed, Photographed, Planned, \
                Revised, Revitalized, Shaped, Solve'    

def draw_life(count) :
    font = pygame.font.SysFont(None, 25)
    text = font.render("Life : " + str(count), True, COLOR_WHITE)
    text_rect = text.get_rect()
    gctrl.surface.blit(text, (gctrl.width - text_rect.width - STATUS_XOFFSET, STATUS_YOFFSET))

def draw_score(count) :
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score : " + str(count), True, COLOR_WHITE)
    gctrl.surface.blit(text, (10, STATUS_YOFFSET))

def draw_inputtext(str) :
    font = pygame.font.Font('freesansbold.ttf', 25)
    text_suf = font.render(str, True, COLOR_WHITE)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))
    text_rect.top = gctrl.height - INPUTTEXT_YOFFSET
    gctrl.surface.blit(text_suf, text_rect)    

def game_over() :
    font = pygame.font.Font('freesansbold.ttf', 80)
    text_suf = font.render('Game Over', True, COLOR_RED)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))

    gctrl.surface.blit(text_suf, text_rect)
    pygame.display.update()
    sleep(2)
    run_game()

def terminate() :
    pygame.quit()
    sys.exit()

def run_game() :
    global clock
    global bg_img, boom_img
    global snd_shot, snd_explosion

    start_game()

    test_dic = []
    f = StringIO(test_word_str)
    reader = csv.reader(f, delimiter=',')
    for rows in reader :
        for word in rows :
            word = word.strip()
            word = word.lower()
            test_dic.append(word)

    enemies = []
    delete_indexes = []
    max_enemy = ENEMY_MAX

    booms = []

    input_str = ''

    tick = 0
    enemy_tick = 0
    score = 0
    life = LIFE_COUNT
    crashed = False
    while not crashed :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                crashed = True

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_F10 :
                    gctrl.save_scr_capture(TITLE_STR)

            if event.type == pygame.KEYUP :
                if event.key >= pygame.K_a and event.key <= pygame.K_z :
                    input_str = input_str + "%c"%event.key
                    #print(input_str)
                elif event.key == pygame.K_BACKSPACE :
                    if len(input_str) > 0 :
                        input_str = input_str[slice(-1)]
                        #print(input_str)
                elif event.key == pygame.K_RETURN :
                    delete_index = -1
                    for index, enemy in enumerate(enemies) :
                        # print(enemy.text, input_str)
                        if enemy.text == input_str :
                            delete_index = index
                            x = enemy.x
                            y = enemy.y
                            break
                    
                    if delete_index != -1 :
                        booms.append(boom_object(x, y))
                        del enemies[index]
                        score += 10

                    input_str = ''
                elif event.key == pygame.K_F10 :
                    gctrl.save_scr_capture(TITLE_STR)

        # Clear gamepad
        gctrl.surface.fill(COLOR_WHITE)

        # Draw background
        gctrl.surface.blit(bg_img, (0, 0))

        # Draw test
        if len(input_str) > 0 :
            draw_inputtext(input_str)

        # Create enemy
        enemy_tick += 1
        if enemy_tick > ENEMY_CREATION_SPEED :
            enemy_tick = 0
        
            if len(enemies) < max_enemy :
                random.shuffle(test_dic)
                enemies.append(enemy_object(test_dic[0]))

        # Move enemy
        tick += 1
        if tick > DOWN_SPEED :
            for i, enemy in enumerate(enemies) :
                enemy.move()
                if enemy.is_out_of_range() == True :
                    delete_indexes.append(i)
                    life -= 1
            tick = 0

        for index in delete_indexes :
            del enemies[index]

        delete_indexes = []

        # Draw enemy
        for enemy in enemies :
            enemy.draw()

        for i in range(len(booms)) :
            boom = booms.pop(0)
            if boom.draw() == True :
                booms.append(boom)

        # Draw Score
        draw_score(score)
        draw_life(life)

        pygame.display.update()
        clock.tick(60)

        if life <= 0 :
            game_over()
            crashed = True

    terminate()

def start_game() :
    # Clear gamepad
    gctrl.surface.fill(COLOR_WHITE)

    font1 = pygame.font.SysFont(None, 40)
    text_suf1 = font1.render("press any key", True, COLOR_RED)
    text_rect1 = text_suf1.get_rect()
    text_rect1.top = gctrl.height / 2
    text_rect1.centerx = gctrl.width / 2
    gctrl.surface.blit(text_suf1, text_rect1)
    
    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

        pygame.display.update()
        clock.tick(60)    
       
def init_game() :
    global clock
    global bg_img, boom_img
    global snd_shot, snd_explosion

    # initialize
    pygame.init()
    clock = pygame.time.Clock()
    
    # backgroud and screen
    bg_img = pygame.image.load(get_img_resource('id_background'))

    pad_width = bg_img.get_width()
    pad_height = bg_img.get_height()

    gctrl.set_surface(pygame.display.set_mode((pad_width, pad_height)))
    pygame.display.set_caption(TITLE_STR)

    # sound resource
    snd_shot = pygame.mixer.Sound(get_snd_resource('snd_shot'))
    snd_explosion = pygame.mixer.Sound(get_snd_resource('snd_explosion'))   

if __name__ == '__main__' :
    init_game()
    run_game()


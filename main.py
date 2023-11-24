#!/usr/bin/python

import sys
import pygame
import random
from time import sleep

from gobject import *
from gresource import *

TITLE_STR = "Typing Game"

SCORE_UNIT = 10
LIFE_COUNT = 3

STATUS_XOFFSET = 10
STATUS_YOFFSET = 5

INPUTTEXT_YOFFSET = 30

ALIGN_LEFT = 0x01
ALIGN_RIGHT = 0x02
ALIGN_CENTER = 0x04
ALIGN_BOTTOM = 0x10
ALIGN_TOP = 0x20

class game :
    def __init__(self) :
        # initialize pygame
        pygame.init()
        self.clock = pygame.time.Clock()
    
        # backgroud and screen
        self.bg_img = pygame.image.load(get_img_resource('id_background'))

        pad_width = self.bg_img.get_width()
        pad_height = self.bg_img.get_height()

        gctrl.set_surface(pygame.display.set_mode((pad_width, pad_height)))
        pygame.display.set_caption(TITLE_STR)

        # sound resource
        self.snd_shot = pygame.mixer.Sound(get_snd_resource('snd_shot'))
        self.snd_explosion = pygame.mixer.Sound(get_snd_resource('snd_explosion'))   

    def terminate(self) :
        pygame.quit()
        sys.exit()

    def draw_string(self, str, x_offset = 0, y = 0, align = ALIGN_LEFT) :
        font = pygame.font.SysFont(None, 25)
        text = font.render(str, True, COLOR_WHITE)
        text_rect = text.get_rect()

        if align == ALIGN_LEFT :
            gctrl.surface.blit(text, (x_offset, y))
        elif align == ALIGN_RIGHT :
            gctrl.surface.blit(text, (gctrl.width - text_rect.width - x_offset, y))

    def draw_life(self, count) :
        self.draw_string("Life : " + str(count), STATUS_XOFFSET, STATUS_YOFFSET, ALIGN_RIGHT)

    def draw_score(self, count) :
        self.draw_string("Score : " + str(count), STATUS_XOFFSET, STATUS_YOFFSET, ALIGN_LEFT)

    def draw_inputtext(self, str) :
        if len(str) > 0 :
            font = pygame.font.Font('freesansbold.ttf', 25)
            text_suf = font.render(str, True, COLOR_WHITE)
            text_rect = text_suf.get_rect()
            text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))
            text_rect.top = gctrl.height - INPUTTEXT_YOFFSET
            gctrl.surface.blit(text_suf, text_rect)    

    def game_over(self) :
        font = pygame.font.Font('freesansbold.ttf', 80)
        text_suf = font.render('Game Over', True, COLOR_RED)
        text_rect = text_suf.get_rect()
        text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))

        gctrl.surface.blit(text_suf, text_rect)
        pygame.display.update()
        sleep(2)
        self.run_game()

    def start_game(self) :
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
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.terminate()
                    return

            pygame.display.update()
            self.clock.tick(60)    

    def run_game(self) :
        self.start_game()

        input_str = ''

        enemy_ctrl = enemy_group()

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
                        if enemy_ctrl.compare(input_str) == True :
                            score += 10

                        input_str = ''
                    elif event.key == pygame.K_F10 :
                        gctrl.save_scr_capture(TITLE_STR)

            # Clear gamepad
            gctrl.surface.fill(COLOR_WHITE)

            # Draw background
            gctrl.surface.blit(self.bg_img, (0, 0))

            # Draw test
            self.draw_inputtext(input_str)

            # Create enemy
            enemy_ctrl.create()

            # Move enemy
            if enemy_ctrl.move() == True :
                life -= 1

            # Draw enemy
            enemy_ctrl.draw()

            # Draw Score
            self.draw_score(score)
            self.draw_life(life)

            pygame.display.update()
            self.clock.tick(60)

            if life <= 0 :
                self.game_over()
                crashed = True

        self.terminate()

if __name__ == '__main__' :
    typing_game = game() 
    typing_game.run_game()


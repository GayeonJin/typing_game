#!/usr/bin/python

import sys
import pygame
import random
from time import sleep

from dic_data import *
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

class player :
    def __init__(self) :
        self.life = LIFE_COUNT
        self.score = 0

    def update_score(self) :
        self.score += SCORE_UNIT

    def kill_life(self) :
        self.life -= 1

    def is_game_over(self) :
        if self.life <= 0 :
            return True
        else : 
            return False

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

    def draw_string(self, str, x_offset = 0, y = 0, align = ALIGN_LEFT, font_size = 25, font_color = COLOR_WHITE) :
        font = pygame.font.SysFont(None, font_size)
        text = font.render(str, True, font_color)
        text_rect = text.get_rect()

        text_rect.top = y
        if align & ALIGN_LEFT :
            text_rect.left = x_offset    
        elif align & ALIGN_RIGHT :
            text_rect.left = gctrl.width - text_rect.width - x_offset
        elif align & ALIGN_CENTER :
            text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))

        if align & ALIGN_TOP :
            text_rect.top = INPUTTEXT_YOFFSET
        elif align & ALIGN_BOTTOM :
            text_rect.top = gctrl.height - INPUTTEXT_YOFFSET
        
        gctrl.surface.blit(text, text_rect)

    def draw_life(self, count) :
        self.draw_string("Life : " + str(count), STATUS_XOFFSET, STATUS_YOFFSET, ALIGN_RIGHT)

    def draw_score(self, count) :
        self.draw_string("Score : " + str(count), STATUS_XOFFSET, STATUS_YOFFSET, ALIGN_LEFT)

    def draw_inputtext(self, str) :
        if len(str) > 0 :
            self.draw_string(str, 0, INPUTTEXT_YOFFSET, ALIGN_CENTER | ALIGN_BOTTOM)

    def game_over(self) :
        self.draw_string('Game Over', 0, 0, ALIGN_CENTER, 80, COLOR_RED)
        pygame.display.update()
        sleep(2)
        self.run_game()

    def start_game(self) :
        # Clear gamepad
        gctrl.surface.fill(COLOR_WHITE)
        self.draw_string("press any key", 0, 0, ALIGN_CENTER, 40, COLOR_RED)

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

        game_player = player()
        enemy_ctrl = enemy_group(test_word_str)

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
                            game_player.update_score()

                        input_str = ''
                    elif event.key == pygame.K_F10 :
                        gctrl.save_scr_capture(TITLE_STR)

            # Clear gamepad
            gctrl.surface.fill(COLOR_WHITE)

            # Draw background
            gctrl.surface.blit(self.bg_img, (0, 0))

            # Draw text
            self.draw_inputtext(input_str)

            # Create and move enemy
            enemy_ctrl.create()
            if enemy_ctrl.move() == True :
                game_player.kill_life()

            # Draw enemy
            enemy_ctrl.draw()

            # Draw Score
            self.draw_score(game_player.score)
            self.draw_life(game_player.life)

            pygame.display.update()
            self.clock.tick(60)

            if game_player.is_game_over() == True :
                self.game_over()
                crashed = True

        self.terminate()

if __name__ == '__main__' :
    typing_game = game() 
    typing_game.run_game()


#!/usr/bin/python

import sys
import pygame
import random
from time import sleep

from dic_data import *
from gobject import *
from gresource import *

TITLE_STR = "Typing Game"

class player :
    SCORE_UNIT = 10
    LIFE_COUNT = 3

    STATUS_XOFFSET = 10
    STATUS_YOFFSET = 5

    def __init__(self) :
        self.life = player.LIFE_COUNT
        self.score = 0

    def update_score(self) :
        self.score += player.SCORE_UNIT

    def kill_life(self) :
        self.life -= 1

    def is_game_over(self) :
        if self.life <= 0 :
            return True
        else : 
            return False

    def draw_life(self, count) :
        gctrl.draw_string("Life : " + str(count), player.STATUS_XOFFSET, player.STATUS_YOFFSET, ALIGN_RIGHT)

    def draw_score(self, count) :
        gctrl.draw_string("Score : " + str(count), player.STATUS_XOFFSET, player.STATUS_YOFFSET, ALIGN_LEFT)

class game :
    INPUTTEXT_YOFFSET = 30

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

    def draw_inputtext(self, str) :
        if len(str) > 0 :
            gctrl.draw_string(str, 0, game.INPUTTEXT_YOFFSET, ALIGN_CENTER | ALIGN_BOTTOM)

    def game_over(self) :
        gctrl.draw_string('Game Over', 0, 0, ALIGN_CENTER, 80, COLOR_RED)
        pygame.display.update()
        sleep(2)
        self.run_game()

    def start_game(self) :
        # Clear gamepad
        gctrl.surface.fill(COLOR_WHITE)
        gctrl.draw_string("press any key", 0, 0, ALIGN_CENTER, 40, COLOR_RED)

        while True :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.terminate()
                    return

            pygame.display.update()
            self.clock.tick(FPS)    

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
            game_player.draw_score(game_player.score)
            game_player.draw_life(game_player.life)

            pygame.display.update()
            self.clock.tick(FPS)

            if game_player.is_game_over() == True :
                self.game_over()
                crashed = True

        self.terminate()

if __name__ == '__main__' :
    typing_game = game() 
    typing_game.run_game()


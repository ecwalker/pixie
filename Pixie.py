# -*- coding: utf-8 -*-
"""
Pixie

Created on Mon Jun 22 15:54:38 2020

@author: ecwal
"""

import pygame
from sys import exit
import random
import time
from Character import Character
import pygame_functions as pg
import dialogue as d

#initialise pygame
pygame.init()
mainloop = True
fishing_hole_loop = True
bag_loop = False
dialogue_iterator = []
dialogue_text = ""

#game_clock = pygame.time.Clock

#Settings
width = 800
height = 600
#FPS = 30
font = pygame.font.Font('freesansbold.ttf', 20)
small_font = pygame.font.Font('freesansbold.ttf', 12)

#Create screen
screen = pygame.display.set_mode((width, height)) #width, height

#Title & Icon
pygame.display.set_caption('Pixie')
icon = pygame.image.load('fairyR.png')
pygame.display.set_icon(icon)

#coin icon
coinImg = pygame.image.load('coin.png')
purse_value = 0

textX = 25
textY = 5

def show_purse(x, y) :
    purse = font.render(str(purse_value), True, (255, 255, 255))
    screen.blit(purse, (x, y))

#Player
player = Character('fairyR.png', 300, 300, 64)

#Non-playable characters
wizard = Character('wizard.png', 250, 112, 64) #Check size...
frog = Character('frog.png', 750, 325, 24)

#Empty Bag
X = []
Y = []
capacity = 16
slot_size = 80 #where X=Y
y1 = height - (slot_size + 5)
y2 = height - (slot_size + 5)
for i in range(capacity) :
    if i < 8 :
        X.append(width - (slot_size + 5))
        Y.append(y1)
        y1 -= (slot_size + 5)
    else :
        X.append(width - 2 * (slot_size + 5))
        Y.append(y2)
        y2 -= (slot_size + 5)
bag = []
flying_fish = pygame.image.load('flying_fish.png')
crab = pygame.image.load('crab.png')
river_eel = pygame.image.load('eel.png')

#Village objects
lake = pygame.image.load('lake.png')
hut = pygame.image.load('hut.png')
box = pygame.image.load('dialogue_box.png')

#Wizard's shop
price_dict = {}
price_dict['flying fish'] = 1
price_dict['crab'] = 50
price_dict['rare river eel'] = 350

#Fishing hole
fishing_hole = (600, 450)
fishing = False
end_fish = 0
species = ""

#Game stage and state
start = True
in_dialogue = False

#Game loop 
while mainloop :
    #game_clock.tick(FPS)
    screen.fill((200, 200, 200))
    
    #Dialogue
    if start :
        dialogue_iterator = iter(d.game_start)
        dialogue_text = next(dialogue_iterator)
        start = False
        in_dialogue = True
    
    if fishing_hole_loop : 
        screen.fill((2, 209, 30))
        screen.blit(coinImg, (5, 5))
        show_purse(textX, textY)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN :
                key_move = 0.5
                if in_dialogue :
                    if event.key == pygame.K_RETURN :
                        try :
                            dialogue_text = next(dialogue_iterator)
                        except StopIteration :
                            in_dialogue = False
                else :
                    if event.key == pygame.K_2 : #Change screen
                        fishing_hole_loop = False
                        bag_loop = True
                    #Player movement:
                    if event.key == pygame.K_LEFT :
                        player.X_change -= key_move
                        player.change_img('fairyL.png')
                        fishing = False
                    elif event.key == pygame.K_RIGHT :
                        player.X_change += key_move
                        player.change_img('fairyR.png')
                        fishing = False
                    elif event.key == pygame.K_UP :
                        player.Y_change -= key_move
                        fishing = False
                    elif event.key == pygame.K_DOWN :
                        player.Y_change += key_move
                        fishing = False
                    elif event.key == pygame.K_f : #Initiate fishing
                        if pg.collision(player.X, player.Y, fishing_hole[0], fishing_hole[1], 60) :
                            player.change_img('fairy_fishing.png')
                            fishing = True
                    elif event.key == pygame.K_s : #Speak
                        if pg.collision(player.X, player.Y, wizard.X, wizard.Y, 50) :
                            in_dialogue = True #Speaking to wizard
                            dialogue_iterator =  iter(d.speak_wizard)
                            dialogue_text = next(dialogue_iterator)
                            purse_value += pg.sell_all(bag, price_dict)
                            bag = []
                        if pg.collision(player.X, player.Y, frog.X, frog.Y, 75) :
                            pygame.mixer.music.load('frog.mp3')
                            pygame.mixer.music.play()
                            in_dialogue = True
                            dialogue_iterator = iter(d.speak_frog)
                            dialogue_text = next(dialogue_iterator)
            elif event.type == pygame.KEYUP : #Stops player movement
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                    player.X_change = 0
                if event.key == pygame.K_UP or pygame.K_DOWN :
                    player.Y_change  = 0
        #Update Coordinates:
        player.update_coord()
        #Fishing
        if fishing == True :
            if end_fish == 0 :
                start_fish = time.time()
                catch_sec = random.randint(30, 60)
                end_fish = start_fish + catch_sec
                catch = random.randint(1, 100)
                if catch < 50 :
                    species = "flying fish"
                elif catch < 80 :
                    species = "crab"
                else :
                    species = "rare river eel"
            if time.time() >= end_fish :
                if len(bag) < capacity :
                    bag.append(species)
                end_fish = 0
                fishing = False
                player.change_img('fairyR.png')
                pygame.mixer.music.load('fish.mp3')
                pygame.mixer.music.play()
                in_dialogue = True
                dialogue_iterator = iter(d.catch_fish)
                dialogue_text = next(dialogue_iterator)
        #Keep moveable objects in bounds (player)
        player.X_in_bounds(width)
        player.Y_in_bounds(height)
        #Render fishing hole
        pg.show_object(450, 100, lake, screen)
        pg.show_object(wizard.X, wizard.Y, wizard.img, screen)
        pg.show_object(100, 50, hut, screen)
        pg.show_object(frog.X, frog.Y, frog.img, screen)
        pygame.draw.rect(screen, (200, 200, 9), (fishing_hole[0], fishing_hole[1], 5, 5)) #Rect -> (X, Y, width, height)
        #Render player
        player.show(screen)
        #Dialogue box
        if in_dialogue :
            pg.show_object(-68, 450, box, screen)
            dialogue_box = font.render(dialogue_text, True, (255, 255, 255))
            press_enter = small_font.render("Press enter to continue...", True, (255, 255, 255))
            screen.blit(dialogue_box, (75, 525))
            screen.blit(press_enter, (625, 575))
        
    if bag_loop :
        screen.fill((200, 200, 200))
        press_1 = small_font.render("Press 1 to return to fishing hole.", True, (255, 255, 255))
        screen.blit(press_1, (10, 575))
        for i in range(capacity) :
            pygame.draw.rect(screen, (200, 200, 9), (X[i], Y[i], 80, 80), 1) #Rect -> (X, Y, width, height)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_1 :
                    fishing_hole_loop = True
                    bag_loop = False
        for i in range(len(bag)) :
            if bag[i] == "flying fish" :
                pg.show_object(X[i] + 5, Y[i] + 5, flying_fish, screen)
            elif bag[i] == "crab" :
                pg.show_object(X[i] + 5, Y[i] + 5, crab, screen)
            else :
                pg.show_object(X[i] + 5, Y[i] + 5, river_eel, screen)

    pygame.display.flip()
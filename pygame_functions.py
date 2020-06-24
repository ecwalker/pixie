# -*- coding: utf-8 -*-
"""
Pygame Useful Functions

Created on Sun Jun 21 11:55:44 2020

@author: ecwal
"""

import math
import time
import random

#Object Movement
def random_movement(direction, move) :
    """For random object movement (N, NE, E, SE, S, SW, NW) 
    Args: 
        direction: Random number from 1 to 8
        move: Distance to move per game loop
        
    Returns: tuple of (X_change, Y-change)"""
    
    if direction == 1 : #Move N
        return (0, -move)
    elif direction == 2 : #Move NE
        return (move, -move)
    elif direction == 3 : #Move E
        return (move, 0)
    elif direction == 4 : #Move SE
        return (move, move)
    elif direction == 5 : #Move S
        return (0, move)
    elif direction == 6 : #Move SW
        return (-move, move)
    elif direction == 7 : #Move W
        return (-move, 0)
    elif direction == 8 : #Move NW
        return (-move, -move)


#Object Collision
def collision(X1, Y1, X2, Y2, collision_boundary): 
    """Calculates distance between two objects and then determines whether they are in contact
    
    Args:
        X1: Object 1 X co-ordinate
        Y1: Object 1 Y co-ordinate
        X2: Object 2 X co-ordinate
        Y2: Object 2 Y co-ordinate
        collision_boundary: Distance between objects which defines collision boundary
            
    Returns: Boolean"""
    
    distance = math.sqrt(math.pow(X1 - X2, 2) 
    + math.pow(Y1 - Y2, 2))
    if distance < collision_boundary :
        return True 
    else :
        return False

#Keep object in bounds
def X_in_bounds(X, size, width):
    """Check X coordinate is within pygame window and readjust where necessary
    
    Args:
        X - Current X coordinate
        size - size of object (pixels)
        width - width of pygame window (pixels)
    
    Returns : 
        X - adjusted X coordinate
    """
    if X <= 0 :
        X = 0
    elif X >= width - size : #(width - image pixels)
        X = width - size
    #else :
        #X = X

def Y_in_bounds(Y, size, height) :
    """Check Y coordinate is within pygame window and readjust where necessary
    
    Args:
        Y - Current Y coordinate
        size - size of object (pixels)
        height - height of pygame window (pixels)
    
    Returns : 
        Y - adjusted Y coordinate
    """
    if Y <= 0 :
        Y = 0
    elif Y >= height - size : #(height - image pixels)
        Y = height - size
    #else :
        #Y = Y

#Spawn Object
def spawn_object(spawnX, last_pickup, spawn_status, respawn_time) :
    """Spawns an object by adjusting X cooridinate of spawn object based on epoch time of last pick up
   
    Args:
        spawnX - X coordinate of spawn item
        last_pickup - time.time() of last pick up
        spawn_status - status (start, ready, waiting)
        respawn_time - time between pick up and respawn (seconds)
      
    Returns:
        spawnX - re-adjusted to spawn point if respawn time has passed since last pick up
    """
    if spawn_status == 'waiting' :
        if last_pickup < (time.time() - respawn_time) :
            spawn_status = 'ready'
            spawnX += 2000
            
    """Object pick-up
    elif in_contact(playerX, playerY, seed_spawnX, seed_spawnY) :
            seed_value += 1
            seed_last_pickup = time.time()
            seed_spawn_status = 'waiting'
            seed_spawnX -= 2000 """

#Draw object
def show_object(X, Y, img, screen) :
    screen.blit(img, (X, Y))

#Go fishing
def catch_time(fishing) :
    if fishing == True :
        start_fish = time.time()
        catch_sec = random.randint(30, 60)
        return start_fish + catch_sec
    

def catch_species(fishing) :
    if fishing == True :
        catch = random.randint(1, 100)
        if catch < 80 :
            return "fish_a"
        elif catch < 99 :
            return "fish_b"
        else :
            return "fish_c"
        
def sell_all(bag, price_dict):
    price = []
    for i in range(len(bag)) :
        price.append(price_dict[bag[i]])
    return sum(price)
    
            

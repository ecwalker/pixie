# -*- coding: utf-8 -*-
"""
Character Class

Created on Mon Jun 22 18:50:31 2020

@author: ecwal
"""
import pygame

#Game settings
#width = 800
#height = 600

class Character :
    def __init__(self, img, X, Y, size, X_change=0, Y_change=0) :
        self.img = pygame.image.load(img)
        self.X = X
        self.Y = Y
        self.size = size
        self.X_change = X_change
        self.Y_change = Y_change
        
    
    def change_img(self, new_image) :
        self.img = pygame.image.load(new_image)
        
    def show(self, screen) :
        screen.blit(self.img, (self.X, self.Y))
    
    def update_coord(self) :
        self.X += self.X_change
        self.Y += self.Y_change
        
    def X_in_bounds(self, width):
        """Check X coordinate is within pygame window and readjust where necessary
        
        Args:
            X - Current X coordinate
            size - size of object (pixels)
            width - width of pygame window (pixels)
        
        Returns:
            X - adjusted X coordinate"""
        if self.X <= 0 :
            self.X = 0
        elif self.X >= width - self.size : #(width - image pixels)
            self.X = width - self.size

    def Y_in_bounds(self, height) :
        """Check Y coordinate is within pygame window and readjust where necessary
        
        Args:
            Y - Current Y coordinate
            size - size of object (pixels)
            height - height of pygame window (pixels)
        
        Returns : 
            Y - adjusted Y coordinate"""
        if self.Y <= 0 :
            self.Y = 0
        elif self.Y >= height - self.size : #(height - image pixels)
            self.Y = height - self.size
    
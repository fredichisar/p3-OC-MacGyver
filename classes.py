#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""Classes of MacGyver maze"""

import pygame
from pygame.locals import *
from constants import *
from random import sample, choice


class Level:
    """Class to create a level (map)"""

    def __init__(self, file):
        self.file = file
        self.structure = 0

    def create(self):
        """Method to create a level from a file.
        We create a global list containing a list per line to display"""
        # Open the file
        with open(self.file, "r") as file:
            level_structure = []
            # Travel across file lines
            for line in file:
                level_line = []
                # Travel across sprites (letters) inside the file
                for sprite in line:
                    # Ignore "\n" from end lines
                    if sprite != '\n':
                        # Add sprites to the line list
                        level_line.append(sprite)
                # Add line to level list
                level_structure.append(level_line)
            # Save the level structure
            self.structure = level_structure

            # Select randomly 3 lines
            rand_lines = sample([r for r in range(len(self.structure))], 3)

            # Select randomly a 0 from 1st random line
            ether = sample([i for i, val in enumerate(
                self.structure[rand_lines[0]]) if '0' in val], 1)
            # Select randomly a 0 from 2nd random line
            needle = sample([i for i, val in enumerate(
                self.structure[rand_lines[1]]) if '0' in val], 1)
            # Select randomly a 0 from 3rd random line
            plastic_tube = sample([i for i, val in enumerate(
                self.structure[rand_lines[2]]) if '0' in val], 1)

            # Replace old 0 by our items letters
            self.structure[rand_lines[0]][ether[0]] = 'e'
            self.structure[rand_lines[1]][needle[0]] = 'n'
            self.structure[rand_lines[2]][plastic_tube[0]] = 'p'

    def display(self, window):
        """Method to display the level from the list returned by create()"""
        # Load assets
        wall = pygame.image.load(img_wall).convert()
        finish = pygame.image.load(img_guardian).convert_alpha()
        ether = pygame.image.load(image_ether).convert_alpha()
        needle = pygame.image.load(image_needle).convert_alpha()
        plastic_tube = pygame.image.load(image_plastic_tube).convert_alpha()
        syringe = pygame.image.load(image_syringe).convert_alpha()

        # Travel across level list
        lin_number = 0
        for line in self.structure:
            # Travel across line lists
            num_case = 0
            for sprite in line:
                # Compute real position in pixels
                x = num_case * sprite_size
                y = lin_number * sprite_size
                if sprite == 'w':  # w = Wall
                    window.blit(wall, (x, y))
                elif sprite == 'f':  # f = Finish
                    window.blit(finish, (x, y))
                elif sprite == 'e':  # e = Ether
                    window.blit(ether, (x, y))
                elif sprite == 'n':  # n = Needle
                    window.blit(needle, (x, y))
                elif sprite == 'p':  # f = Plastic tube
                    window.blit(plastic_tube, (x, y))
                elif sprite == 'g':  # f = Plastic tube
                    window.blit(syringe, (x, y))
                num_case += 1
            lin_number += 1


class Player:
    """Class to create a character"""

    def __init__(self, img, level):
        # Character sprites
        self.character = pygame.image.load(img_mac_gyver).convert_alpha()

        # Character posdition in boxes and and pixels
        self.case_x = 0
        self.case_y = 0
        self.x = 0
        self.y = 0
        # Default direction
        self.direction = self.character
        # Character level
        self.level = level

    def deplacer(self, direction):
        """Method to move the character"""

        # Move to the right
        if direction == 'right':
            # Check for screen size
            if self.case_x < (sprite_side_number - 1):
                # Check next box isn't a wall
                if self.level.structure[self.case_y][self.case_x+1] != 'w':
                    # Move for 1 box
                    self.case_x += 1
                    # Compute real position in pixels
                    self.x = self.case_x * sprite_size
            self.direction = self.character

        # Move to the left
        if direction == 'left':
            if self.case_x > 0:
                if self.level.structure[self.case_y][self.case_x-1] != 'w':
                    self.case_x -= 1
                    self.x = self.case_x * sprite_size
            self.direction = self.character

        # Move up
        if direction == 'up':
            if self.case_y > 0:
                if self.level.structure[self.case_y-1][self.case_x] != 'w':
                    self.case_y -= 1
                    self.y = self.case_y * sprite_size
            self.direction = self.character

        # Move down
        if direction == 'down':
            if self.case_y < (sprite_side_number - 1):
                if self.level.structure[self.case_y+1][self.case_x] != 'w':
                    self.case_y += 1
                    self.y = self.case_y * sprite_size
            self.direction = self.character

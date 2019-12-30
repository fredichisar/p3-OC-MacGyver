#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
MacGyver maze
An amazing game where MacGyver must collect a plastic tube, 
ether and needle to create a seringe by moving inside a maze 
and asleep the guardian to exit and win.

Python scripts
Fichiers : macgyvermaze.py, classes.py, constants.py, map, assets
"""

import pygame
from pygame.locals import *

from classes import *
from constants import *

pygame.init()

#Open Pygame window with properties from constants
window = pygame.display.set_mode((window_side, window_height))
#Game icon
icone = pygame.image.load(image_icon)
pygame.display.set_icon(icone)
#Game title
pygame.display.set_caption(window_title)


#Main loop
main_continue = 1
while main_continue:	
	#Display home screen
	home = pygame.image.load(img_home).convert()
	window.blit(home, (0,0))

	#Refresh screen
	pygame.display.flip()

	#Reset variables after each loop
	continue_playing = 1
	continue_home = 1

	#Home loop
	while continue_home:
	
		#Limit loop speed
		pygame.time.Clock().tick(30)
	
		for event in pygame.event.get():
		
			#If user exit, set all variables to 0 and close
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				continue_home = 0
				continue_playing = 0
				main_continue = 0
				#Level choice variable
				level_choice = 0
				
			elif event.type == KEYDOWN:				
				#Run level 1
				if event.key == K_F1:
					continue_home = 0	#Leave home screen
					level_choice = 'map'		#Load level file
         	

	#Ensure level choice is make
	if level_choice != 0:
		#Set background image
		fond = pygame.image.load(img_background).convert()

		#Create a level from 'map' file
		level = Level(level_choice)
		level.create()
		level.display(window)

		#Create a counter for items (needle, ether, plastic tube)
		items_count = 0

		#Create MacGyver character
		mg = Player(img_mac_gyver, level)

				
	#Game loop
	while continue_playing:
	
		#Loop speed limitation
		pygame.time.Clock().tick(30)
	
		for event in pygame.event.get():
		
			#If user press 'esc' from home menu, set variables to 0
			#To close the window
			if event.type == QUIT:
				continue_playing = 0
				main_continue = 0
		
			elif event.type == KEYDOWN:
				#If user press 'esc' we only return to the home menu
				if event.key == K_ESCAPE:
					continue_playing = 0
					
				#Direction keys
				elif event.key == K_RIGHT:
					mg.deplacer('right')
				elif event.key == K_LEFT:
					mg.deplacer('left')
				elif event.key == K_UP:
					mg.deplacer('up')
				elif event.key == K_DOWN:
					mg.deplacer('down')			
			
		#Detect position to increment items_counter
		if level.structure[mg.case_y][mg.case_x] == 'e':
			level.structure[mg.case_y][mg.case_x] = 0
			items_count += 1

		if level.structure[mg.case_y][mg.case_x] == 'n':
			level.structure[mg.case_y][mg.case_x] = 0
			items_count += 1

		if level.structure[mg.case_y][mg.case_x] == 'p':
			level.structure[mg.case_y][mg.case_x] = 0
			items_count += 1
		
		#Display syringe if items counter is = 3
		if items_count == 3:
			level.structure[15][1] = 'g'

		#Display new position
		window.blit(fond, (0,0))
		level.display(window)
		window.blit(mg.direction, (mg.x, mg.y))
		pygame.display.flip()

		#Lose -> Display lose screen
		if level.structure[mg.case_y][mg.case_x] == 'f' and items_count < 3:
			continue_playing = 0
			img_home = img_lose

		#Win -> Display Win screen
		if level.structure[mg.case_y][mg.case_x] == 'f' and items_count == 3:
			continue_playing = 0
			img_home = img_win

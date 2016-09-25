#!/usr/bin/env python3

import pygame
from gameobject import GameObject
import message
from sys import exit
import tkinter as tk
from tkinter import filedialog
from platform import system
import pickle

__name__ = "mapeditor.py"
__author__ = "Tristan Arthur"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0.0.0.1"
__maintainer__ = "Tristan Arthur"
__email__ = "roguesgonnasneak@gmail.com"
__status__ = "Prototype"

# TODO: Saving


def save(file_to_save, objects):
    file = open(file_to_save, "w+")
    save_to = []
    for game_object in objects:
        # Save all properties to a list
        save_to += ["{" + str(game_object.x) + "," + str(game_object.y) + "<" + str(game_object.sprite_locations) +
                    ">" + str(game_object.animation_speed) + ":" + str(game_object.move_speed) + "}"]
    file.writelines(save_to)

current_tile_creation_height = 0
current_tile_creation_width = 0
tile_map = {}
while current_tile_creation_height <= 650:
    while current_tile_creation_width <= 650:
        tile_map[current_tile_creation_width] = current_tile_creation_width
        current_tile_creation_width += 32
    current_tile_creation_height += 32

pygame.init()
clock = pygame.time.Clock()
SURFACE = pygame.display.set_mode((650, 650))
pygame.display.set_caption(__name__ + " " + __version__)

add_sprite_button = GameObject([pygame.image.load("assets/mapeditor/add_normal.png"),
                                pygame.image.load("assets/mapeditor/add_depressed.png")],
                               ["assets/mapeditor/add_normal.png", "assets/mapeditor/add_depressed.png"],
                               (600, 100), 0, 0)

save_sprite_button = GameObject([pygame.image.load("assets/mapeditor/save_button.png")],
                                ["assets/mapeditor/save_button.png"],
                                (600, 150), 0, 0)

block = GameObject([pygame.image.load("proto/blue_tile.png")], ["proto/blue_tile.png"], (50, 50), 0, 0)

msg = message.Messenger("log_mapeditor.txt")

ms_time = 0

blocks = []

# Needed to open file dialog for saving
if system() == "Windows":
    root = tk.Tk()
    root.withdraw()

while True:

    SURFACE.fill((0, 0, 0))

    msFrameElapsed = clock.tick(30)
    ms_time += msFrameElapsed

    msg.timed_save_log(ms_time)

    mouse_pos = pygame.mouse.get_pos()
    # block.x = mouse_pos[0]
    # block.y = mouse_pos[1]

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            # Exit PyGame and Python
            pygame.mixer.quit()
            pygame.font.quit()
            pygame.quit()

            msg.save_log()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Whether a button has been clicked, so know not to place block.
            button_click = False
            # Whether a block has already been placed in that tile. Reduces map file size
            block_overlap = False
            # On Left Click only
            if event.button == 1:
                if add_sprite_button.point_rectangle_collide((mouse_pos[0], mouse_pos[1])):
                    add_sprite_button.get_next_frame()
                    button_click = True
                if save_sprite_button.point_rectangle_collide((mouse_pos[0], mouse_pos[1])):
                    msg.log_debug("Saving map")
                    if system() == "Windows":
                        with open("map.pickle", "wb") as f:
                            pickle.dump(blocks, f)
                        # TODO File dialog crap
                        # save(filedialog.asksaveasfilename(defaultextension="mp"), blocks)
                    else:
                        with open("map.pickle", "wb") as f:
                            pickle.dump(blocks, f)
                    msg.log_debug("Finished saving map")
                    button_click = True

            for block in blocks:
                if block.point_rectangle_collide((mouse_pos[0], mouse_pos[1])):
                    block_overlap = True
                    # msg.log_error("Tile populated, could not place block there")

            if not button_click:
                # Used to change block placement
                x_temp = mouse_pos[0]
                # Make block x be placed in tiles of 32x32
                while not x_temp % 32 == 0:
                    x_temp -= 1

                y_temp = mouse_pos[1]
                while not y_temp % 32 == 0:
                    y_temp -= 1
                if not block_overlap:
                    blocks += [GameObject([pygame.image.load("proto/blue_tile.png")],
                                          ["proto/blue_tile.png"], (x_temp, y_temp), 0, 0)]
                else:
                    for block in blocks:
                        # On Right Click only
                        if block.x == x_temp and block.y == y_temp and event.button == 3:
                            blocks.remove(block)
                            break

    for block in blocks:
        SURFACE.blit(block.get_next_frame(), (block.x, block.y))
    SURFACE.blit(add_sprite_button.get_current_frame(), (add_sprite_button.x, add_sprite_button.y))
    SURFACE.blit(save_sprite_button.get_current_frame(), (save_sprite_button.x, save_sprite_button.y))

    pygame.display.update()

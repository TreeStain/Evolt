#!/usr/bin/env python3

# |----------| #
#   evolt.py   #
#  30/08/2016  #
# |----------| #

import pygame
from sys import exit
import message
from gameobject import GameObject
import map
import pickle

__name__ = "evolt.py"
__author__ = "Tristan Arthur"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0.0.0.2"
__maintainer__ = "Tristan Arthur"
__email__ = "roguesgonnasneak@gmail.com"
__status__ = "Prototype"

# TODO: Smoother jumps
# TODO: Change move speed to go off time not frames
# TODO: Finish rectangle on rectangle collision
# TODO: Load and display maps from file
# TODO:     Fix Serialization plz


# Function to detect collision between a rectangle and a rectangle
def rectangle_rectangle_collide():
    pass

# Initialise constants
WINDOW_WIDTH = 650
WINDOW_HEIGHT = 650


# Game Loop
def main():

    # Initialise PyGame
    pygame.init()
    clock = pygame.time.Clock()
    pygame.mixer.init()
    pygame.font.init()

    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Initialise & load objects
    player = GameObject([pygame.image.load("assets/player/leg_day.png")],
                        ["assets/player/leg_day.png"], ((WINDOW_WIDTH // 2) - 16, 50), 2000, 5)

    # game_map = map.Map("map_text.txt")
    with open("map.pickle", "rb") as f:
        objects = pickle.load(f)

    # for num in range(game_map.num_of_objects):
    #    objects += [GameObject([pygame.image.load(game_map.sprites[num])],
    #                           game_map.sprites[num], game_map.positions[num], game_map.animation_times[num],
    #                           game_map.move_times[num])]

    msg = message.Messenger("/log_evolt.txt", save_error=True)
    msg.log_debug(str(objects))
    msg.log_debug("Map loaded")
    msg.save_log()

    # Set caption for main window
    pygame.display.set_caption(__name__ + " " + __version__)

    # Start timer for game
    ms_time = 0

    # Initialise the variable for checking when player is jumping
    jump_in_progress = False

    # Initialise world skew variables
    world_skew_x = 0
    world_skew_y = 0

    # Initialise colour tuples
    _BLACK = (0, 0, 0)
    _WHITE = (255, 255, 255)
    _SKY_BLUE = (20, 100, 255)
    _RED = (255, 20, 20)

    while True:

        surface.fill(_BLACK)

        # Get time elapsed from last time
        ms_frame_elapsed = clock.tick(30)

        # Add the milliseconds since last frame to overall game time
        ms_time += ms_frame_elapsed

        # Get mouse position at start of frame
        # Uncommented, not being used
        # mouse_pos = pygame.mouse.get_pos()

        msg.timed_save_log(ms_time)

        # Get all keys pressed this frame
        keys = pygame.key.get_pressed()

        # Reset animation variables, tells when to play an animation
        player_running = False

        # If left arrow key has been pressed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            world_skew_x += player.move_speed
            player_running = True

        # If right arrow key has been pressed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            world_skew_x -= player.move_speed
            player_running = True

        # Reset fall frame variable
        fall_frame = False

        # If fall calculations have not taken place lower player by 5
        if not fall_frame:
            player.y += 5

        # Check for new events
        for event in pygame.event.get():

            # On 'X' press
            if event.type == pygame.QUIT:

                msg.log_debug("Exiting game due to user interaction")

                # Exit PyGame and Python
                pygame.mixer.quit()
                pygame.font.quit()
                pygame.quit()

                msg.save_log()
                exit()

            # On mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Get (x, y) coordinates of click & update mouse_pos
                pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not jump_in_progress:
                    player.y -= 75
                    jump_in_progress = True

        # Draw
        # For each tile in terrain class
        for tile in objects:
            # Display tile at appropriate x, y + player x, y/skew
            surface.blit(tile.get_current_frame(), (tile.x + world_skew_x, tile.y + world_skew_y))

        surface.blit(player.get_next_frame(ms_time, player_running), (player.x, player.y))

        # Update display
        pygame.display.update()

# TODO: Fix plz
if __name__ == "__main__":
    print("Hello")
    main()
else:
    print("World")
    main()

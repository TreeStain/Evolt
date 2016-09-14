# |----------| #
#   evolt.py   #
#  30/08/2016  #
# |----------| #

import pygame
from sys import exit
import message
from gameobject import GameObject
# Uncommented, not being used yet
# from random import randint

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
# TODO: Non-flat terrain
# TODO: Change move speed to go off time not frames
# TODO: Load and display maps from file


class Map(object):
    def __init__(self, file_to_load):
        map_raw = open(file_to_load).read()
        self.positions = []
        self.sprites = []
        self.animation_times = []
        self.move_times = []
        self.num_of_objects = 0
        start_pos = 0
        start_sprites = 0
        for i, char in enumerate(map_raw):
            if char == "{":
                start_pos = i
            if char == "<":
                pos = map_raw[start_pos + 1:i]
                pos = pos.split(",")
                self.positions += [[int(pos[0]), int(pos[1])]]
            if char == "[":
                start_sprites = i
            if char == "]":
                self.sprites += [map_raw[start_sprites + 1:i].strip("'")]
            if char == ":":
                self.animation_times += [int(map_raw[i - 1])]
                self.move_times += [int(map_raw[i + 1])]
        self.num_of_objects = len(self.positions)


# TODO: Fix text being an object
class Text(object):
    """
    Text structure class, holds text surface
    :rtype: pygame.font.Font
    """
    def __init__(self, font_location, text="Text", size=45, colour=(0, 0, 0)):
        fnt_text = pygame.font.Font(font_location, int(size))
        self.surface = fnt_text.render(text, True, colour)


# TODO: Finish rectangle on rectangle collision
# Function to detect collision between a rectangle and a rectangle
def rectangle_rectangle_collide():
    pass

# Initialise constants
WINDOW_WIDTH = 650
WINDOW_HEIGHT = 650

# Initialise PyGame
pygame.init()
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.font.init()

SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Initialise & load objects
current_player_surface = 0
player = GameObject([pygame.image.load("assets/player/leg_day.png")],
                    ["assets/player/leg_day.png"], ((WINDOW_WIDTH // 2) - 16, 50), 2000, 5)

game_map = Map("map_text.txt")
objects = []

for num in range(game_map.num_of_objects):
    objects += [GameObject([pygame.image.load(game_map.sprites[num])],
                           game_map.sprites[num], game_map.positions[num], game_map.animation_times[num],
                           game_map.move_times[num])]
print(objects)

msg = message.Messenger()

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

last_animation_time = 0

# Game Loop
while True:

    # Fill background with black (0, 0, 0)
    SURFACE.fill(_BLACK)
    
    # Get time elapsed from last time 
    msFrameElapsed = clock.tick(30)
    
    # Add the milliseconds since last frame to overall game time
    ms_time += msFrameElapsed

    # Get mouse position at start of frame
    # Uncommented, not being used
    # mouse_pos = pygame.mouse.get_pos()

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

    # Get the x, y values of all terrain tiles
    # for x, y in terrain.x_map.items():

        # If player x is in the bounds of the terrain
        # if x + world_skew_x <= player.x + 16 <= x + world_skew_x + 32:
            # If player is above terrain
            # if player.y + 66 <= y + world_skew_y:
                # player.y += 5
            # else:
                # jump_in_progress = False
            # Has fall calculations taken place this frame?
            # fall_frame = True
            # break

    # If fall calculations have not taken place lower player by 5
    if not fall_frame:
        player.y += 5

    # Check for new events
    for event in pygame.event.get():
    
        # On 'X' press
        if event.type == pygame.QUIT:
    
            # Exit PyGame and Python
            pygame.mixer.quit()
            pygame.font.quit()
            pygame.quit()
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
        SURFACE.blit(tile.get_current_frame(), (tile.x + world_skew_x, tile.y + world_skew_y))

    SURFACE.blit(player.get_next_frame(ms_time, player_running), (player.x, player.y))

    # Update display
    pygame.display.update()

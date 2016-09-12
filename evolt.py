# |----------| #
#   evolt.py   #
#  30/08/2016  #
# |----------| #

import pygame
from sys import exit
# Uncommented, not being used yet
# from random import randint

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


# TODO: fix debug and error display and save
class Messenger(object):

    def __init__(self, show_debug=True, show_error=True, save_debug=False, save_error=False):
        self.show_debug = show_debug
        self.show_error = show_error
        self.save_debug = save_debug
        self.save_error = save_error
        self.debug_to_save = []
        self.error_to_save = []

    def debug(self, msg):
        print(msg)
        if self.save_debug:
            self.debug_to_save += [msg]



class GameObject(object):
    """Game object : tracks coordinates, animations and surfaces"""

    def __init__(self, animation_locations, pos, animation_speed=30, move_speed=3):

        """
        Game Object, holds all data for objects that move and have animations and positions
        :param animation_locations:
        :param pos:
        :param animation_speed:
        :param move_speed:
        """

        # How many pixels the sprite will move per frame
        self.move_speed = move_speed

        # List of all the surfaces used for the object. Considered animation if more than 1.
        self.animation_locations = animation_locations
        
        # All surface objects
        self.surfaces = []

        # Set animation speed, ms change
        self.animation_speed = animation_speed
        
        for animation in self.animation_locations:
            # Add listed image as part of object animation
            self.surfaces += [pygame.image.load(animation)]
        self.x, self.y = pos

        # Current frame of sprite animation in use
        self.current_frame = 0

        # The last time in ms that a new sprite animation was displayed
        self.last_animation_time = 0

    def get_next_frame(self, ms_current_time, constant=True):
        if ms_current_time >= self.last_animation_time + self.animation_speed and constant:
            # Next player animation server
            self.current_frame += 1
            # set last animation time to current time
            self.last_animation_time = ms_current_time
            # If current animation is out of bounds
            if self.current_frame >= len(self.surfaces):
                # Go back to first animation surface
                self.current_frame = 0
        return self.surfaces[self.current_frame]

    def __iter__(self):
        yield from self.surfaces


# TODO: destructible terrain
class TerrainObject(object):
    def __init__(self, sprite_location, pos, destruct=True):
        """
        Terrain Object/Tile, holds the data of the individual tiles
        :param sprite_location:
        :param pos:
        :param destruct:
        """

        # Location of sprite used for Terrain Object
        self.sprite_location = sprite_location

        # Surface object for terrain tile
        self.surface = pygame.image.load(sprite_location)

        # Set whether the tile is destructible or not
        self.destruct = destruct

        self.x, self.y = pos


# TODO: Add dictionary instead of list for varying terrain heights in sections
# TODO: Save terrain dictionary into a file that can be loaded
class Terrain(object):

    blue_tile_surface = "proto/blue_tile_surface.png"
    blue_tile = "proto/blue_tile.png"

    def __init__(self, wanted_width, wanted_height, gen_height):
        """
        Terrain, holds all terrain tiles and their data in a dictionary
        :param wanted_width:
        :param wanted_height:
        :param gen_height:
        """

        # X map, x: y
        self.x_map = {}

        # Terrain tile dictionary
        self.terrain = []

        # Initialise the current terrain width to 0 and height to wanted generation height
        c_terrain_width, c_terrain_height = 0, gen_height

        # Initialise variable to store whether the surface is being created
        surface_create = True

        # While current terrain height is less than the wanted height ROW
        while c_terrain_height < wanted_height:

            # While current terrain width is less than the wanted width COLUMN
            while c_terrain_width < wanted_width:

                # If surface is being created
                if surface_create:

                    # Add tile y to x mapping
                    self.x_map[c_terrain_width] = c_terrain_height

                    # Add the terrain tile with surface sprite
                    self.terrain += [TerrainObject(Terrain.blue_tile_surface, (c_terrain_width, c_terrain_height))]
                else:

                    # Add terrain tile with ground sprite
                    self.terrain += [TerrainObject(Terrain.blue_tile, (c_terrain_width, c_terrain_height))]

                # Add sprite width to current terrain width
                c_terrain_width += 32

            # Stop creating surface
            surface_create = False

            # Reset current terrain width
            c_terrain_width = 0

            # Add sprite height to current terrain height
            c_terrain_height += 32

    def __iter__(self):
        yield from self.terrain


# TODO: Fix text being an object
class Text(object):
    """
    Text structure class, holds text surface
    :rtype: pygame.font.Font
    """
    def __init__(self, font_location, text="Text", size=45, colour=(0, 0, 0)):
        fnt_text = pygame.font.Font(font_location, int(size))
        self.surface = fnt_text.render(text, True, colour)


# Function to detect collision between a point and a rectangle
def point_rectangle_collide(surf, surf_pos, point):
    """
    Detects collision between a point and a rectangle
    :rtype: bool
    """
    if point[0] > surf_pos[0] < surf_pos[0] + surf.get_width() > point[0]:
        if point[1] > surf_pos[1] < surf_pos[1] + surf.get_height() > point[1]:
            return True
    return False


# TODO: Finish rectangle on rectangle collision
# Function to detect collision between a rectangle and a rectangle
def rectangle_rectangle_collide():
    pass

# Initialise constants
WINDOW_WIDTH = 650
WINDOW_HEIGHT = 650

# Initialise PyGame
pygame.init()

# Initialise PyGame clock
clock = pygame.time.Clock()

# Initialise PyGame music & sound
pygame.mixer.init()

# Initialise PyGame font & text
pygame.font.init()

# Create main surface for drawing
SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Initialise & load objects
current_player_surface = 0
player = GameObject(["proto/player/player_1.png", "proto/player/player_2.png", "proto/player/player_3.png",
                     "proto/player/player_4.png", "proto/player/player_5.png", "proto/player/player_6.png",
                     "proto/player/player_7.png"], ((WINDOW_WIDTH // 2) - 16, 50), 2000, 5)

terrain = Terrain(650, 650, 500)

# Set caption for main window
pygame.display.set_caption("Evolt V0.0.0.2")

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
    for x, y in terrain.x_map.items():

        # If player x is in the bounds of the terrain
        if x + world_skew_x <= player.x + 16 <= x + world_skew_x + 32:
            # If player is above terrain
            if player.y + 66 <= y + world_skew_y:
                player.y += 5
            else:
                jump_in_progress = False
            # Has fall calculations taken place this frame?
            fall_frame = True
            break

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
            mouse_pos = event.pos

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jump_in_progress:
                player.y -= 75
                jump_in_progress = True

    # Draw
    # For each tile in terrain class
    for terrain_tile in terrain:

        # Display tile at appropriate x, y + player x, y/skew
        SURFACE.blit(terrain_tile.surface, (terrain_tile.x + world_skew_x, terrain_tile.y + world_skew_y))

    SURFACE.blit(player.get_next_frame(ms_time, player_running), (player.x, player.y))

    # Update display
    pygame.display.update()

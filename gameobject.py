class GameObject(object):
    """Game object : tracks coordinates, animations and surfaces"""

    def __init__(self, surfaces, sprite_locations, pos, animation_speed=30, move_speed=3):

        """
        Game Object, holds all data for objects that move and have animations and positions
        :param surfaces:
        :param pos:
        :param animation_speed:
        :param move_speed:
        """

        # How many pixels the sprite will move per frame
        self.move_speed = move_speed

        self.surfaces = surfaces

        self.sprite_locations = sprite_locations

        # ms change between frames
        self.animation_speed = animation_speed

        self.x, self.y = pos

        # Current frame of sprite animation in use
        self.current_frame = 0

        # The last time in ms that a new sprite animation was displayed
        self.last_animation_time = 0

    def get_next_frame(self, ms_current_time=None, constant=True):
        # Get next frame without checking times, used for non-animated objects
        if ms_current_time is None:
            self.current_frame += 1
            if self.current_frame >= len(self.surfaces):
                self.current_frame = 0
            return self.surfaces[self.current_frame]
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

    def get_current_frame(self):
        return self.surfaces[self.current_frame]

    # Function to detect collision between a point and a rectangle
    def point_rectangle_collide(self, point):
        """
        Detects collision between a point and a rectangle
        :rtype: bool
        """
        if point[0] > self.x < self.x + self.surfaces[0].get_width() > point[0]:
            if point[1] > self.y < self.y + self.surfaces[0].get_height() > point[1]:
                return True
        return False

    # def __iter__(self):
    #    yield from self.surfaces

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

    def save(self, file_to_save):
        file = open(file_to_save, "w+")
        save_to = []

        for i in range(self.num_of_objects):
            save_to += ["{" + str(self.positions[i][0]) + "," + str(self.positions[i][1]) + "<" + str(self.sprites[i]) +
                        ">" + str(self.animation_times[i]) + ":" + str(self.move_times[i]) + "}"]
        file.writelines(save_to)

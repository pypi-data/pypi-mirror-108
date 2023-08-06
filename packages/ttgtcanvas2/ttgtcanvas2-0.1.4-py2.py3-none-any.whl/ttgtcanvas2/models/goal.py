class PositionGoal():
    def __init__(self, config):
        self.x = config.get("x")
        self.y = config.get("y")
    
    def is_completed(self, bot, world=None):
        return self.x == bot.x and self.y == self.y

    def msg(self):
        return "Reached Final Position: {},{}".format(self.x, self.y)

class WallGoal():
    def __init__(self, config):
        self.directions = config.get("walls", [])
        self.x  = config.get("x")
        self.y = config.get("y")
    
    def is_completed(self, bot, world=None):
        # return sorted(world.added_walls.get(self.xy, [])) == sorted(self.walls)
        cell = world.cells[self.x - 1][self.y - 1]
        return all(cell.has_block(direction) for direction in self.directions)

    def msg(self):
        return "Build walls at:  {}".format(self.xy)

class ObjectGoal():
    def __init__(self, config):
        self.obj_name = config.get("obj_name")
        self.x  = config.get("x")
        self.y = config.get("y")
        self.val  = config.get('val')

    def is_completed(self, bot, world=None):
        obj = bot.collections.get("{},{}".format(self.x, self.y), {})
        val = obj.get(self.obj_name, 0)
        return self.val == val

    def msg(self):
        return "Picked {} at: {},{}".format(self.obj_name, self.x, self.y)

class_list = {
    "position": PositionGoal,
    "wall": WallGoal,
    "object": ObjectGoal
}

class Goal(object):
    @staticmethod
    def load(klassType, config):
        klass = class_list.get(klassType)
        return klass(config)

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
        self.walls = config.get("walls", [])
        self.xy = config.get('xy')
    
    def is_completed(self, bot, world=None):
        return sorted(world.added_walls.get(self.xy, [])) == sorted(self.walls) 

    def msg(self):
        return "Build walls at:  {}".format(self.xy)

class ObjectGoal():
    def __init__(self, config):
        self.obj_name = config.get("obj_name")
        self.xy  = config.get("xy")
        self.val  = config.get('val')

    def is_completed(self, bot, world=None):
        obj = bot.collections.get(self.xy, {})
        val = obj.get(self.obj_name, 0)
        return self.val == val

    def msg(self):
        return "Picked {} at: {}".format(self.obj_name, self.xy)

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

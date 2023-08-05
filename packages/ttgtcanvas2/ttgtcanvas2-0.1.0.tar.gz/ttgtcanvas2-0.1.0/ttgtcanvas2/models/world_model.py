from .robot_model import RobotModel

class WorldModel():
    def __init__(self, kwargs):
        self.walls = kwargs.get('walls', {})
        self.robots_config = kwargs.get('robots', [])

        self.set_dimensions(kwargs)
        self.init_robots(self.robots_config)


    def init_robots(self, robots=[]):
        self.robots = [RobotModel(robot) for robot in robots]

    def set_dimensions(self, options={}):
        self.rows = options.get('rows',10)
        self.cols = options.get('cols', 10)
    
    def dimensions(self):
        return [self.rows, self.cols]
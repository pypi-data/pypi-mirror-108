class RobotModel():
    def __init__(self, kwargs):
        self.x = kwargs.get("x", 1)
        self.y = kwargs.get("y", 1)
        self.orientation = kwargs.get('orientation', 0)
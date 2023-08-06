import random
class RobotModel():
    def __init__(self, kwargs):
        self.x = kwargs.get("x", 1)
        self.y = kwargs.get("y", 1)
        self.orientation = kwargs.get('_orientation', 0)
        self.traceColor = kwargs.get('_trace_color', None)
        self.possible_initial_positions = kwargs.get('possible_initial_positions', None)
        if self.possible_initial_positions is not None: 
            pos = random.choice(self.possible_initial_positions)
            self.x = pos[0]
            self.y = pos[1]
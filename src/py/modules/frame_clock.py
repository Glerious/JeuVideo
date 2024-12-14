class FrameClock():
    def __init__(self):
        self.time = 0

    def update(self):
        self.time += 1

    def get(self):
        return self.time

frame_clock: FrameClock = FrameClock()
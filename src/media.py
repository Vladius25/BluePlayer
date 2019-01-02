class MediaController:

    def __init__(self, device):
        self.device = device

    def play(self):
        self.device.Play()

    def stop(self):
        self.device.Stop()

    def next(self):
        self.device.Next()

    def prevoius(self):
        self.device.Previous()

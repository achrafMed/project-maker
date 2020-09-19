


class keyBindings:
    def __init__(self, window):
        window.bind('<Control-s>', self.saveChanges)
        window.bind('<Control-f>', self.findCharacter)
        window.bind('<Control-r>', self.reloadWindow)

    def reloadWindow(self):
        pass
    def saveChanges(self):
        pass
    def findCharacter(self):
        pass

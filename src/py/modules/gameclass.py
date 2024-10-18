class GameClass:
    def __init__(self, config: dict, name: str):
        self._config = config[name]

    @property
    def config(self):
        return self._config
    
    @config.setter
    def setconfig(self, name: str):
        self._config = self._config[name]
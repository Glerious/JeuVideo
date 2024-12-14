from json import loads

class GlobalConfig:
    """
    Cette Classe permet d'obtenir la config générale.
    """
    def __init__(self):
        self.__path: str = "../../resources/config.json"
        self.__config: dict = self.__save_default_config()
        self.background: dict = self.__config["background"]
        self.constant: dict = self.__config["constant"]
        self.window: dict = self.__config["window"]
        self.entity: dict = self.__config["entity"]
        self.action: dict = self.__config["action"]
    def get(self):
        return self.__config

    def __save_default_config(self):
        json_file = open(self.__path, 'r')
        data = json_file.read()
        return loads(data)
    
class Configurable:
    """ 
    Cet héritage est utilisé pour les classes configurable dans un modèle d'arborescence.
    """
    def __init__(self, config_: dict, name_: str):
        self.__name = name_
        self.config = config_[self.__name]
    
global_config: GlobalConfig = GlobalConfig()
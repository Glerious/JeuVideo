from json import loads
from functools import reduce

class GlobalConfig:
    """
    Cette Classe permet d'obtenir la config générale.
    """
    def __init__(self):
        self.__path: str = "../../resources/config.json"
        self.__config: dict = self.__save_default_config()
        self.background: dict = self.deep_get("background")
        self.constant: dict = self.deep_get("constant")
        self.window: dict = self.deep_get("window")
        self.entity: dict = self.deep_get("entity")
        self.action: dict = self.deep_get("action")
        self.level_design: dict = self.deep_get("level_design")
        self.test: dict = self.deep_get("test")

    def get(self):
        return self.__config

    def __save_default_config(self):
        json_file = open(self.__path, 'r')
        data = json_file.read()
        return loads(data)
    
    def deep_get(self, keys_: str, default_=None, target_type_=None):
        _value = reduce(
            lambda d, key: d.get(key, default_) if isinstance(d, dict) else default_,
            keys_.split("."),
            self.__config
        )
        return _value if not target_type_ else target_type_(_value)
    
    def deep_set(self, path_: str, value):
        _saved_timetable: dict = self.__config
        _keys = path_.split('_')
        _latest = _keys.pop()
        for k in _keys:
            _saved_timetable = _saved_timetable.setdefault(k, {})
        _saved_timetable[_latest] = value   
    
class Configurable:
    """ 
    Cet héritage est utilisé pour les classes configurable dans un modèle d'arborescence.
    """
    def __init__(self, config_: dict, name_: str):
        self.name = name_
        self.config = config_[self.name]
    
global_config: GlobalConfig = GlobalConfig()
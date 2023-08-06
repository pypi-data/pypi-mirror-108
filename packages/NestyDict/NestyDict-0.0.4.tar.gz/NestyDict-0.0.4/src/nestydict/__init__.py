from collections import UserDict
import json

class Nesty(UserDict):
    def __init__(self, data: dict = None):
        self.data = self._dict_loader(data) if data else {}

    @classmethod
    def from_dict(cls, dictionary: dict):
        d = Nesty._dict_loader(dictionary)
        return cls(data=d)

    @staticmethod
    def _dict_loader(dictionary: dict):
        d = {}
        for key, value in dictionary.items():
            if isinstance(value, dict):
                nested = Nesty._dict_loader(value)
                d = Nesty._setter(d, key.split("."), nested)
            else:
                d = Nesty._setter(d, key.split("."), value)
        return d

    def __setitem__(self, key, item) -> None:
        parts = key.split(".")
        new = self._setter(self.data, parts, item)
        self.data = new

    @staticmethod
    def _setter(dictionary: dict, path: list, value) -> dict:
        copy = dictionary.copy()
        key = next(iter(path))

        if len(path) > 1:
            if key in copy and isinstance(copy[key], dict):
                copy[key] = Nesty._setter(copy[key], path[1:], value)
            else:
                copy[key] = Nesty._setter({}, path[1:], value)
        else:
            copy[key] = value
        return copy

    @staticmethod
    def _getter(dictionary: dict, path: list):
        for index, key in enumerate(path):
            if key in dictionary:
                if index == len(path) - 1:
                    return dictionary[key]
                else:
                    return Nesty._getter(dictionary[key], path[index + 1 :])
            raise KeyError(f"Failed to find key: {key} in dict: {dictionary}")

    def __getitem__(self, key):
        parts = key.split(".")
        return self._getter(self.data, parts)

    def __str__(self):
        return json.dumps(self.data, indent=4, ensure_ascii=False)

__all__ = [Nesty]

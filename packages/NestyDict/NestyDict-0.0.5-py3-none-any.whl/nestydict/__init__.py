from __future__ import annotations
from collections import UserDict
from typing import Any
import json

class Nesty(UserDict):
    def __init__(self, data: dict = None, seperator: str = '.'):
        self.data = self._dict_loader(data) if data else {}
        self.seperator = seperator

    @classmethod
    def from_dict(cls, dictionary: dict, seperator: str = '.') -> Nesty:
        """Return an instance of the Nesty class with the data set
        according to the passed `dictionary`. Key's in the passed
        dictionary containing the `seperator` will result in the key
        being split and creating a new sub-dictionary. Please see the
        README for examples.

        Args:
            dictionary (dict): The dictionary to populate the Nesty
            dictionary with.
            seperator (str, optional): The default seperator to use
            for paths in the dictionary. Defaults to '.'.

        Returns:
            Nesty: [description]
        """
        d = Nesty._dict_loader(dictionary, seperator)
        return cls(data=d)

    @staticmethod
    def _dict_loader(dictionary: dict, seperator: str):
        d = {}
        for key, value in dictionary.items():
            if isinstance(value, dict):
                nested = Nesty._dict_loader(value)
                d = Nesty._setter(d, key.split(seperator), nested)
            else:
                d = Nesty._setter(d, key.split(seperator), value)
        return d

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
    def _getter(dictionary: dict, path: list) -> Any:
        for index, key in enumerate(path):
            if key in dictionary:
                if index == len(path) - 1:
                    return dictionary[key]
                else:
                    return Nesty._getter(dictionary[key], path[index + 1 :])
            raise KeyError(f"Failed to find key: {key} in dict: {dictionary}")

    def get(self, key: str, default: Any = None) -> Any:
        """Return an item from the dictionary corresponding to the `key`
        if this is not found return the value provided in the `default`
        argument.

        Args:
            key (str): The key for the item
            default (Any, optional): The default to return if the item is
            not found. Defaults to None.

        Returns:
            Any: An item or default value from the dictionary.
        """

        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __getitem__(self, key: str) -> Any:
        """Return an item from the dictionary corresponding to the
        argument `key`. Raises KeyError if not found"""

        parts = key.split(self.seperator)
        return self._getter(self.data, parts)

    def __setitem__(self, key: str, item: Any) -> None:
        """Set the value of `key` in the dictionary to the value
        provided in the `item` argument.

        Args:
            key (str): The key to set.
            item (Any): The value to set to the key.
        """

        parts = key.split(self.seperator)
        new = self._setter(self.data, parts, item)
        self.data = new

    def __str__(self):
        """Return a string representation of the dictionary"""
        return json.dumps(self.data, indent=4, ensure_ascii=False)

__all__ = [Nesty]

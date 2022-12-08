from contextlib import contextmanager
from copy import deepcopy
from typing import NewType


class UnsupportedOperationException(Exception):
    def __init__(self, *args: object) -> None:
        self.message = "Not allowed on protected object"
        super().__init__(self.message, *args)


def _is_public_name(name: str) -> bool:
    return not name.startswith("_")


class FrozenList(list):
    """
    Based on
    :https://github.com/rohanpm/frozenlist2/blob/master/frozenlist2/__init__.py
    """

    def __setitem__(self, *_args, **_kwargs):
        self.__attempted_modify()

    def __delitem__(self, *_args, **_kwargs):
        self.__attempted_modify()

    def __iadd__(self, *_args, **_kwargs):
        self.__attempted_modify()

    def insert(self, *_args, **_kwargs):
        self.__attempted_modify()

    def append(self, *_args, **_kwargs):
        self.__attempted_modify()

    def extend(self, *_args, **_kwargs):
        self.__attempted_modify()

    def pop(self, *_args, **_kwargs):
        self.__attempted_modify()

    def remove(self, *_args, **_kwargs):
        self.__attempted_modify()

    def sort(self, *_args, **_kwargs):
        self.__attempted_modify()

    # hashable if and only if everything within it is hashable
    def __hash__(self):
        return hash(tuple(self))

    def __attempted_modify(self):
        raise UnsupportedOperationException


ImmutableList = NewType("ImmutableList", FrozenList)


@contextmanager
def unmodifiable_list(self, name: str):
    public_name = name.strip("_")
    origin_name = f"_{self.__class__.__name__}{name}"
    found_name = None
    for name_, type_ in self.__annotations__.items():
        if name_ == public_name and _is_public_name(name_) and type_ is ImmutableList:
            found_name = name_
            break
    if not found_name:
        raise AttributeError(
            "Could not find corresponding public field in origin class or it is not type of ImmutableList"
        )
    origin_list = getattr(self, origin_name)
    # The original list was deep copied and then made to be immutable
    setattr(self, found_name, FrozenList(deepcopy(origin_list)))
    yield getattr(self, found_name)

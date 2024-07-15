from abc import ABC
from dataclasses import dataclass, field
from functools import cached_property
from typing import Union, Optional

import structlog
from structlog import BoundLogger

from .errors import InvalidModel
from .schemas import (
    VendorName,
    Models,
    Model,
)


def get_logger(name: str) -> BoundLogger:
    return structlog.get_logger(name)


logger = get_logger(__name__)


def get_vendor_models(vendor: VendorName) -> list[str] | None:
    if vendor not in Models:
        logger.warning("vendor does not provide a list of models")
        return None

    return Models[vendor]


def pick_best_model(
    model: Optional[str] = None,
    models: Optional[Union[str, list[str]]] = None,
):
    if model is not None:
        return Model.from_string(model)

    if models is not None and len(models) > 0:
        return Model.from_string(models[0])

    raise InvalidModel(
        "Cannot pick the best model, as neither `model` nor `models` contains "
        "a valid model identifier."
    )


@dataclass
class UniversalValue(ABC):
    """
    A UniversalValue can act as a direct string, a lazily evaluated
    string, or a callable string based on the provided methods or attributes.
    """

    original: str
    _value: Optional[str] = field(init=False, default=None)

    def __post_init__(self):
        if hasattr(self, "creator") and callable(self.creator):
            self._value = None
        else:
            self._value = self.original

    @cached_property
    def value(self):
        if hasattr(self, "creator") and callable(self.creator):
            if self._value is None:
                self._value = self.creator(self.original)

        return self._value

    def __call__(self, *args, **kwargs) -> str:
        if hasattr(self, "creator") and callable(self.creator):
            return self.creator(self.original, *args, **kwargs)
        return self.value

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"({self.value if not callable(self) else self()})"
        )

    def __str__(self):
        return self.value if not callable(self) else self()

    def __getattr__(self, item: str):
        if hasattr(str, item):
            return getattr(self.value if not callable(self) else self(), item)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'"
        )

    def __getitem__(self, key):
        return (self.value if not callable(self) else self())[key]

    def __eq__(self, other):
        if isinstance(other, UniversalValue):
            return (self.value if not callable(self) else self()) == other.value
        if isinstance(other, str):
            return (self.value if not callable(self) else self()) == other
        return NotImplemented

    def __len__(self):
        return len(self.value if not callable(self) else self())

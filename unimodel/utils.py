from abc import ABC
from dataclasses import dataclass, field
from functools import cached_property
from types import SimpleNamespace
from typing import Union, Optional

import structlog
from structlog import BoundLogger

from unimodel.schemas import (
    Vendor,
    OPENAI_MODELS,
    AZURE_MODELS,
    ANTHROPHIC_MODELS,
    VENDOR_NAMES,
    Tokenizer,
)


def get_logger(name: str) -> BoundLogger:
    logger = structlog.get_logger(name)
    return logger


@dataclass
class Model:
    vendor: Vendor
    name: Union[OPENAI_MODELS, AZURE_MODELS, ANTHROPHIC_MODELS]

    @classmethod
    def from_string(cls, model_string: str) -> "Model":
        try:
            vendor_name, model_name = model_string.split("/")
        except ValueError:
            raise ValueError("Invalid format. Use 'vendor/model'.")

        if vendor_name not in VENDOR_NAMES:
            raise ValueError(
                f"Invalid vendor name '{vendor_name}'. Valid options are: "
                f"'openai', 'azure', 'anthropic'."
            )

        vendor = Vendor(name=vendor_name)

        return cls(vendor=vendor, name=model_name)

    def get_tokenizer(self) -> Tokenizer | None:
        """
        Returns an instance of the tokenizer that was used to train this model.
        This can be helpful for counting tokens (e.g., for cost estimation).
        """
        match self.vendor.name:
            case "openai":
                from tiktoken import encoding_for_model, get_encoding

                try:
                    return encoding_for_model(self.name)
                except KeyError:
                    return get_encoding("cl100k_base")
            case _:
                return None

    def __post_init__(self):
        if self.vendor.name == "openai" and self.name not in OPENAI_MODELS:
            raise ValueError(
                f"Invalid model name '{self.name}' for vendor 'openai'"
            )
        elif self.vendor.name == "azure" and self.name not in AZURE_MODELS:
            raise ValueError(
                f"Invalid model name '{self.name}' for vendor 'azure'"
            )
        elif (
            self.vendor.name == "anthropic"
            and self.name not in ANTHROPHIC_MODELS
        ):
            raise ValueError(
                f"Invalid model name '{self.name}' for vendor 'anthropic'"
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


class Variables(SimpleNamespace):
    """
    A container for prompt variables that allow for dict-like or object-like
    access patterns.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"Variables({vars(self)})"

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __contains__(self, key):
        return hasattr(self, key)

    def __iter__(self):
        return iter(vars(self))

    def items(self):
        return vars(self).items()

    def keys(self):
        return vars(self).keys()

    def values(self):
        return vars(self).values()

    def to_dict(self):
        return vars(self)

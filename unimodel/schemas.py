from dataclasses import dataclass
from enum import StrEnum
from types import SimpleNamespace
from typing import TypedDict

from unimodel.protocols import Tokenizer


class VendorName(StrEnum):
    ANTHROPHIC = "anthrophic"
    AZURE = "openai"
    DUMMY = "dummy"
    OPENAI = "openai"
    REPLICATE = "replicate"

    @classmethod
    def from_value(cls, value: str) -> "VendorName":
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")

    @classmethod
    def values(cls):
        return [vendor_name.value for vendor_name in cls]


@dataclass
class Vendor:
    name: VendorName

    @classmethod
    def from_value(cls, value: str):
        return Vendor(VendorName.from_value(value))


# TODO: Some API vendors (Azure, Replicate) allow users to deploy various models, and
#   even allow them to choose model names. We need to support registering those
#   models somehow.
Models = {
    VendorName.ANTHROPHIC: ["claude-3-5-sonnet"],
    VendorName.DUMMY: ["base"],
    VendorName.OPENAI: [
        "gpt-4o",
        "gpt-4o-2024-05-13",
        "gpt-4-turbo",
        "gpt-4-turbo-2024-04-09",
        "gpt-4-0125-preview",
        "gpt-4-turbo-preview",
        "gpt-4-1106-preview",
        "gpt-4-vision-preview",
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-0613",
        "gpt-4-32k",
        "gpt-4-32k-0314",
        "gpt-4-32k-0613",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-1106",
        "gpt-3.5-turbo-0125",
        "gpt-3.5-turbo-16k-0613",
    ],
}


class Message(TypedDict):
    role: str
    content: str


class Choice:
    finish_reason: str
    index: int
    message: Message


class Usage:
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class Result:
    id: str
    choices: list[Choice]
    created: str
    model: str
    usage: Usage


@dataclass
class Model:
    vendor: Vendor
    name: str

    @classmethod
    def from_string(cls, vendor_and_model_string: str) -> "Model":
        try:
            vendor_name, model_name = vendor_and_model_string.split("/")
        except ValueError:
            raise ValueError("Invalid format. Use 'vendor/model'.")

        if vendor_name not in VendorName.values():
            raise ValueError(
                f"Invalid vendor name '{vendor_name}'. Valid options are: "
                f"'openai', 'azure', 'anthropic'."
            )

        vendor_name = VendorName.from_value(vendor_name)
        return cls.from_values(vendor_name, model_name)

    @classmethod
    def from_values(cls, vendor_name: VendorName, model: str) -> "Model":
        vendor = Vendor(name=vendor_name)
        return cls(vendor=vendor, name=model)

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
        # TODO: validate that the model exists!
        pass


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

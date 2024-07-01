from dataclasses import dataclass
from typing import Literal, Protocol, TypedDict

VENDOR_NAMES = Literal["openai", "azure", "anthrophic"]


@dataclass
class Vendor:
    name: VENDOR_NAMES


OPENAI_MODELS = Literal["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
AZURE_MODELS = Literal["gpt-3.5-turbo"]
ANTHROPHIC_MODELS = Literal["claude-3.5-sonnet"]


class Tokenizer(Protocol):
    def encode(self, text: str) -> list[int]: ...


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

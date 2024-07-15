from typing import Optional, Literal, TypedDict, Required, Union, Iterable

from pydantic import BaseModel


class TopLogprob(BaseModel):
    token: str
    bytes: Optional[list[int]] = None
    logprob: float


class ChatCompletionTokenLogprob(BaseModel):
    token: str
    bytes: Optional[list[int]] = None
    logprob: float
    top_logprobs: list[TopLogprob]


class ChoiceLogprobs(BaseModel):
    content: Optional[list[ChatCompletionTokenLogprob]] = None


class FunctionCall(BaseModel):
    arguments: str
    name: str


class Function(BaseModel):
    arguments: str
    name: str


class ImageURL(TypedDict, total=False):
    url: Required[str]
    detail: Literal["auto", "low", "high"]


class ChatCompletionContentPartTextParam(TypedDict, total=False):
    text: Required[str]
    type: Required[Literal["text"]]


class ChatCompletionContentPartImageParam(TypedDict, total=False):
    image_url: Required[ImageURL]
    type: Required[Literal["image_url"]]


ChatCompletionContentPartParam = Union[
    ChatCompletionContentPartTextParam, ChatCompletionContentPartImageParam
]


class ChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[str]
    role: Required[Literal["system"]]
    name: str


class ChatCompletionUserMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[ChatCompletionContentPartParam]]]
    role: Required[Literal["user"]]
    name: str


class ChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[str]
    role: Required[Literal["tool"]]
    tool_call_id: Required[str]


class ChatCompletionMessageToolCallParam(TypedDict, total=False):
    id: Required[str]
    function: Required[Function]
    type: Required[Literal["function"]]


class ChatCompletionAssistantMessageParam(TypedDict, total=False):
    role: Required[Literal["assistant"]]
    content: Optional[str]
    function_call: Optional[FunctionCall]
    name: str
    tool_calls: Iterable[ChatCompletionMessageToolCallParam]


class ChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]
    name: Required[str]
    role: Required[Literal["function"]]


ChatCompletionMessageParam = Union[
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionFunctionMessageParam,
]


class ChatCompletionMessageToolCall(BaseModel):
    id: str
    function: Function
    type: Literal["function"]


class ChatCompletionMessage(BaseModel):
    content: Optional[str] = None
    role: Literal["assistant"]
    function_call: Optional[FunctionCall] = None
    tool_calls: Optional[list[ChatCompletionMessageToolCall]] = None


class Choice(BaseModel):
    finish_reason: Literal[
        "stop", "length", "tool_calls", "content_filter", "function_call"
    ]
    index: int
    logprobs: Optional[ChoiceLogprobs] = None
    message: ChatCompletionMessage


class CompletionUsage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class ChatCompletion(BaseModel):
    id: str
    choices: list[Choice]
    created: int
    model: str
    object: Literal["chat.completion"]
    service_tier: Optional[Literal["scale", "default"]] = None
    system_fingerprint: Optional[str] = None
    usage: Optional[CompletionUsage] = None

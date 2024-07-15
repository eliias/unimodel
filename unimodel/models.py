from typing import Optional, Literal

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

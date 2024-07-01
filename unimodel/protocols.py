from typing import Protocol, Iterable, Optional, Union


class Completions(Protocol):
    class Completion(Protocol):
        pass

    def create(self) -> Completion: ...


class Chat(Protocol):
    class Completions(Protocol):
        class ChatCompletion(Protocol):
            pass

        def create(
            self,
            messages: Iterable[any],
            model: Optional[str] = None,
            models: Optional[Union[str, list[str]]] = None,
            frequency_penalty: Optional[float] = None,
            logit_bias: Optional[dict[str, int]] = None,
            logprobs: Optional[bool] = None,
            max_tokens: Optional[int] = None,
            n: Optional[int] = None,
            presence_penalty: Optional[float] = None,
            temperature: Optional[float] = None,
            top_logprobs: Optional[int] = None,
            top_p: Optional[float] = None,
            timeout: Optional[float] = None,
        ) -> ChatCompletion: ...

    @property
    def completions(self) -> Completions: ...


class ClientAdapter(Protocol):
    """
    Client implements the adapter pattern to forward requests sent to a uniform
    interface to the specific clients from vendors (e.g. OpenAI, Anthropic, …).

    Specific clients implement this protocol (and all sub-protocols) via
    composition, so lookup adapters for the specific client implementation.
    """

    @property
    def chat(self) -> Chat: ...

    @property
    def completions(self) -> Completions: ...

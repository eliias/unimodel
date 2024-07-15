from functools import cached_property
from typing import Iterable, Optional, Union, cast

from ..models import ChatCompletion, ChatCompletionMessageParam
from ..protocols import ClientAdapter, Chat
from ..schemas import VendorName

from .utils import get_memoized_vendor_client


class OpenAIAdapter(ClientAdapter):
    class OpenAIChat(Chat):
        class OpenAICompletions(Chat.Completions):
            class OpenAICompletion(ChatCompletion):
                pass

            def create(
                self,
                messages: Iterable[ChatCompletionMessageParam],
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
            ) -> OpenAICompletion:
                client = get_memoized_vendor_client(VendorName.OPENAI)
                return cast(
                    OpenAIAdapter.OpenAIChat.OpenAICompletions.OpenAICompletion,
                    client.chat.completions.create(
                        messages=messages, model=model
                    ),
                )

        @cached_property
        def completions(self) -> OpenAICompletions:
            return OpenAIAdapter.OpenAIChat.OpenAICompletions()

    @cached_property
    def chat(self) -> Chat:
        return OpenAIAdapter.OpenAIChat()

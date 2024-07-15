from functools import cached_property
from typing import Iterable, Optional, Union, cast

from anthropic import Anthropic

from ..models import ChatCompletion
from ..protocols import ClientAdapter, Chat
from ..schemas import VendorName

from .utils import get_memoized_vendor_client


class AnthropicAdapter(ClientAdapter):
    class AnthropicChat(Chat):
        class AnthropicCompletions(Chat.Completions):
            class AnthropicCompletion(ChatCompletion):
                pass

            client: Anthropic

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
            ) -> AnthropicCompletion:
                client = get_memoized_vendor_client(VendorName.ANTHROPHIC)
                return cast(
                    AnthropicAdapter.AnthropicChat.AnthropicCompletions.AnthropicCompletion,
                    client.chat.completions.create(
                        messages=messages, model=model
                    ),
                )

        @cached_property
        def completions(self) -> AnthropicCompletions:
            return AnthropicAdapter.AnthropicChat.AnthropicCompletions()

    @cached_property
    def chat(self) -> Chat:
        return AnthropicAdapter.AnthropicChat()

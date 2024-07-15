from functools import cached_property
from typing import Iterable, Optional, Union, cast

from ..protocols import ClientAdapter, Chat
from ..schemas import VendorName

from .utils import get_memoized_vendor_client


class ReplicateAdapter(ClientAdapter):
    class ReplicateChat(Chat):
        class ReplicateCompletions(Chat.Completions):
            class ReplicateCompletion(Chat.Completions.ChatCompletion):
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
            ) -> ReplicateCompletion:
                client = get_memoized_vendor_client(VendorName.REPLICATE)
                return cast(
                    ReplicateAdapter.ReplicateChat.ReplicateCompletions.ReplicateCompletion,
                    client.chat.completions.create(
                        messages=messages, model=model
                    ),
                )

        @cached_property
        def completions(self) -> ReplicateCompletions:
            return ReplicateAdapter.ReplicateChat.ReplicateCompletions()

    @cached_property
    def chat(self) -> Chat:
        return ReplicateAdapter.ReplicateChat()

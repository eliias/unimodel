import time
from functools import cached_property
from typing import Iterable, Optional, Union, cast

from ..protocols import (
    ClientAdapter,
    Chat,
)
from ..models import ChatCompletionMessage, Choice, CompletionUsage
from ..schemas import VendorName

from .utils import get_memoized_vendor_client


class DummyAdapter(ClientAdapter):
    class DummyChat(Chat):
        class DummyCompletions(Chat.Completions):
            class DummyCompletion(Chat.Completions.ChatCompletion):
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
            ) -> DummyCompletion:
                # TODO: should we actually implement a fake client?
                _client = get_memoized_vendor_client(VendorName.DUMMY)

                completion_message = ChatCompletionMessage(
                    content=(
                        "Marco Polo was a Venetian merchant, explorer "
                        "and writer who travelled through Asia along "
                        "the Silk Road between 1271 and 1295."
                    ),
                    role="assistant",
                )

                choice = Choice(
                    message=completion_message,
                    index=1,
                    finish_reason="stop",
                )

                completion = (
                    DummyAdapter.DummyChat.DummyCompletions.DummyCompletion(
                        id=f"dummy/{model}",
                        model="model",
                        choices=[choice],
                        created=int(time.time()),
                        object="chat.completion",
                        usage=CompletionUsage(
                            completion_tokens=100,
                            prompt_tokens=20,
                            total_tokens=120,
                        ),
                    )
                )

                return cast(
                    DummyAdapter.DummyChat.DummyCompletions.DummyCompletion,
                    completion,
                )

        @cached_property
        def completions(self) -> DummyCompletions:
            return DummyAdapter.DummyChat.DummyCompletions()

    @cached_property
    def chat(self) -> Chat:
        return DummyAdapter.DummyChat()

from functools import cached_property
from typing import Optional, Iterable

from openai import OpenAI

from .protocols import Chat, ClientAdapter


class LazyInitAdapter(ClientAdapter):
    class LazyInitChat(Chat):
        class LazyInitCompletions(Chat.Completions):
            class LazyInitCompletion(Chat.Completions.ChatCompletion):
                pass

            def create(self) -> LazyInitCompletion:
                pass

        @property
        def completions(self):
            return LazyInitAdapter.LazyInitChat.LazyInitCompletions()

    @property
    def chat(self) -> Chat:
        return LazyInitAdapter.LazyInitChat()


class OpenAIAdapter(ClientAdapter):
    class OpenAIChat(Chat):
        class OpenAICompletions(Chat.Completions):
            class OpenAICompletion(Chat.Completions.ChatCompletion):
                pass

            client: OpenAI

            def create(
                self,
                messages: Iterable[any],
                model: str,
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
                return self.client.chat.completions.create(
                    messages=messages, model=model
                )

        @cached_property
        def completions(self) -> OpenAICompletions:
            return OpenAIAdapter.OpenAIChat.OpenAICompletions()

    @cached_property
    def chat(self) -> Chat:
        return OpenAIAdapter.OpenAIChat()

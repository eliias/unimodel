from typing import Iterable, Optional, Union

from ..protocols import Chat, ClientAdapter
from ..utils import pick_best_model

from .utils import get_adapter


class LazyInitAdapter(ClientAdapter):
    class LazyInitChat(Chat):
        class LazyInitCompletions(Chat.Completions):
            class LazyInitCompletion(Chat.Completions.ChatCompletion):
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
            ) -> LazyInitCompletion:
                chosen_model = pick_best_model(model, models)
                # TODO: We actually want to return the vendor adapter, not the
                #   client. Otherwise we can't encapsulate this properly.
                client = get_adapter(chosen_model.vendor.name)
                return client.chat.completions.create(
                    messages=messages, model=chosen_model.name
                )

        @property
        def completions(self):
            return LazyInitAdapter.LazyInitChat.LazyInitCompletions()

    @property
    def chat(self) -> Chat:
        return LazyInitAdapter.LazyInitChat()

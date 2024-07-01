from .adapters import LazyInitAdapter
from .protocols import ClientAdapter, Chat, Completions


class Client(ClientAdapter):
    def __init__(self):
        self.client = LazyInitAdapter()

    @property
    def chat(self) -> Chat:
        return self.client.chat

    @property
    def completions(self) -> Completions:
        return self.client.completions

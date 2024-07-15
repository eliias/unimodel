from typing import Optional, overload

from unimodel import Client


class Scope:
    """
    Creates a client execution scope. This allows usage of e.g. custom user
    credentials instead of global ones (BYOK scenarios).
    """

    client: Client

    def __init__(self, *args, **kwargs):
        self.client = Client()

    def __enter__(self):
        return self.client

    def __exit__(self, _exc_type, exc_val, _exc_tb):
        if exc_val is not None:
            return False

        return True


@overload
def scoped_for(api_key: str) -> Scope: ...


@overload
def scoped_for(openai_api_key: str) -> Scope: ...


@overload
def scoped_for(anthropic_api_key: str) -> Scope: ...


@overload
def scoped_for(
    api_key: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    anthropic_api_key: Optional[str] = None,
) -> Scope: ...


def scoped_for(*args, **kwargs) -> Scope:
    """
    Creates a block that creates a pre-configured unimodel client. The client
    is automatically teared down when the block exits.
    """

    return Scope(*args, **kwargs)

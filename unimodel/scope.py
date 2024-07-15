from unimodel import Client
from unimodel.schemas import Model


class Scope:
    """
    Creates a client execution scope. This allows usage of e.g. custom user
    credentials instead of global ones (BYOK scenarios).
    """

    def __init__(self, model: str):
        self.model = Model.from_string(model)
        self.client = Client()

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, exc_val, _exc_tb):
        if exc_val is not None:
            return False

        return True


def scope_for(model: str) -> Scope:
    """
    Creates a block that creates a pre-configured unimodel client. The client
    is automatically teared down when the block exits.

    :param model:
    """

    return Scope(model)

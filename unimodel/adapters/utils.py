from functools import lru_cache

from ..errors import InvalidVendor
from ..schemas import VendorName


@lru_cache(maxsize=None)
def get_memoized_vendor_client(vendor: VendorName, *args, **kwargs) -> any:
    match vendor:
        case VendorName.ANTHROPHIC:
            from anthropic import Anthropic

            return Anthropic()
        case VendorName.DUMMY:
            return None
        case VendorName.AZURE, VendorName.OPENAI:
            from openai import OpenAI

            return OpenAI()
        case VendorName.REPLICATE:
            from replicate import Client

            return Client()
        case _:
            raise InvalidVendor(
                f"The vendor has no supported adapter: `{vendor.name}`."
            )


def get_adapter(vendor_name: VendorName, *args, **kwargs):
    match vendor_name:
        case VendorName.ANTHROPHIC:
            from .anthropic import AnthropicAdapter

            return AnthropicAdapter()
        case VendorName.DUMMY:
            from .dummy import DummyAdapter

            return DummyAdapter()
        case VendorName.OPENAI:
            from .openai import OpenAIAdapter

            return OpenAIAdapter()
        case VendorName.REPLICATE:
            from .replicate import ReplicateAdapter

            return ReplicateAdapter()
        case _:
            raise InvalidVendor(
                f"The requested adapter for vendor: `{vendor_name.name}` does not exist."
            )

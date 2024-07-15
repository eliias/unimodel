from unittest import TestCase

from devtools import pprint

from unimodel import scoped_for


class TestScope(TestCase):
    def test_scope(self):
        with scoped_for(api_key="") as client:
            client.chat.completions.create(
                model="dummy/base",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant!",
                    },
                ],
            )
            pprint(client)

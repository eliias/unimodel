from devtools import pprint
from unittest import TestCase

from unimodel import Client


class TestAdapters(TestCase):
    def test_openai_initialization(self):
        client = Client()
        response = client.chat.completions.create(
            model="dummy/base",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant!",
                },
                {
                    "role": "user",
                    "content": "Who was Marco Polo?",
                },
            ],
        )
        print("\n# Response")
        pprint(response)

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
        assert response.choices[0].message.content == (
            "Marco Polo was a Venetian "
            "merchant, explorer and writer who travelled through Asia along the "
            "Silk Road between 1271 and 1295."
        )

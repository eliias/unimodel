from unittest import TestCase

from unimodel import Client


class TestAdapters(TestCase):
    def test_openai_initialization(self):
        client = Client()
        response = client.chat.completions.create(model="openai/gpt-4o")

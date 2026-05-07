import unittest
from unittest.mock import patch

from news_bot.agents.research_agent import NewsItem
from news_bot.agents.translation_agent import TranslationAgent


class FakeResponse:
    def raise_for_status(self) -> None:
        return None

    def json(self) -> list:
        return [[["Привет, ", "Hello, ", None, None], ["мир!", "world!", None, None]]]


class FakeClient:
    def __init__(self, *args, **kwargs) -> None:
        self.requests: list[dict] = []

    def __enter__(self) -> "FakeClient":
        return self

    def __exit__(self, *args) -> None:
        return None

    def get(self, url: str, *, params: dict) -> FakeResponse:
        self.requests.append({"url": url, "params": params})
        return FakeResponse()


class TranslationAgentTests(unittest.TestCase):
    @patch("news_bot.agents.translation_agent.httpx.Client", FakeClient)
    def test_translates_item_text_fields_to_russian(self) -> None:
        item = NewsItem(
            title="Hello, world!",
            summary="Hello, world!",
            url="https://example.com",
            source="rss:test",
            published_hint="Thu, 07 May 2026 18:00:00 GMT",
            sort_ts=123.0,
        )

        translated = TranslationAgent().translate_item(item)

        self.assertEqual(translated.title, "Привет, мир!")
        self.assertEqual(translated.summary, "Привет, мир!")
        self.assertEqual(translated.url, item.url)
        self.assertEqual(translated.source, item.source)
        self.assertEqual(translated.published_hint, item.published_hint)
        self.assertEqual(translated.sort_ts, item.sort_ts)


if __name__ == "__main__":
    unittest.main()

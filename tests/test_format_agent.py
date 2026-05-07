from dataclasses import dataclass
import unittest

from news_bot.agents.format_agent import FormatAgent


@dataclass
class FakeNewsItem:
    title: str
    summary: str
    url: str
    published_hint: str | None = None


class FormatAgentTests(unittest.TestCase):
    def test_unescapes_rss_entities_before_telegram_escaping(self) -> None:
        item = FakeNewsItem(
            title="ChatGPT&#8217;s &#8216;Trusted Contact&#8217;",
            summary="Trusted [&#8230;] & more",
            url="https://example.com/article?a=1&b=2",
            published_hint="2026-05-07T14:00:00-04:00",
        )

        html = FormatAgent().to_telegram_html(
            item,
            reference_time_utc="2026-05-07T18:00:41+00:00",
        )

        self.assertIn("ChatGPT’s ‘Trusted Contact’", html)
        self.assertIn("Trusted […] &amp; more", html)
        self.assertIn("Опубликовано: 2026-05-07T14:00:00-04:00", html)
        self.assertNotIn("&#8217;", html)
        self.assertNotIn("&#8230;", html)
        self.assertNotIn("UTC:", html)
        self.assertIn('href="https://example.com/article?a=1&amp;b=2"', html)


if __name__ == "__main__":
    unittest.main()

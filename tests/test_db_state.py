import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from news_bot.db import build_db, normalize_url


class PostedNewsStateTests(unittest.TestCase):
    def test_imports_and_appends_tracked_state_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            state_path = tmp_path / "state" / "posted_news.tsv"
            seeded_url = "https://example.com/already-posted"
            state_path.parent.mkdir(parents=True)
            state_path.write_text(
                "\t".join(
                    [
                        "url_norm",
                        "title_fp",
                        "title",
                        "source",
                        "posted_at",
                        "raw_url",
                    ]
                )
                + "\n"
                + "\t".join(
                    [
                        normalize_url(seeded_url),
                        "seeded-fingerprint",
                        "Seeded title",
                        "rss:test",
                        "1.000000",
                        seeded_url,
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            with patch("news_bot.db.POSTED_NEWS_STATE_PATH", state_path):
                db = build_db(tmp_path / "posted_news.sqlite3")
                self.assertTrue(db.exists(seeded_url, "Different title"))

                new_url = "https://example.com/new-post"
                db.record(new_url, "New title", source="rss:test")

                state_text = state_path.read_text(encoding="utf-8")
                self.assertIn(normalize_url(new_url), state_text)
                self.assertTrue(db.exists(new_url, "New title"))


if __name__ == "__main__":
    unittest.main()

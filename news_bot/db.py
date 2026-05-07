"""Хранилище уже опубликованных новостей (URL + хэш заголовка)."""

from __future__ import annotations

import hashlib
import sqlite3
import time
from pathlib import Path
from contextlib import contextmanager

from news_bot.config import POSTED_NEWS_STATE_PATH


def _title_fingerprint(title: str) -> str:
    t = (title or "").lower().strip()
    t = " ".join(t.split())[:500]
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    try:
        from urllib.parse import urlparse, urlunparse

        p = urlparse(url)
        path = p.path.rstrip("/") if len(p.path) > 1 else p.path
        netloc = p.netloc.lower()
        return urlunparse(
            (p.scheme.lower() or "https", netloc, path, "", "", "")
        )
    except Exception:
        return url


class PostedNewsDB:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._state_path = POSTED_NEWS_STATE_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        self._state_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self._path, timeout=30)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init(self) -> None:
        with self._conn() as c:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS posted_news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url_norm TEXT NOT NULL UNIQUE,
                    title_fp TEXT NOT NULL,
                    title TEXT,
                    source TEXT,
                    posted_at REAL NOT NULL,
                    raw_url TEXT
                )
                """
            )
            c.execute(
                "CREATE INDEX IF NOT EXISTS idx_posted_title_fp ON posted_news(title_fp)"
            )
        self._import_state_file()

    def exists(self, url: str, title: str) -> bool:
        un = normalize_url(url)
        fp = _title_fingerprint(title)
        if not un:
            return self._exists_by_title_fp(fp)
        with self._conn() as c:
            row = c.execute(
                "SELECT 1 FROM posted_news WHERE url_norm = ? OR title_fp = ? LIMIT 1",
                (un, fp),
            ).fetchone()
            return row is not None

    def _exists_by_title_fp(self, title_fp: str) -> bool:
        with self._conn() as c:
            row = c.execute(
                "SELECT 1 FROM posted_news WHERE title_fp = ? LIMIT 1",
                (title_fp,),
            ).fetchone()
            return row is not None

    def record(
        self,
        url: str,
        title: str,
        *,
        source: str | None = None,
    ) -> None:
        un = normalize_url(url)
        fp = _title_fingerprint(title)
        now = time.time()
        with self._conn() as c:
            c.execute(
                """
                INSERT OR IGNORE INTO posted_news
                (url_norm, title_fp, title, source, posted_at, raw_url)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (un, fp, title, source or "", now, url),
            )
        self._append_state_file(un, fp, title, source or "", now, url)

    def _import_state_file(self) -> None:
        if not self._state_path.exists():
            self._state_path.write_text(
                "url_norm\ttitle_fp\ttitle\tsource\tposted_at\traw_url\n",
                encoding="utf-8",
            )
            return

        rows: list[tuple[str, str, str, str, float, str]] = []
        for line in self._state_path.read_text(encoding="utf-8").splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) != 6:
                continue
            url_norm, title_fp, title, source, posted_at, raw_url = parts
            try:
                posted_at_float = float(posted_at)
            except ValueError:
                posted_at_float = 0.0
            if url_norm or title_fp:
                rows.append((url_norm, title_fp, title, source, posted_at_float, raw_url))

        with self._conn() as c:
            c.executemany(
                """
                INSERT OR IGNORE INTO posted_news
                (url_norm, title_fp, title, source, posted_at, raw_url)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

    def _append_state_file(
        self,
        url_norm: str,
        title_fp: str,
        title: str,
        source: str,
        posted_at: float,
        raw_url: str,
    ) -> None:
        if self._state_contains(url_norm, title_fp):
            return
        line = "\t".join(
            self._tsv(value)
            for value in (url_norm, title_fp, title, source, f"{posted_at:.6f}", raw_url)
        )
        with self._state_path.open("a", encoding="utf-8") as f:
            f.write(f"{line}\n")

    def _state_contains(self, url_norm: str, title_fp: str) -> bool:
        if not self._state_path.exists():
            return False
        for line in self._state_path.read_text(encoding="utf-8").splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) != 6:
                continue
            if parts[0] == url_norm or parts[1] == title_fp:
                return True
        return False

    @staticmethod
    def _tsv(value: str) -> str:
        return str(value or "").replace("\t", " ").replace("\n", " ").replace("\r", " ")


def build_db(path: Path) -> PostedNewsDB:
    db = PostedNewsDB(path)
    db.init()
    return db

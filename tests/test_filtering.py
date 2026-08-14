import unittest
from unittest.mock import patch

from RTN import parse

from comet.services.filtering import (
    _clone_parsed,
    _normalize_aliases,
    exact_alias_match,
    filter_worker,
    settings,
)


class AliasFilteringTests(unittest.TestCase):
    def test_cached_parse_clone_detaches_mutated_languages(self):
        cached = parse("Movie.2024.MULTI.FRENCH.1080p.WEB-DL")
        clone = _clone_parsed(cached)

        clone.languages.append("de")

        self.assertNotIn("de", cached.languages)
        self.assertIn("de", clone.languages)

    def test_empty_alias_does_not_match_every_title(self):
        self.assertFalse(exact_alias_match("unrelated title", [""]))

    def test_short_or_partial_alias_does_not_bypass_title_matching(self):
        self.assertFalse(exact_alias_match("quality release", ["it"]))
        self.assertFalse(exact_alias_match("friends swapped places", ["swap"]))
        self.assertFalse(exact_alias_match("friends swapped places", ["swapped"]))
        self.assertTrue(exact_alias_match("swapped", ["swapped"]))

    def test_alias_normalization_keeps_only_current_unique_entries(self):
        self.assertEqual(
            _normalize_aliases(
                {
                    "": ["Ignored"],
                    "en": "Ignored",
                    "fr": [None, "", "  ", " Titre ", "Titre", 1],
                }
            ),
            {"fr": ["Titre"]},
        )
        self.assertEqual(_normalize_aliases([]), {})

    def test_empty_alias_cannot_bypass_worker_title_matching(self):
        torrents = [
            {
                "title": "Completely.Different.2024.1080p.WEB-DL.x264",
                "infoHash": "1" * 40,
            }
        ]

        actual = filter_worker(
            torrents,
            "The Matrix",
            1999,
            0,
            "movie",
            {"ez": [""]},
            False,
        )

        self.assertEqual(actual, [])

    def test_language_scoped_alias_sets_the_exact_language(self):
        torrent = {
            "title": "Il.Postino.2020.1080p.WEB-DL",
            "infoHash": "1" * 40,
        }

        with patch.object(settings, "SMART_LANGUAGE_DETECTION", True):
            actual = filter_worker(
                [torrent],
                "The Postman",
                2020,
                None,
                "movie",
                {"lang:it": ["Il Postino"]},
                False,
            )

        self.assertEqual(actual[0]["parsed"].languages, ["it"])

    def test_external_event_matches_fixture_tokens_and_date(self):
        torrent = {
            "title": (
                "NBA 2025-2026 RS 12.04.2026 Chicago Bulls @ "
                "Dallas Mavericks 1080p WEB-DL"
            ),
            "infoHash": "2" * 40,
        }

        actual = filter_worker(
            [torrent],
            "Dallas Mavericks vs Chicago Bulls",
            2026,
            None,
            "movie",
            {},
            False,
            ("Dallas Mavericks vs Chicago Bulls",),
            "2026-04-12",
        )

        self.assertEqual(len(actual), 1)

    def test_external_event_rejects_a_different_fixture_date(self):
        torrent = {
            "title": (
                "NBA 2025-2026 RS 18.01.2026 Dallas Mavericks @ "
                "Chicago Bulls 1080p WEB-DL"
            ),
            "infoHash": "3" * 40,
        }

        actual = filter_worker(
            [torrent],
            "Dallas Mavericks vs Chicago Bulls",
            2026,
            None,
            "movie",
            {},
            False,
            ("Dallas Mavericks vs Chicago Bulls",),
            "2026-04-12",
        )

        self.assertEqual(actual, [])


if __name__ == "__main__":
    unittest.main()

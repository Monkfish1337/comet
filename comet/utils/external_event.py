import re

_IGNORED_EVENT_WORDS = frozenset({"and", "event", "full", "the", "versus", "vs"})


def _normalise_event_title(title: str) -> str:
    return " ".join(title.casefold().replace("&", " and ").replace("@", " at ").split())


def external_event_title_matches(raw_title: str, aliases: tuple[str, ...]) -> bool:
    normalised_raw = re.sub(r"[^a-z0-9]+", " ", _normalise_event_title(raw_title))
    normalised_raw = " ".join(normalised_raw.split())
    raw_tokens = set(normalised_raw.split())

    for alias in aliases:
        normalised_alias = re.sub(r"[^a-z0-9]+", " ", _normalise_event_title(alias))
        normalised_alias = " ".join(normalised_alias.split())
        if not normalised_alias:
            continue
        if normalised_alias in normalised_raw:
            return True
        tokens = [
            token
            for token in normalised_alias.split()
            if (len(token) >= 3 or token.isdigit())
            and token not in _IGNORED_EVENT_WORDS
        ]
        if len(tokens) >= 2 and all(token in raw_tokens for token in tokens):
            return True
    return False

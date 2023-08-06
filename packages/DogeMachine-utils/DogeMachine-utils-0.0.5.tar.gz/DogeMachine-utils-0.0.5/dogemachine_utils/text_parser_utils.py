import re


def parse_text_for_url(string: str) -> str:
    return re.search("(?P<url>https?://[^\s'\"]+)", string).group("url")

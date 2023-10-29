import random
import re

from .constants import (
    AVAILABLE_CHARS,
    AVAILABLE_CHARS_REGEX_PATTERN,
    MAX_SHORT_LINK_LENGTH_AUTOGEN,
    MAX_SHORT_LINK_LENGTH,
)

from .models import URLMap


def get_unique_short_id():
    while True:
        short_id = "".join(
            random.choices(AVAILABLE_CHARS, k=MAX_SHORT_LINK_LENGTH_AUTOGEN)
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


def validate_short_link(link):
    if len(link) > MAX_SHORT_LINK_LENGTH or not re.match(
        AVAILABLE_CHARS_REGEX_PATTERN, link
    ):
        return False
    return True

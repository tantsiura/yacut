from random import choices
from string import ascii_letters, digits

from .models import URLMap


def get_unique_short_id(list=ascii_letters + digits, k=6):
    while True:
        short_id = ''.join(choices(list, k=k))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
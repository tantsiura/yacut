from random import choices
from string import ascii_letters, digits

from .models import URL_map


def get_unique_short_id(list=ascii_letters + digits, k=6):
    while True:
        short_id = ''.join(choices(list, k=k))
        if not URL_map.query.filter_by(short=short_id).first():
            return short_id
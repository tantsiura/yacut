from datetime import datetime

from flask import url_for

from yacut import db
from yacut.constants import MAX_CUSTOM_ID_LENGTH


class URLMap(db.Model):
    """Модель проекта."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(MAX_CUSTOM_ID_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Метод-сериализатор."""
        return dict(
            url=self.original,
            short_link=url_for(
                'url_view',
                short=self.short,
                _external=True
            )
        )

    def from_dict(self, data):
        """Метод-десериализатор."""
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])
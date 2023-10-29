from datetime import datetime

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(16), unique=True, nullable=False)
    original = db.Column(db.String(2048), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<URLMap {self.short} {self.original!r}>"

    def from_dict(self, data):
        for field in ["short", "original"]:
            if field in data:
                setattr(self, field, data[field])

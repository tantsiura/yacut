from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import AVAILABLE_CHARS_REGEX_PATTERN, MAX_SHORT_LINK_LENGTH


class CutForm(FlaskForm):
    original_link = URLField("Ссылка", validators=[DataRequired(), Length(max=2048)])
    custom_id = StringField(
        "Короткая ссылка",
        validators=[
            Optional(),
            Length(max=MAX_SHORT_LINK_LENGTH),
            Regexp(AVAILABLE_CHARS_REGEX_PATTERN),
        ],
    )
    submit = SubmitField("Обрезать")

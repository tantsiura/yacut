from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional, Regexp, ValidationError)

from yacut.contants import (REQUIRED_FIELD_MESSAGE, URL_VALIDATION_MESSAGE, MIN_CUSTOM_ID_LENGTH,
                            MAX_CUSTOM_ID_LENGTH, CUSTOM_ID_VALIDATION_MESSAGE, CUSTOM_ID_EXISTS_MESSAGE)
from yacut.models import URLMap


class URLForm(FlaskForm):
    """Класс формы проекта."""

    original_link = URLField(
        'Ваша длинная ссылка',
        validators=[DataRequired(message=REQUIRED_FIELD_MESSAGE), URL(
            require_tld=True, message=URL_VALIDATION_MESSAGE)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(MIN_CUSTOM_ID_LENGTH, MAX_CUSTOM_ID_LENGTH), Optional(), Regexp(
            r'^[A-Za-z0-9]+$',
            message=CUSTOM_ID_VALIDATION_MESSAGE)]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        """Метод проверки уникальности поля."""
        if field.data and URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(CUSTOM_ID_EXISTS_MESSAGE)
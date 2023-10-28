from http import HTTPStatus
from re import match

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsageError
from .models import URL_map
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsageError('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsageError('"url" является обязательным полем!')
    if not match(
            r'^[a-z]+://[^\/\?:]+(:[0-9]+)?(\/.*?)?(\?.*)?$', data['url']):
        raise InvalidAPIUsageError('Указан недопустимый URL')
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()
    if not match(r'^[A-Za-z0-9]{1,16}$', data['custom_id']):
        raise InvalidAPIUsageError(
            'Указано недопустимое имя для короткой ссылки')
    if URL_map.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsageError(f'Имя "{data["custom_id"]}" уже занято.')
    url_map = URL_map()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/')
def get_url(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsageError(
            'Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
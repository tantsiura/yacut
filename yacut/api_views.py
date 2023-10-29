from http import HTTPStatus
from re import match

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_unique_short_id


HTTP_OK = HTTPStatus.OK
HTTP_NOT_FOUND = HTTPStatus.NOT_FOUND
HTTP_CREATED = HTTPStatus.CREATED

URL_REGEX_PATTERN = r'^[a-z]+://[^\/\?:]+(:[0-9]+)?(\/.*?)?(\?.*)?$'
CUSTOM_ID_REGEX_PATTERN = r'^[A-Za-z0-9]{1,16}$'


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTP_NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTP_OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    validate_create_id(data)
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTP_CREATED


def validate_create_id(data):
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not match(URL_REGEX_PATTERN, data['url']):
        raise InvalidAPIUsage('Указан недопустимый URL')
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()
        return HTTP_CREATED
    if not match(CUSTOM_ID_REGEX_PATTERN, data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
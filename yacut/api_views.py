from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .helpers import get_unique_short_id, validate_short_link
from .models import URLMap


@app.route("/api/id/", methods=["POST"])
def cut_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")
    if "url" not in data or not data["url"]:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    url = data["url"]
    if "custom_id" in data and data["custom_id"]:
        if not validate_short_link(data["custom_id"]):
            raise InvalidAPIUsage("Указано недопустимое имя для короткой ссылки")
        short_id = data["custom_id"]
        if URLMap.query.filter_by(short=short_id).first():
            raise InvalidAPIUsage(
                "Предложенный вариант короткой ссылки уже существует."
            )
    else:
        short_id = get_unique_short_id()
    link = URLMap.query.filter_by(original=url).first()
    if not link:
        link = URLMap(short=short_id, original=url)
        db.session.add(link)
    else:
        link.short = short_id
    db.session.commit()
    return (
        jsonify(
            {
                "url": url,
                "short_link": url_for(
                    "redirect_to_original", short_url=short_id, _external=True
                ),
            }
        ),
        HTTPStatus.CREATED,
    )


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_link(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if not link:
        raise InvalidAPIUsage(
            "Указанный id не найден", status_code=HTTPStatus.NOT_FOUND
        )
    return jsonify({"url": link.original}), HTTPStatus.OK

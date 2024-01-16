from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import check_short_link, get_unique_short_id, link_view


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    if ('custom_id' in data
            and data['custom_id'] is not None
            and len(data['custom_id']) > 0):
        check_result, message = check_short_link(data['custom_id'])
        if check_result:
            raise InvalidAPIUsage(message)
        short_id = data['custom_id']
    else:
        short_id = get_unique_short_id()

    url_map = URLMap(
        original=data['url'],
        short=short_id,
    )
    db.session.add(url_map)
    db.session.commit()

    data_result = {
        'url': data['url'],
        'short_link': url_for(link_view.__name__, short=short_id, _external=True),
    }
    return jsonify(data_result), HTTPStatus.CREATED

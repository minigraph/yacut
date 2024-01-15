from flask import jsonify, request, url_for

from . import app, db
from .models import URLMap
from .views import get_unique_short_id, check_short_link, link_view
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    elif 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    elif ('custom_id' in data
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
    return jsonify(data_result), 201

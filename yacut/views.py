from random import choice
import re

from flask import flash, redirect, render_template

from . import app, db
from .forms import LinkForm
from .models import URLMap


CHARS: str = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
LENGTH_SHORT: int = 6
MAX_LEN_SHORT: int = 16
RE_ALLOWED_CHARS: str = r'^[a-zA-Z0-9]+$'


def get_unique_short_id():
    short_unique = ''
    while not (len(short_unique) > 0
               and not URLMap.query.filter_by(short=short_unique).first()):
        for i in range(LENGTH_SHORT):
            short_unique += choice(CHARS)
    return short_unique


def check_short_link(short):
    if URLMap.query.filter_by(short=short).first():
        return True, 'Предложенный вариант короткой ссылки уже существует.'

    if len(short) > MAX_LEN_SHORT:
        return True, 'Указано недопустимое имя для короткой ссылки'

    pattern = re.compile(RE_ALLOWED_CHARS)
    if pattern.search(short) is None:
        return True, 'Указано недопустимое имя для короткой ссылки'

    return False, ''


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        if form.custom_id is not None and form.custom_id.data:
            check_result, message = check_short_link(form.custom_id.data)
            if check_result:
                flash(message)
                return render_template('link_handler.html', form=form)
        else:
            form.custom_id.data = get_unique_short_id()

        url_map = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
        db.session.add(url_map)
        db.session.commit()

    return render_template('link_handler.html', form=form)


@app.route('/<string:short>')
def link_view(short):
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original, code=302)

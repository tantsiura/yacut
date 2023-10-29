import string
import random

from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.constants import SHORT_URL_LENGTH


def get_unique_short_id(length=SHORT_URL_LENGTH):
    seq = string.ascii_letters + string.digits
    existing_urls = URLMap.query.all()
    existing_ids = {url.short for url in existing_urls}
    while True:
        new_short_id = ''.join(random.choices(seq, k=length))
        if new_short_id not in existing_ids:
            return new_short_id


@app.route('/', methods=['GET', 'POST'])
def add_url_view():
    form = URLForm()
    if form.validate_on_submit():
        short = form.custom_id.data or get_unique_short_id()

        if URLMap.query.filter_by(short=short).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return redirect(url_for('add_url_view'))

        url = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        flash(url_for('url_view', short=short, _external=True))
    return render_template('url.html', form=form)


@app.route('/<string:short>')
def url_view(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)
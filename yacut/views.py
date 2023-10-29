from urllib.parse import urlparse

from flask import flash, redirect, render_template

from . import app, db
from .forms import CutForm
from .helpers import get_unique_short_id
from .models import URLMap


@app.route("/", methods=["GET", "POST"])
def index_view():
    form = CutForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()
        elif URLMap.query.filter_by(short=custom_id).first():
            flash("Предложенный вариант короткой ссылки уже существует.")
            return render_template("index.html", form=form)
        if not urlparse(form.original_link.data).scheme:
            form.original_link.data = "http://" + form.original_link.data
        link = URLMap.query.filter_by(original=form.original_link.data).first()
        if link:
            link.short = custom_id
        else:
            link = URLMap(
                short=custom_id,
                original=form.original_link.data,
            )
            db.session.add(link)
        db.session.commit()
        return render_template("index.html", form=form, short_link=link)
    return render_template("index.html", form=form)


@app.route("/<short_url>")
def redirect_to_original(short_url):
    link = URLMap.query.filter_by(short=short_url).first_or_404()
    return redirect(link.original)

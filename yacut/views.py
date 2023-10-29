
    urlmap = URLMap(
        original=form.original_link.data,
        short=form.custom_id.data,
    )
    save(urlmap)

    form.custom_id.data = None
    return render_template(
        'index.html',
        form=form,
        short_link=url_for(
            'mapping_redirect',
            short_id=urlmap.short,
            _external=True,
        ),
    )


@app.route('/<string:short_id>', strict_slashes=False)
def mapping_redirect(short_id: str) -> Response:
    return redirect(
        URLMap.query.filter_by(short=short_id).first_or_404().original,
    )
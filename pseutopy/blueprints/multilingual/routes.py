from flask import render_template, Blueprint, g, redirect, request, current_app, abort, url_for
from flask_babel import _, refresh

multilingual = Blueprint('multilingual', __name__,
                         template_folder='templates', url_prefix='/<lang_code>')


@multilingual.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@multilingual.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@multilingual.route('/')
def index():
    return render_template('multilingual/index.html')


@multilingual.route('/editor')
def editor():
    return render_template('multilingual/editor.html',
                           variables="Variables",
                           data_structures="Data structures",
                           maths="Maths",
                           control_structures="Control structures",
                           functions="Functions")

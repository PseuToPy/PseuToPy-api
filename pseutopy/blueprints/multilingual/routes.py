from flask import render_template, Blueprint, g, redirect, request, current_app, \
    url_for
from flask_babel import _
from werkzeug.exceptions import BadRequest

from pseutopy import app

multilingual = Blueprint('multilingual', __name__,
                         template_folder='templates', url_prefix='/<lang_code>')


@multilingual.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@multilingual.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@multilingual.route('/home')
def index():
    return render_template('multilingual/index.html', title=_('Home'))


@multilingual.route('/editor')
def editor():
    return render_template('multilingual/editor.html')


@multilingual.route('/error404')
def page_not_found():
    return render_template('multilingual/error404.html', title=_('Error404'))


@multilingual.before_request
def before_request():
    """
    This is where the URL of type <lang>/<home> will be managed
    :return:
    """
    if g.lang_code not in current_app.config['LANGUAGES']:
        print("TEST")
        g.lang_code = 'en'
        return render_template('multilingual/error404.html')
    dfl = request.url_rule.defaults
    if 'lang_code' in dfl:
        print("DEBUG TEST")
        if dfl['lang_code'] != request.full_path.split('/')[1]:
            return render_template('multilingual/error404.html')

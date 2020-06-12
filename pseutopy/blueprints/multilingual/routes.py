from flask import render_template, Blueprint, g, redirect, request, current_app, \
    url_for
from flask_babel import _

multilingual = Blueprint('multilingual', __name__,
                         template_folder='templates', url_prefix='/<lang_code>')


@multilingual.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@multilingual.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@multilingual.route('/home', defaults={'lang_code': 'en'})
@multilingual.route('/accueil', defaults={'lang_code': 'fr'})
def index():
    return render_template('multilingual/index.html', title=_('Home'))


@multilingual.route('/editor', defaults={'lang_code': 'en'})
@multilingual.route('/editeur', defaults={'lang_code': 'fr'})
def editor():
    return render_template('multilingual/editor.html',
                           title=_('Editor'),
                           variables="Variables",
                           data_structures="Data structures",
                           maths="Maths",
                           control_structures="Control structures",
                           functions="Functions")


@multilingual.before_request
def before_request():
    if g.lang_code not in current_app.config['LANGUAGES']:
        adapter = current_app.url_map.bind('')
        try:
            endpoint, args = adapter.match('/en' +
                                           request.full_path.rstrip('/ ?'))
            return redirect(url_for(endpoint, **args), 301)
        except:
            return render_template('multilingual/404.html')
    dfl = request.url_rule.defaults
    if 'lang_code' in dfl:
        if dfl['lang_code'] != request.full_path.split('/')[1]:
            return render_template('multilingual/404.html')

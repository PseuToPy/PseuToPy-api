from flask import Flask, request, g, redirect, url_for, render_template
from flask_babel import Babel
from config import Config
# import and register blueprints
from pseutopy.blueprints.multilingual import multilingual

# set up application
app = Flask(__name__)
app.config.from_object(Config)


app.register_blueprint(multilingual)

# set up babel
babel = Babel(app)


@babel.localeselector
def get_locale():
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(
            app.config['LANGUAGES'])
    return g.lang_code


@app.route('/')
def home():
    g.lang_code = 'en'
    return redirect(url_for('multilingual.index'))


@app.errorhandler(404)
def not_found(e):
    print("Message", e)
    return render_template("error404.html")

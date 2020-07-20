from flask import Flask, request, g, redirect, url_for, render_template, jsonify
from flask_cors import CORS, cross_origin
from flask_babel import Babel, _
from werkzeug.exceptions import HTTPException
from werkzeug.debug import DebuggedApplication
from pseutopy.pseutopy import PseuToPy
import astor


from config import Config
# import and register blueprints
from src.blueprints.multilingual import multilingual

# set up application
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(multilingual)
if app.debug:
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)


cors = CORS(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(
            app.config['LANGUAGES'])
    return g.lang_code


@app.route('/')
@app.route('/home')
def home():
    g.lang_code = 'en'
    return redirect(url_for('multilingual.index'))


@app.route('/editor')
def editor():
    g.lang_code = 'en'
    return redirect(url_for('multilingual.editor'))


@app.route('/convert', methods=['POST'])
@cross_origin()
def convert():
    params = request.get_json()
    if params['status'] == 0:
        instructions = params['instructions']
        try:
            pseutopy = PseuToPy()
            python_ast = pseutopy.convert_from_string(instructions)
            python_instructions = astor.to_source(python_ast)
            return jsonify(status=0, response=python_instructions)
        except Exception:
            return jsonify(status=1, response= _("Pseudocode parsing error"))
    else:
        return jsonify(status=1, response=_("Convert error"))


@app.errorhandler(HTTPException)
def http_error_handler(e):
    return render_template('error404.html')

from flask import Flask, request, g, redirect, url_for, render_template, jsonify
from flask_cors import CORS, cross_origin
from flask_babel import Babel, _
from werkzeug.exceptions import HTTPException
from werkzeug.debug import DebuggedApplication
from config import Config

from .services.convert import convert, PseutopyParsingException
from .util.http import HttpStatus

# set up application
app = Flask(__name__)
app.config.from_object(Config)
if app.debug:
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

cors = CORS(app)
babel = Babel(app)

def get_language(language):
    if language in app.config['LANGUAGES']:
        return language
    return "en"

@app.route('/')
def home():
    return redirect(url_for('multilingual.index'))

@app.route('/convert/<string:language>', methods=['POST'])
@cross_origin()
def convert_code(language):
    params = request.get_json()
    if((params is None) or (params['instructions'] is None)):
        return "Missing parameter 'instructions'", HttpStatus.BAD_REQUEST
    instructions = params['instructions']
    chosen_lang = get_language(language)
    try:
        python_instructions = convert(instructions, chosen_lang)
        return jsonify(code=python_instructions, language=chosen_lang), HttpStatus.OK
    except PseutopyParsingException as e:
        return jsonify(code="", language=chosen_lang, error="{}".format(e)), HttpStatus.UNPROCESSABLE_ENTITY

# @app.errorhandler(HTTPException)
# def http_error_handler(e):
#     return render_template('error404.html')

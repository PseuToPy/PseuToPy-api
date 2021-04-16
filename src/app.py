from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import BadRequest, UnprocessableEntity, NotFound, InternalServerError
from werkzeug.debug import DebuggedApplication
from config import Config

from .services.convert import convert
from .services.grammar import get_grammar, MalformedJsonException
from .services.metadata import get_metadata

http_ok = 200

# set up application
app = Flask(__name__)
app.config.from_object(Config)
if app.debug:
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

cors = CORS(app)

def get_language(language):
    if language in app.config['LANGUAGES']:
        return language
    return "en"

@app.route('/')
def metadata():
    (pythonVersion, pseutopyVersion, pseutopyTargetGrammar) = get_metadata()
    return jsonify(pythonVersion=pythonVersion, pseutopyVersion=pseutopyVersion,
                   pseutopyTargetGrammar=pseutopyTargetGrammar), http_ok

@app.route('/convert/<string:language>', methods=['POST'])
@cross_origin()
def convert_code(language):
    params = request.get_json()
    if((params is None) or ('instructions' not in params)):
        return "Missing parameter 'instructions'", BadRequest.code
    instructions = params['instructions']
    chosen_lang = get_language(language)
    try:
        python_instructions, status, message = convert(instructions, chosen_lang)
        return jsonify(code=python_instructions, language=chosen_lang, status=status.value, message=message), http_ok
    except Exception as e:
        return "Internal server error", InternalServerError.code

@app.route('/grammar/<string:language>', methods=['GET'])
@cross_origin()
def fetch_grammar(language):
    chosen_lang = get_language(language)
    try:
        return jsonify(get_grammar(chosen_lang)), http_ok
    except FileNotFoundError as fnfErr:
        return "{}".format(fnfErr), InternalServerError.code
    except MalformedJsonException as mjErr:
        return "{}".format(mjErr), InternalServerError.code
    except:
        return "Internal server error", InternalServerError.code

@app.errorhandler(NotFound)
def http_not_found_handler(e):
    return "{}".format(e)

@app.errorhandler(InternalServerError)
def http_internal_error_handler(e):
    return "{}".format(e)

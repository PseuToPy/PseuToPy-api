from flask import Flask, request, g, redirect, url_for, render_template, jsonify, session
from flask_cors import CORS, cross_origin
from flask_babel import Babel, _
from werkzeug.exceptions import HTTPException
from werkzeug.debug import DebuggedApplication
from pseutopy.pseutopy import PseuToPy
import astor

# For Logging
import secrets
import psycopg2
from config import config
from datetime import datetime
from config import Config

# import and register blueprints
from src.blueprints.multilingual import multilingual

# set up application
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(multilingual)
app.secret_key = "#py-th*on"
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
    if 'id' not in session:
        session['id'] = secrets.token_urlsafe(10)
        print("session_id " + session['id'])
    else:
        print("session_id already set " + session['id'])

    g.lang_code = 'en'
    return redirect(url_for('multilingual.index'))


@app.route('/editor')
def editor():
    if 'id' not in session:
        session['id'] = secrets.token_urlsafe(10)
        print("session_id " + session['id'])
    else:
        print("session_id already set " + session['id'])
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
            return jsonify(status=1, response=_("Pseudocode parsing error"))
    else:
        return jsonify(status=1, response=_("Convert error"))


@app.route('/log/documentation', methods=['POST'])
def log_doc():
    data = request.get_json()
    if (data['status'] == 0) & ('id' in session):
        specification = data['specification']
        expanded = data['expanded']
        timestamp = datetime.utcnow()
        session_id = session['id']
        try:
            params = config()
            conn = psycopg2.connect(**params)
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS documentation_viewed (session_id VARCHAR, specification VARCHAR, expanded BOOLEAN , interacted_at TIMESTAMP);")
                    cursor.execute(
                        "INSERT INTO documentation_viewed (session_id, specification, expanded, interacted_at) VALUES(%s, %s, %s, %s)",
                        (session_id, specification, expanded, timestamp,))
                    return jsonify(status=1, response=_("Data logged at" + str(timestamp)))
        except (Exception, psycopg2.DatabaseError) as error:
            print("ERROR: " + error)
    else:
        return jsonify(status=1, response=_("Error logging documentation_viewed!"))


@app.route('/log/input', methods=['POST'])
def log_input():
    data = request.get_json()
    if (data['status'] == 0) & ('id' in session):
        text = data['text']
        timestamp = datetime.utcnow()
        session_id = session['id']
        try:
            params = config()
            conn = psycopg2.connect(**params)
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS user_input(session_id VARCHAR, text VARCHAR, interacted_at TIMESTAMP);")
                    cursor.execute(
                        "INSERT INTO user_input (session_id, text, interacted_at) VALUES(%s, %s, %s)",
                        (session_id, text, timestamp,))
                    return jsonify(status=1, response=_("Data logged at" + str(timestamp)))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    else:
        return jsonify(status=1, response=_("Error logging user_input!"))


@app.route('/log/convert', methods=['POST'])
def log_convert():
    data = request.get_json()
    if (data['status'] == 0) & ('id' in session):
        pseudocode = data['pseudocode']
        successful = data['successful']
        timestamp = datetime.utcnow()
        session_id = session['id']
        try:
            params = config()
            conn = psycopg2.connect(**params)
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS convert(session_id VARCHAR, pseudocode VARCHAR, successful BOOLEAN, interacted_at TIMESTAMP);")
                    cursor.execute(
                        "INSERT INTO convert(session_id, pseudocode, successful, interacted_at) VALUES(%s,%s, %s, %s)",
                        (session_id, pseudocode, successful, timestamp,))
                    return jsonify(status=1, response=_("Data logged at" + str(timestamp)))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    else:
        return jsonify(status=1, response=_("Error logging convert!"))


@app.errorhandler(HTTPException)
def http_error_handler(e):
    return render_template('error404.html')

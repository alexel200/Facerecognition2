import os

from flask import Flask
import sys

sys.path.append('./src')
from src.routes.ai import bp
from pymongo import MongoClient

def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    app.config['BASE_PATH'] = os.path.abspath(os.path.dirname(__file__))

    client = MongoClient("mongodb+srv://alexel200:yAXXQHGA1xGIXjiJ@facedetection.ckah3mj.mongodb.net/", 27017)
    db = client.faceDetection

    from src.routes import ai
    app.register_blueprint(ai.bp, url_prefix='/ai')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app
import os

from flask import Flask
import sys

sys.path.append('./src')


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True, static_folder="resources")

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    app.config['BASE_PATH'] = os.path.abspath(os.path.dirname(__file__))
    app.config['API_SWAGGER_URL'] = os.path.join(app.config['BASE_PATH'] , "/resources/swagger.json")

    with app.app_context():
        from src.routes import ai, swagger
        app.register_blueprint(ai.bp, url_prefix='/ai')
        app.register_blueprint(swagger.swagger_ui_blueprint, url_prefix='/swagger')

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
        print(app.root_path)
        return 'Hello, World!'

    return app
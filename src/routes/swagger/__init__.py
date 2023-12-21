from flask_swagger_ui import get_swaggerui_blueprint
from flask import current_app as app

SWAGGER_URL="/swagger"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    app.config['API_SWAGGER_URL'],
    config={
        'app_name': 'Access API'
    }
)
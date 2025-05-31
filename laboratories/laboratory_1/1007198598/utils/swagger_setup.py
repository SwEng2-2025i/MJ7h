# Swagger setup for documentation
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

def setup_swagger(app):
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'  # Path to the swagger.json file

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Multichannel Notification System"
        }
    )

  # Debugging line to check registered routes
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Swagger JSON path

swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL, 
    API_URL, 
    config={  # Swagger UI config
        'app_name': "Flask API"
    }
)

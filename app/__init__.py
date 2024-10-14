from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(config_class)
    # Supprimez ou commentez les lignes suivantes si elles existent
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ndao123456789@localhost/flaskApi'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def homepage():
        return render_template('index.html')
    
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    from .utils import swaggerui_bp, SWAGGER_URL
    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app

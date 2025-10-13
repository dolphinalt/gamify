from flask import Flask
from flask_cors import CORS
from datetime import datetime, timezone
import os

def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))

    instance_path = os.path.join(basedir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    app = Flask(__name__, instance_path=instance_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "database.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    from extensions import db
    db.init_app(app)

    with app.app_context():
        from routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')

        db.create_all()

    @app.route('/')
    def index():
        return {
            'message': 'Calendar API is running', 
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
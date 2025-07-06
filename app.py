from flask import Flask, jsonify
from routes.s3_routes import s3_blueprint
from config.settings import Settings

def create_app():
    app = Flask(__name__)
    app.config.from_object(Settings)

    # Register blueprints
    app.register_blueprint(s3_blueprint, url_prefix='/api/s3')

    # Root/Health route
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"message": "Server is running on http://localhost:5000"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

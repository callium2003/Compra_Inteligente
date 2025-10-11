import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from src.routes.normalize import normalize_bp
from src.routes.quote import quote_bp

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'compra-inteligente-secret-key-2025')

# Habilitar CORS para desenvolvimento
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Registrar blueprints
app.register_blueprint(normalize_bp, url_prefix='/api')
app.register_blueprint(quote_bp, url_prefix='/api')

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'compra-inteligente-api'}, 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

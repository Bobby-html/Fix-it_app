import os
from flask import Flask

# Import the Blueprints from your two new folders
from web_module.web_routes import web_bp
from mobile_module.mobile_routes import mobile_bp

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_fixit'

# Configure File Uploads globally
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Register the modules (This connects the folders to the main app)
app.register_blueprint(web_bp)
app.register_blueprint(mobile_bp)

if __name__ == '__main__':
    app.run(debug=True)
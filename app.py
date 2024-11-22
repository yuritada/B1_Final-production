from flask import Flask
from blueprints.auth import auth_bp
from blueprints.main import main_bp
from blueprints.reviews import reviews_bp
from db import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# 初期化
print('初期化')
init_db(test=False)

# Blueprintの登録
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(reviews_bp)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from app.extensions import db, login_manager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'amapola123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager.init_app(app)

# IMPORTAR BLUEPRINT
from app.routes.auth.routes import auth

# REGISTRAR BLUEPRINT
app.register_blueprint(auth)

# RUTA PRINCIPAL
@app.route('/')
def home():
    return "Amapola Gourmet funcionando 🚀"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
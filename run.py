from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from myapp.views.routes import modulo1_blueprint

import sys
sys.dont_write_bytecode=True

# app = Flask(__name__)

from config import app

app.register_blueprint(modulo1_blueprint,url_prefix='/')


if __name__ == '__main__':  
    app.run(debug=True)    
    # db.create_all()
        
    
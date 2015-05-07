from flask import Flask

app = Flask(__name__)
  
app.secret_key = '021454044'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/uni_database'
 
from models import db
db.init_app(app)

import uni_app.routes
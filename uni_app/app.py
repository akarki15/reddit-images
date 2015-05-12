from flask import Flask
 
from models import db


import uni_app.routes

app = Flask(__name__)
  
app.secret_key = '021454044'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/uni_database'

db.init_app(app)

app.run(debug=True)


import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

  
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def to_json(self):
            return jsonify({
                "username": self.username,
                "email": self.email
            })
  
db.create_all()  
  
@app.route('/')
def hello_world():
        user1 = User(username='bob', email='bob@bob.com')
        db.session.add(user1)
        db.session.commit()
        return 'Hello, World!'
        
        
@app.route('/user/<int:person_id>')
def get_user(person_id):
    user1 = User.query.get(person_id)
    return user1.to_json()
    
@app.route('/user')
def get_all_user():
    users = User.query.all()
    return jsonify(results = users)
    
    
    
  
  
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
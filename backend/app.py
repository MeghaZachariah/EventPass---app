import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from routes.registration_routes import reg_bp
# 1. Initialize Flask App first
app = Flask(__name__, 
            template_folder='../frontend', 
            static_folder='../frontend')

# 2. Configuration
app.secret_key = 'eventpass_secret_key_2026'
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "..", "database", "eventpass.db")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Initialize Database
db = SQLAlchemy(app)

# 4. Import and Register Blueprint (MUST be after app and db are defined)
from routes.event_routes import event_bp
app.register_blueprint(event_bp)
app.register_blueprint(reg_bp)
# --- MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) 
    role = db.Column(db.String(20), nullable=False)

# Initialize Database File
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        flash('Email already exists!', 'danger')
        return redirect(url_for('signup_page'))

    new_user = User(username=username, email=email, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    
    flash('Account created! Please login.', 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email, password=password).first()
    
    if user:
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials!', 'danger')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    if session['role'] == 'organizer':
        return render_template('organizer.html', name=session['username'])
    return render_template('dashboard.html', name=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- ERROR HANDLERS ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
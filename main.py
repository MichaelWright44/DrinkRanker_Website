import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from config import Config
from database import db, init_db, Drink
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import logging

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(1000), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_admin_user():
    admin_username = 'admin'
    admin_password = 'adminpassword'  # You should change this to a secure password
    
    if not User.query.filter_by(username=admin_username).first():
        admin_user = User(username=admin_username, password=admin_password)
        db.session.add(admin_user)
        db.session.commit()
        logging.info(f"Admin user '{admin_username}' created successfully.")
    else:
        logging.info(f"Admin user '{admin_username}' already exists.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/drinks')
def get_drinks():
    drinks = Drink.query.all()
    return jsonify([
        {
            'name': drink.name,
            'source': drink.source,
            'taste': drink.taste,
            'cost': drink.cost,
            'fun_factor': drink.fun_factor,
            'overall_score': drink.overall_score
        } for drink in drinks
    ])

@app.route('/admin')
@login_required
def admin():
    logging.debug(f"Accessing admin route. User authenticated: {current_user.is_authenticated}")
    drinks = Drink.query.all()
    return render_template('admin.html', drinks=drinks)

@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_drink():
    if request.method == 'POST':
        new_drink = Drink(
            name=request.form['name'],
            source=request.form['source'],
            taste=float(request.form['taste']),
            cost=float(request.form['cost']),
            fun_factor=float(request.form['fun_factor']),
            overall_score=float(request.form['overall_score'])
        )
        db.session.add(new_drink)
        db.session.commit()
        flash('Drink added successfully!', 'success')
        return redirect(url_for('admin'))
    return render_template('add_drink.html')

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_drink(id):
    drink = Drink.query.get_or_404(id)
    if request.method == 'POST':
        drink.name = request.form['name']
        drink.source = request.form['source']
        drink.taste = float(request.form['taste'])
        drink.cost = float(request.form['cost'])
        drink.fun_factor = float(request.form['fun_factor'])
        drink.overall_score = float(request.form['overall_score'])
        db.session.commit()
        flash('Drink updated successfully!', 'success')
        return redirect(url_for('admin'))
    return render_template('edit_drink.html', drink=drink)

@app.route('/admin/delete/<int:id>')
@login_required
def delete_drink(id):
    drink = Drink.query.get_or_404(id)
    db.session.delete(drink)
    db.session.commit()
    flash('Drink deleted successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        logging.debug(f"Login attempt for username: {username}")
        user = User.query.filter_by(username=username).first()
        logging.debug(f"User query result: {user}")
        if user and user.check_password(password):
            logging.debug(f"Password check result: {user.check_password(password)}")
            login_user(user)
            logging.info(f"User {username} logged in successfully")
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            logging.debug(f"Redirecting to: {next_page or url_for('admin')}")
            return redirect(next_page or url_for('admin'))
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
    app.run(host='0.0.0.0', port=5000, debug=True)

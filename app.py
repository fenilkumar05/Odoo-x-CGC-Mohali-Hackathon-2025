from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quickdesk.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Import models first
from models import db, User, Ticket, Category, Comment, Vote, Attachment

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
mail = Mail(app)

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import and register blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.tickets import tickets_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(main_bp)
app.register_blueprint(tickets_bp, url_prefix='/tickets')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Add custom template filters
@app.template_filter('nl2br')
def nl2br_filter(text):
    """Convert newlines to HTML line breaks"""
    if text:
        return text.replace('\n', '<br>')
    return text

# Make the filter safe for HTML
from markupsafe import Markup
@app.template_filter('nl2br_safe')
def nl2br_safe_filter(text):
    """Convert newlines to HTML line breaks and mark as safe"""
    if text:
        return Markup(text.replace('\n', '<br>'))
    return text

# Create database tables
with app.app_context():
    db.create_all()
    
    # Create default admin user if it doesn't exist
    admin_user = User.query.filter_by(email='admin@quickdesk.com').first()
    if not admin_user:
        from werkzeug.security import generate_password_hash
        admin_user = User(
            username='admin',
            email='admin@quickdesk.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin_user)
        
        # Create default categories
        categories = [
            Category(name='Technical Support', description='Technical issues and problems'),
            Category(name='General Inquiry', description='General questions and information'),
            Category(name='Bug Report', description='Software bugs and issues'),
            Category(name='Feature Request', description='New feature suggestions')
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        print("Default admin user and categories created!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

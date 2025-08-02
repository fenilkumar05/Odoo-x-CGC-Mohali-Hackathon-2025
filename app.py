"""
QuickDesk Enhanced Edition - Professional Help Desk Management System

A comprehensive, enterprise-grade help desk solution designed for modern organizations.
Provides streamlined support operations with advanced features, professional UI/UX,
and powerful automation capabilities.

Features:
- Role-based user management (Admin, Agent, End User)
- Advanced ticket management with self-assignment
- Email notifications and activity tracking
- Professional responsive interface
- Complete admin controls and user management
- Production-ready security and error handling

Author: QuickDesk Development Team
Version: Enhanced Edition
License: MIT
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# =============================================================================
# APPLICATION CONFIGURATION
# =============================================================================

# Core Flask configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quickdesk.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

# File upload configuration
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB default

# Email notification configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

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

# Register template context processors
@app.context_processor
def inject_utility_functions():
    """Inject utility functions into template context"""
    from utils import time_ago, format_full_datetime, get_user_role_display, get_user_display_name
    return {
        'time_ago': time_ago,
        'format_full_datetime': format_full_datetime,
        'get_user_role_display': get_user_role_display,
        'get_user_display_name': get_user_display_name
    }

# Database initialization is handled by run_enhanced.py or setup scripts
# This prevents issues when running with enhanced models

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

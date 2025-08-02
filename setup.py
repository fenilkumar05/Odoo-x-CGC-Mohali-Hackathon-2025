#!/usr/bin/env python3
"""
QuickDesk Setup Script
This script sets up the QuickDesk help desk system.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8 or higher is required")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create a virtual environment"""
    if os.path.exists('venv'):
        print("✓ Virtual environment already exists")
        return True
    
    return run_command('python -m venv venv', 'Creating virtual environment')

def activate_and_install_requirements():
    """Install requirements in virtual environment"""
    if os.name == 'nt':  # Windows
        pip_command = 'venv\\Scripts\\pip install -r requirements.txt'
    else:  # Unix/Linux/macOS
        pip_command = 'venv/bin/pip install -r requirements.txt'
    
    return run_command(pip_command, 'Installing Python packages')

def setup_database():
    """Initialize the database with enhanced features"""
    if os.name == 'nt':  # Windows
        python_command = 'venv\\Scripts\\python'
    else:  # Unix/Linux/macOS
        python_command = 'venv/bin/python'

    # Check if database already exists
    if os.path.exists('instance/quickdesk.db'):
        print("📋 Existing database found. Running migration...")
        return run_command(f'{python_command} migrate_database.py', 'Migrating database to latest version')
    else:
        print("🗄️  Creating new database with enhanced features...")
        # Create a comprehensive database initialization script
        init_script = f"""
import sys
sys.path.append('.')
from app import app, db
from models import User, Category, Tag, NotificationSettings
from werkzeug.security import generate_password_hash
from datetime import datetime

with app.app_context():
    # Create all tables
    db.create_all()
    print("✅ Database tables created")

    # Create default admin user
    admin_user = User.query.filter_by(email='admin@quickdesk.com').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@quickdesk.com',
            first_name='System',
            last_name='Administrator',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            is_active=True,
            email_notifications=True
        )
        db.session.add(admin_user)
        db.session.flush()

        # Create notification settings for admin
        admin_notifications = NotificationSettings(
            user_id=admin_user.id,
            email_on_ticket_created=True,
            email_on_ticket_updated=True,
            email_on_comment_added=True,
            email_on_status_changed=True,
            email_on_assignment=True
        )
        db.session.add(admin_notifications)
        print("✅ Admin user created: admin@quickdesk.com / admin123")

    # Create default categories
    default_categories = [
        {{'name': 'Technical Support', 'description': 'Technical issues and troubleshooting'}},
        {{'name': 'Bug Report', 'description': 'Software bugs and errors'}},
        {{'name': 'Feature Request', 'description': 'Requests for new features or improvements'}},
        {{'name': 'General Inquiry', 'description': 'General questions and information requests'}},
        {{'name': 'Account Issues', 'description': 'Account access and management problems'}},
        {{'name': 'Billing', 'description': 'Billing and payment related questions'}}
    ]

    for cat_data in default_categories:
        existing_cat = Category.query.filter_by(name=cat_data['name']).first()
        if not existing_cat:
            category = Category(**cat_data)
            db.session.add(category)

    # Create default tags
    default_tags = [
        {{'name': 'urgent', 'color': '#ef4444', 'description': 'Urgent issues requiring immediate attention'}},
        {{'name': 'bug', 'color': '#f59e0b', 'description': 'Software bugs and errors'}},
        {{'name': 'feature-request', 'color': '#10b981', 'description': 'Requests for new features'}},
        {{'name': 'question', 'color': '#3b82f6', 'description': 'General questions and inquiries'}},
        {{'name': 'billing', 'color': '#8b5cf6', 'description': 'Billing and payment related issues'}},
        {{'name': 'hardware', 'color': '#6b7280', 'description': 'Hardware related problems'}},
        {{'name': 'software', 'color': '#06b6d4', 'description': 'Software related issues'}},
        {{'name': 'network', 'color': '#84cc16', 'description': 'Network connectivity issues'}},
        {{'name': 'security', 'color': '#dc2626', 'description': 'Security related concerns'}},
        {{'name': 'training', 'color': '#7c3aed', 'description': 'Training and documentation requests'}}
    ]

    for tag_data in default_tags:
        existing_tag = Tag.query.filter_by(name=tag_data['name']).first()
        if not existing_tag:
            tag = Tag(**tag_data)
            db.session.add(tag)

    db.session.commit()
    print("✅ Default categories and tags created")
    print("✅ Database initialized successfully with enhanced features!")
"""

        with open('init_db.py', 'w') as f:
            f.write(init_script)

        success = run_command(f'{python_command} init_db.py', 'Initializing enhanced database')

        # Clean up
        if os.path.exists('init_db.py'):
            os.remove('init_db.py')

        return success

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'instance']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✓ Created necessary directories")
    return True

def setup_environment_file():
    """Setup environment file"""
    if os.path.exists('.env'):
        print("✓ .env file already exists")
        return True
    
    env_content = """SECRET_KEY=your-secret-key-here-change-this-in-production
DATABASE_URL=sqlite:///quickdesk.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✓ Created .env file")
    return True

def main():
    """Main setup function"""
    print("🚀 QuickDesk Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Setup environment file
    if not setup_environment_file():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install requirements
    if not activate_and_install_requirements():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("🎉 QuickDesk Enhanced Setup Completed Successfully!")
    print("=" * 70)
    print("\n📋 NEXT STEPS:")
    print("\n1. 🔧 Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")

    print("\n2. ⚙️  Configure your environment (optional but recommended):")
    print("   • Edit the .env file to configure email settings")
    print("   • See CONFIGURATION_GUIDE.md for detailed setup instructions")

    print("\n3. 🚀 Run the application:")
    print("   python app.py")
    print("   or use: python run.py")

    print("\n4. 🌐 Open your browser and go to:")
    print("   http://localhost:5000")

    print("\n🔑 DEFAULT ADMIN CREDENTIALS:")
    print("   Email: admin@quickdesk.com")
    print("   Password: admin123")
    print("   ⚠️  IMPORTANT: Change the default password after first login!")

    print("\n✨ NEW ENHANCED FEATURES AVAILABLE:")
    print("   🎯 Role-based registration (User, Agent, Admin)")
    print("   🎨 Modern responsive UI with dark mode")
    print("   🏷️  Advanced tagging system")
    print("   📹 Video call integration for support")
    print("   📊 Comprehensive analytics dashboard")
    print("   🔔 Enhanced notification system")
    print("   📱 Progressive Web App (PWA) support")
    print("   🤖 Auto-assignment and escalation")
    print("   💬 Real-time collaboration features")

    print("\n📚 DOCUMENTATION:")
    print("   • README.md - General overview and features")
    print("   • CONFIGURATION_GUIDE.md - Detailed configuration")
    print("   • SETUP_GUIDE.md - Step-by-step setup instructions")

    print("\n🎫 Enjoy using QuickDesk Enhanced Edition!")
    print("   Professional help desk system with enterprise features")
    print("=" * 70)

if __name__ == '__main__':
    main()

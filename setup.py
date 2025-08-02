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
    """Initialize the database"""
    if os.name == 'nt':  # Windows
        python_command = 'venv\\Scripts\\python'
    else:  # Unix/Linux/macOS
        python_command = 'venv/bin/python'
    
    # Create a simple database initialization script
    init_script = f"""
import sys
sys.path.append('.')
from app import app, db
with app.app_context():
    db.create_all()
    print("Database initialized successfully!")
"""
    
    with open('init_db.py', 'w') as f:
        f.write(init_script)
    
    success = run_command(f'{python_command} init_db.py', 'Initializing database')
    
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
    
    print("\n" + "=" * 50)
    print("🎉 QuickDesk setup completed successfully!")
    print("\nNext steps:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    print("2. Run the application:")
    print("   python app.py")
    print("3. Open your browser and go to: http://localhost:5000")
    print("\nDefault admin credentials:")
    print("   Email: admin@quickdesk.com")
    print("   Password: admin123")
    print("\nEnjoy using QuickDesk! 🎫")

if __name__ == '__main__':
    main()

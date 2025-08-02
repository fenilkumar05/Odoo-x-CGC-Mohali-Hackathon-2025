#!/usr/bin/env python3
"""
QuickDesk Enhanced Edition - Simple Runner
This script starts QuickDesk with all enhanced features enabled.
"""

import os
import sys
from app import app, db

def create_database():
    """Create database tables if they don't exist"""
    try:
        with app.app_context():
            # Import all models to ensure they're registered
            from models import (User, Category, Ticket, Comment, Vote, Attachment, 
                              Tag, TicketActivity, NotificationSettings, TicketEscalation)
            
            # Create all tables
            db.create_all()
            print("Database tables created successfully!")
            
            # Create default admin user if it doesn't exist
            admin_user = User.query.filter_by(email='admin@quickdesk.com').first()
            if not admin_user:
                from werkzeug.security import generate_password_hash
                
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
                print("Admin user created: admin@quickdesk.com / admin123")
            
            # Create default categories if they don't exist
            default_categories = [
                {'name': 'Technical Support', 'description': 'Technical issues and troubleshooting'},
                {'name': 'Bug Report', 'description': 'Software bugs and errors'},
                {'name': 'Feature Request', 'description': 'Requests for new features or improvements'},
                {'name': 'General Inquiry', 'description': 'General questions and information requests'},
                {'name': 'Account Issues', 'description': 'Account access and management problems'},
                {'name': 'Billing', 'description': 'Billing and payment related questions'}
            ]
            
            for cat_data in default_categories:
                existing_cat = Category.query.filter_by(name=cat_data['name']).first()
                if not existing_cat:
                    category = Category(**cat_data)
                    db.session.add(category)
            
            # Create default tags if they don't exist
            default_tags = [
                {'name': 'urgent', 'color': '#ef4444', 'description': 'Urgent issues requiring immediate attention'},
                {'name': 'bug', 'color': '#f59e0b', 'description': 'Software bugs and errors'},
                {'name': 'feature-request', 'color': '#10b981', 'description': 'Requests for new features'},
                {'name': 'question', 'color': '#3b82f6', 'description': 'General questions and inquiries'},
                {'name': 'billing', 'color': '#8b5cf6', 'description': 'Billing and payment related issues'},
                {'name': 'hardware', 'color': '#6b7280', 'description': 'Hardware related problems'},
                {'name': 'software', 'color': '#06b6d4', 'description': 'Software related issues'},
                {'name': 'network', 'color': '#84cc16', 'description': 'Network connectivity issues'},
                {'name': 'security', 'color': '#dc2626', 'description': 'Security related concerns'},
                {'name': 'training', 'color': '#7c3aed', 'description': 'Training and documentation requests'}
            ]
            
            for tag_data in default_tags:
                existing_tag = Tag.query.filter_by(name=tag_data['name']).first()
                if not existing_tag:
                    tag = Tag(**tag_data)
                    db.session.add(tag)
            
            db.session.commit()
            print("Default data created successfully!")
            
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
    
    return True

def main():
    """Main function to run QuickDesk Enhanced Edition"""
    print("=" * 60)
    print("QuickDesk Enhanced Edition")
    print("Professional Help Desk System")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("Error: Please run this script from the QuickDesk root directory")
        sys.exit(1)
    
    # Create uploads directory if it doesn't exist
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"Created uploads directory: {uploads_dir}")
    
    # Initialize database
    print("Initializing database...")
    if not create_database():
        print("Failed to initialize database. Please check the error messages above.")
        sys.exit(1)
    
    print("\nStarting QuickDesk Enhanced Edition...")
    print("Features enabled:")
    print("  * Role-based user management")
    print("  * Modern responsive UI with dark mode")
    print("  * Advanced tagging system")
    print("  * Video call integration")
    print("  * Enhanced notifications")
    print("  * Analytics dashboard")
    print("  * Progressive Web App (PWA)")
    print("  * Auto-assignment and escalation")
    
    print("\nDefault admin credentials:")
    print("  Email: admin@quickdesk.com")
    print("  Password: admin123")
    print("  IMPORTANT: Change the default password after first login!")
    
    print(f"\nServer starting at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start the Flask application
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

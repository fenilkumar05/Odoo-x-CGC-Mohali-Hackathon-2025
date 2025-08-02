#!/usr/bin/env python3
"""
QuickDesk Run Script
Simple script to start the QuickDesk application
"""

import os
import sys
from pathlib import Path

def main():
    """Main run function"""
    print("🎫 Starting QuickDesk Help Desk System...")
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Not running in a virtual environment")
        print("   Consider activating the virtual environment first:")
        if os.name == 'nt':  # Windows
            print("   venv\\Scripts\\activate")
        else:  # Unix/Linux/macOS
            print("   source venv/bin/activate")
        print()
    
    # Check if required files exist
    required_files = ['app.py', 'models.py', 'requirements.txt']
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("   Please ensure you're in the correct directory")
        sys.exit(1)
    
    # Create uploads directory if it doesn't exist
    Path('uploads').mkdir(exist_ok=True)
    
    # Import and run the app
    try:
        from app import app
        print("✅ QuickDesk loaded successfully!")
        print("🌐 Starting web server...")
        print("📱 Open your browser and go to: http://localhost:5000")
        print("👤 Default admin login: admin@quickdesk.com / admin123")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 60)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please install requirements: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

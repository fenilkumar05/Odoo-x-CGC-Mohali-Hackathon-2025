# QuickDesk Setup Guide

## Quick Start (Easiest Method)

### For Windows Users:
1. **Double-click `start.bat`** - This will automatically set up and run QuickDesk
2. **Open your browser** and go to: http://localhost:5000
3. **Login with default admin credentials**:
   - Email: `admin@quickdesk.com`
   - Password: `admin123`

### For All Platforms:
1. **Run the setup script**:
   ```bash
   python setup.py
   ```
2. **Start the application**:
   ```bash
   # Windows
   venv\Scripts\python.exe app.py
   
   # macOS/Linux
   source venv/bin/activate
   python app.py
   ```
3. **Open browser**: http://localhost:5000

## Manual Setup (Advanced Users)

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Step-by-Step Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create directories**:
   ```bash
   mkdir uploads
   ```

5. **Configure environment** (optional):
   - Edit `.env` file for email settings
   - Default SQLite database will be created automatically

6. **Run the application**:
   ```bash
   python app.py
   ```

## Configuration

### Email Notifications (Optional)
To enable email notifications, edit the `.env` file:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

**For Gmail users**: Use an App Password instead of your regular password.

### Database
- Default: SQLite database (`quickdesk.db`)
- Location: Project root directory
- Automatically created on first run

## Default Accounts

### Administrator
- **Email**: admin@quickdesk.com
- **Password**: admin123
- **Permissions**: Full system access

### Creating Additional Users
1. Login as admin
2. Go to Admin → Users
3. Click "Create User"
4. Choose role: User, Agent, or Admin

## System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux
- **Python**: 3.10 or higher
- **RAM**: 512 MB
- **Storage**: 100 MB free space
- **Browser**: Chrome, Firefox, Safari, or Edge

### Recommended Requirements
- **RAM**: 1 GB or more
- **Storage**: 1 GB free space (for file uploads)
- **Network**: Internet connection (for email notifications)

## Troubleshooting

### Common Issues

#### 1. "Python not found"
**Solution**: Install Python 3.10+ from python.org

#### 2. "Permission denied" errors
**Solution**: 
- Windows: Run as Administrator
- macOS/Linux: Check file permissions with `chmod +x setup.py`

#### 3. "Port 5000 already in use"
**Solution**: 
- Stop other applications using port 5000
- Or edit `app.py` to use a different port

#### 4. Database errors
**Solution**: 
- Delete `quickdesk.db` file
- Restart the application

#### 5. Email not working
**Solution**:
- Check SMTP settings in `.env`
- For Gmail, enable 2FA and use App Password
- Verify firewall settings

### Getting Help

1. **Check the console output** for error messages
2. **Verify Python version**: `python --version`
3. **Check dependencies**: `pip list`
4. **Review log files** in the application directory

## File Structure

```
quick-desk/
├── app.py              # Main application
├── models.py           # Database models
├── forms.py            # Web forms
├── utils.py            # Utility functions
├── requirements.txt    # Dependencies
├── setup.py           # Setup script
├── start.bat          # Windows startup script
├── .env               # Environment variables
├── routes/            # Application routes
├── templates/         # HTML templates
├── uploads/           # File uploads
└── venv/              # Virtual environment
```

## Security Notes

### Important Security Considerations

1. **Change default admin password** immediately after setup
2. **Update SECRET_KEY** in `.env` for production use
3. **Use HTTPS** in production environments
4. **Regular backups** of the database file
5. **Keep dependencies updated**: `pip install --upgrade -r requirements.txt`

### Production Deployment

For production use:
1. Use a production WSGI server (e.g., Gunicorn)
2. Set up a reverse proxy (e.g., Nginx)
3. Use a production database (e.g., PostgreSQL)
4. Enable SSL/TLS certificates
5. Set up proper logging and monitoring

## Features Overview

### For End Users
- Create and track support tickets
- Add comments and attachments
- Vote on tickets
- Search and filter tickets
- Email notifications

### For Support Agents
- View and manage all tickets
- Assign tickets to team members
- Update ticket status
- Add internal notes
- Respond to customer inquiries

### For Administrators
- User management (create, edit, delete)
- Category management
- System statistics and reporting
- Role-based access control
- System configuration

## Next Steps

After successful setup:

1. **Login as admin** and change the default password
2. **Create categories** for organizing tickets
3. **Add agent accounts** for your support team
4. **Configure email settings** for notifications
5. **Create test tickets** to familiarize yourself with the system
6. **Train your team** on using the system

## Support

For additional help:
- Check the main README.md file
- Review the application logs
- Test with the default admin account
- Verify all dependencies are installed correctly

---

**QuickDesk** - Simple, efficient help desk management for teams of all sizes.

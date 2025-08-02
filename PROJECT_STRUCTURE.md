# QuickDesk Enhanced Edition - Project Structure

This document provides a comprehensive overview of the project structure and file organization for QuickDesk Enhanced Edition.

## 📁 **Root Directory Structure**

```
quickdesk-enhanced/
├── 📄 README.md                    # Complete project documentation
├── 📄 CHANGELOG.md                 # Version history and changes
├── 📄 LICENSE                      # MIT License
├── 📄 CONFIGURATION_GUIDE.md       # Detailed configuration instructions
├── 📄 DEPLOYMENT_GUIDE.md          # Production deployment guide
├── 📄 PROJECT_STRUCTURE.md         # This file - project organization
├── 📄 .env.example                 # Environment configuration template
├── 📄 requirements.txt             # Python dependencies
├── 📄 app.py                       # Main Flask application
├── 📄 models.py                    # Database models and schemas
├── 📄 forms.py                     # WTForms form definitions
├── 📄 utils.py                     # Utility functions and helpers
├── 📄 run_enhanced.py              # Enhanced application runner
├── 📄 setup.py                     # Setup and installation script
├── 📁 routes/                      # Application route blueprints
├── 📁 templates/                   # Jinja2 HTML templates
├── 📁 static/                      # Static assets (CSS, JS, images)
├── 📁 uploads/                     # File upload directory
├── 📁 instance/                    # Instance-specific files (database)
└── 📁 venv/                        # Python virtual environment
```

## 🗂️ **Detailed File Descriptions**

### **Core Application Files**

| File | Purpose | Description |
|------|---------|-------------|
| `app.py` | Main Application | Flask app initialization, configuration, and setup |
| `models.py` | Database Models | SQLAlchemy models for all database tables |
| `forms.py` | Form Definitions | WTForms classes for all application forms |
| `utils.py` | Utility Functions | Helper functions for email, formatting, etc. |
| `run_enhanced.py` | Application Runner | Enhanced startup script with initialization |

### **Configuration Files**

| File | Purpose | Description |
|------|---------|-------------|
| `.env.example` | Config Template | Example environment configuration |
| `requirements.txt` | Dependencies | Python package requirements |
| `setup.py` | Installation | Automated setup and installation script |

### **Documentation Files**

| File | Purpose | Description |
|------|---------|-------------|
| `README.md` | Main Documentation | Complete setup and usage guide |
| `CHANGELOG.md` | Version History | Detailed change log and version notes |
| `CONFIGURATION_GUIDE.md` | Config Guide | Detailed configuration instructions |
| `DEPLOYMENT_GUIDE.md` | Deployment Guide | Production deployment instructions |
| `LICENSE` | Legal | MIT License terms and conditions |

## 📂 **Directory Structure**

### **routes/ - Application Routes**

```
routes/
├── __init__.py                     # Blueprint package initialization
├── auth.py                         # Authentication routes (login, register)
├── main.py                         # Main application routes (dashboard, analytics)
├── tickets.py                      # Ticket management routes
└── admin.py                        # Administrative routes and controls
```

**Route Responsibilities:**
- `auth.py`: User authentication, registration, login/logout
- `main.py`: Dashboard, analytics, profile management
- `tickets.py`: Ticket CRUD, comments, assignments, status updates
- `admin.py`: User management, system administration

### **templates/ - HTML Templates**

```
templates/
├── base.html                       # Base template with common layout
├── index.html                      # Landing page template
├── dashboard.html                  # Main dashboard template
├── agent_dashboard.html            # Agent-specific dashboard
├── analytics.html                  # Analytics and reporting page
├── profile.html                    # User profile management
├── auth/                           # Authentication templates
│   ├── login.html                  # Login form
│   ├── register.html               # Registration form
│   └── logout.html                 # Logout confirmation
├── tickets/                        # Ticket management templates
│   ├── create.html                 # Ticket creation form
│   ├── view.html                   # Ticket detail view
│   ├── edit.html                   # Ticket editing form
│   └── list.html                   # Ticket listing page
└── admin/                          # Administrative templates
    ├── dashboard.html              # Admin dashboard
    ├── users.html                  # User management
    ├── edit_user.html              # User editing form
    └── categories.html             # Category management
```

### **static/ - Static Assets**

```
static/
├── css/                            # Stylesheets
│   ├── style.css                   # Main application styles
│   ├── admin.css                   # Admin-specific styles
│   └── responsive.css              # Mobile responsive styles
├── js/                             # JavaScript files
│   ├── app.js                      # Main application JavaScript
│   ├── dashboard.js                # Dashboard functionality
│   └── tickets.js                  # Ticket management scripts
├── images/                         # Image assets
│   ├── logo.png                    # Application logo
│   ├── favicon.ico                 # Browser favicon
│   └── avatars/                    # User avatar images
└── fonts/                          # Custom fonts (if any)
```

### **uploads/ - File Storage**

```
uploads/
├── tickets/                        # Ticket attachments
│   ├── 2024/                       # Year-based organization
│   │   ├── 01/                     # Month-based organization
│   │   └── 02/
│   └── temp/                       # Temporary uploads
└── avatars/                        # User profile pictures
```

### **instance/ - Instance Data**

```
instance/
├── quickdesk.db                    # SQLite database file
├── config.py                       # Instance-specific configuration
└── logs/                           # Application logs (if configured)
    ├── app.log                     # General application logs
    ├── error.log                   # Error logs
    └── access.log                  # Access logs
```

## 🔧 **Key Components**

### **Database Models (models.py)**

| Model | Purpose | Key Fields |
|-------|---------|------------|
| `User` | User accounts | username, email, role, password_hash |
| `Ticket` | Support tickets | subject, description, status, priority |
| `Comment` | Ticket comments | content, user_id, ticket_id |
| `Category` | Ticket categories | name, description, is_active |
| `Tag` | Ticket tags | name, color |
| `Attachment` | File attachments | filename, file_path, ticket_id |
| `TicketActivity` | Audit trail | activity_type, description, user_id |
| `Vote` | Ticket voting | vote_type, user_id, ticket_id |
| `NotificationSettings` | User preferences | email_on_comment, email_on_status |

### **Form Classes (forms.py)**

| Form | Purpose | Key Fields |
|------|---------|------------|
| `LoginForm` | User authentication | email, password |
| `RegistrationForm` | User registration | username, email, password, role |
| `TicketForm` | Ticket creation/editing | subject, description, category, priority |
| `CommentForm` | Adding comments | content |
| `UserForm` | User management | username, email, role, is_active |
| `CategoryForm` | Category management | name, description |

### **Utility Functions (utils.py)**

| Function | Purpose | Description |
|----------|---------|-------------|
| `send_notification_email()` | Email notifications | Send automated email notifications |
| `time_ago()` | Time formatting | Human-readable time differences |
| `format_full_datetime()` | Date formatting | Consistent date/time formatting |
| `get_user_display_name()` | User display | Formatted user names |
| `get_user_role_display()` | Role display | Human-readable role names |

## 🚀 **Deployment Structure**

### **Development Environment**
- Uses SQLite database in `instance/` directory
- Debug mode enabled
- Development server on localhost:5000
- File uploads stored locally in `uploads/`

### **Production Environment**
- PostgreSQL or MySQL database (configured via DATABASE_URL)
- Debug mode disabled
- WSGI server (Gunicorn) with reverse proxy (Nginx)
- File uploads with proper permissions and security
- Environment variables for all sensitive configuration

## 📋 **File Permissions**

### **Required Permissions**

| Directory/File | Permission | Purpose |
|----------------|------------|---------|
| `uploads/` | 755 (rwxr-xr-x) | File upload storage |
| `instance/` | 755 (rwxr-xr-x) | Database and logs |
| `static/` | 755 (rwxr-xr-x) | Static asset serving |
| `templates/` | 644 (rw-r--r--) | Template files |
| `*.py` | 644 (rw-r--r--) | Python source files |
| `.env` | 600 (rw-------) | Environment configuration |

## 🔒 **Security Considerations**

### **File Security**
- `.env` file should never be committed to version control
- Upload directory should have proper file type restrictions
- Database files should not be web-accessible
- Log files should have restricted access

### **Directory Security**
- `venv/` directory should be excluded from deployment
- `__pycache__/` directories should be excluded
- Temporary files should be regularly cleaned up

## 📦 **Deployment Package**

### **Files to Include in Deployment**
```
✅ app.py, models.py, forms.py, utils.py
✅ run_enhanced.py, setup.py
✅ requirements.txt, .env.example
✅ routes/ directory (all files)
✅ templates/ directory (all files)
✅ static/ directory (all files)
✅ README.md, CHANGELOG.md, LICENSE
✅ CONFIGURATION_GUIDE.md, DEPLOYMENT_GUIDE.md
```

### **Files to Exclude from Deployment**
```
❌ venv/ directory
❌ __pycache__/ directories
❌ .env file (create new for production)
❌ instance/quickdesk.db (create new for production)
❌ uploads/ contents (create empty directory)
❌ Development logs and temporary files
```

---

This project structure provides a clean, organized, and maintainable codebase that follows Flask best practices and is ready for both development and production deployment.

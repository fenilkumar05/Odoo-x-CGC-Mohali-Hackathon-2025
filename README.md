# QuickDesk - Help Desk System

QuickDesk is a simple, easy-to-use help desk solution where users can raise support tickets, and support staff can manage and resolve them efficiently. The system aims to streamline communication between users and support teams without unnecessary complexity.

## Features

### Core Features
- **User Authentication**: Registration and login system with role-based access
- **Ticket Management**: Create, view, update, and track support tickets
- **Comment System**: Threaded conversations on tickets
- **File Attachments**: Support for file uploads on tickets
- **Voting System**: Users can upvote/downvote tickets
- **Email Notifications**: Automated notifications for ticket events
- **Search & Filtering**: Advanced search and filtering options
- **Responsive Design**: Mobile-friendly interface

### User Roles
- **End Users**: Can create and track their own tickets
- **Support Agents**: Can view, respond to, and manage all tickets
- **Administrators**: Full system access including user and category management

### Ticket Workflow
- **Open** → **In Progress** → **Resolved** → **Closed**
- Priority levels: Low, Medium, High, Urgent
- Category-based organization
- Agent assignment capabilities

## Technology Stack

- **Backend**: Python 3.10+ with Flask
- **Database**: SQLite (local development)
- **Frontend**: Bootstrap 5, HTML5, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Email**: Flask-Mail
- **File Handling**: Werkzeug

## Quick Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Automated Setup (Recommended)

1. **Clone or download the project**
   ```bash
   cd quick-desk
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Activate the virtual environment**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Start the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to: http://localhost:5000

### Manual Setup

If you prefer to set up manually:

1. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create necessary directories**
   ```bash
   mkdir uploads instance
   ```

5. **Set up environment variables**
   Copy `.env` file and update with your settings

6. **Initialize database**
   ```bash
   python app.py
   ```
   (The database will be created automatically on first run)

## Default Credentials

After setup, you can log in with the default admin account:
- **Email**: admin@quickdesk.com
- **Password**: admin123

**Important**: Change the default admin password after first login!

## Configuration

### Environment Variables (.env file)

```env
SECRET_KEY=your-secret-key-here-change-this-in-production
DATABASE_URL=sqlite:///quickdesk.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Email Configuration

To enable email notifications:
1. Update `MAIL_USERNAME` and `MAIL_PASSWORD` in `.env`
2. For Gmail, use an App Password instead of your regular password
3. Restart the application

## Project Structure

```
quick-desk/
├── app.py                 # Main application file
├── models.py             # Database models
├── forms.py              # WTForms definitions
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── setup.py             # Automated setup script
├── .env                 # Environment variables
├── routes/              # Route handlers
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── main.py          # Main dashboard routes
│   ├── tickets.py       # Ticket management routes
│   └── admin.py         # Admin panel routes
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Landing page
│   ├── dashboard.html   # Main dashboard
│   ├── profile.html     # User profile
│   ├── auth/           # Authentication templates
│   ├── tickets/        # Ticket templates
│   └── admin/          # Admin templates
└── uploads/            # File upload directory
```

## Usage Guide

### For End Users

1. **Register/Login**: Create an account or log in
2. **Create Ticket**: Click "New Ticket" and fill out the form
3. **Track Progress**: View your tickets on the dashboard
4. **Add Comments**: Communicate with support agents
5. **Vote**: Upvote/downvote tickets to show importance

### For Support Agents

1. **View All Tickets**: Access all tickets from the dashboard
2. **Assign Tickets**: Assign tickets to yourself or other agents
3. **Update Status**: Move tickets through the workflow
4. **Add Comments**: Respond to users and add internal notes
5. **Manage Workload**: Filter by assigned tickets

### For Administrators

1. **User Management**: Create, edit, and manage user accounts
2. **Category Management**: Create and organize ticket categories
3. **System Overview**: Monitor system statistics and activity
4. **Role Assignment**: Assign user roles (User, Agent, Admin)

## Features in Detail

### Ticket Management
- Rich text descriptions
- File attachments (images, documents)
- Priority levels and categories
- Status tracking and history
- Agent assignment

### Search and Filtering
- Full-text search across tickets
- Filter by status, category, priority
- Sort by date, votes, activity
- Pagination for large datasets

### Notification System
- Email notifications for ticket events
- Configurable notification preferences
- Real-time status updates

### Security Features
- Role-based access control
- Secure file upload handling
- CSRF protection
- Password hashing

## Customization

### Adding New Categories
1. Log in as admin
2. Go to Admin → Categories
3. Click "Create Category"
4. Fill out the form and save

### Creating Agent Accounts
1. Log in as admin
2. Go to Admin → Users
3. Click "Create User"
4. Set role to "Agent"

### Modifying Email Templates
Edit the email templates in `utils.py` in the `send_notification_email` function.

## Troubleshooting

### Common Issues

1. **Database errors**: Delete `quickdesk.db` and restart the app
2. **Email not working**: Check SMTP settings in `.env`
3. **File upload issues**: Ensure `uploads/` directory exists and is writable
4. **Permission errors**: Check file permissions on project directory

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure Python 3.10+ is being used
4. Check file permissions

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows
python app.py
```

### Database Reset
To reset the database:
```bash
rm quickdesk.db
python app.py
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

**QuickDesk** - Simple, efficient help desk management for teams of all sizes.

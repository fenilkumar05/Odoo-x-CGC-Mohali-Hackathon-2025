from flask import current_app
from flask_mail import Message, Mail
import os

# Mail instance will be imported when needed
mail = None

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_notification_email(ticket, event_type, recipient_email, **kwargs):
    """Send notification emails for ticket events"""
    try:
        # Get mail instance from current app
        from flask import current_app
        mail = current_app.extensions.get('mail')

        if not current_app.config.get('MAIL_USERNAME') or not mail:
            # Email not configured, skip sending
            return
        
        subject_map = {
            'created': f'New Ticket Created: {ticket.subject}',
            'commented': f'New Comment on Ticket: {ticket.subject}',
            'status_changed': f'Ticket Status Updated: {ticket.subject}',
            'assigned': f'Ticket Assigned to You: {ticket.subject}'
        }
        
        subject = subject_map.get(event_type, f'Ticket Update: {ticket.subject}')
        
        # Create email body based on event type
        if event_type == 'created':
            body = f"""
A new ticket has been created:

Ticket ID: #{ticket.id}
Subject: {ticket.subject}
Category: {ticket.category.name}
Priority: {ticket.priority.title()}
Created by: {ticket.creator.username}

Description:
{ticket.description}

You can view this ticket at: [Your QuickDesk URL]/tickets/{ticket.id}
"""
        elif event_type == 'commented':
            body = f"""
A new comment has been added to your ticket:

Ticket ID: #{ticket.id}
Subject: {ticket.subject}

You can view this ticket at: [Your QuickDesk URL]/tickets/{ticket.id}
"""
        elif event_type == 'status_changed':
            old_status = kwargs.get('old_status', 'Unknown')
            new_status = kwargs.get('new_status', 'Unknown')
            body = f"""
The status of your ticket has been updated:

Ticket ID: #{ticket.id}
Subject: {ticket.subject}
Status changed from: {old_status.title()} to {new_status.title()}

You can view this ticket at: [Your QuickDesk URL]/tickets/{ticket.id}
"""
        else:
            body = f"""
Your ticket has been updated:

Ticket ID: #{ticket.id}
Subject: {ticket.subject}

You can view this ticket at: [Your QuickDesk URL]/tickets/{ticket.id}
"""
        
        msg = Message(
            subject=subject,
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[recipient_email],
            body=body
        )
        
        mail.send(msg)
        
    except Exception as e:
        # Log the error but don't break the application
        current_app.logger.error(f'Failed to send email: {str(e)}')

def format_datetime(dt):
    """Format datetime for display"""
    if dt:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return ''

def get_status_badge_class(status):
    """Get CSS class for status badges"""
    status_classes = {
        'open': 'badge-primary',
        'in_progress': 'badge-warning',
        'resolved': 'badge-success',
        'closed': 'badge-secondary'
    }
    return status_classes.get(status, 'badge-secondary')

def get_priority_badge_class(priority):
    """Get CSS class for priority badges"""
    priority_classes = {
        'low': 'badge-success',
        'medium': 'badge-info',
        'high': 'badge-warning',
        'urgent': 'badge-danger'
    }
    return priority_classes.get(priority, 'badge-secondary')

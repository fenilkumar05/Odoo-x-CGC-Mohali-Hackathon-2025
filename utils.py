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
        from flask import current_app, url_for
        mail = current_app.extensions.get('mail')

        if not current_app.config.get('MAIL_USERNAME') or not mail:
            # Email not configured, skip sending
            return

        # Enhanced subject mapping
        subject_map = {
            'created': f'New Ticket Created: #{ticket.id} - {ticket.subject}',
            'commented': f'New Comment on Ticket: #{ticket.id} - {ticket.subject}',
            'comment_added': f'New Comment on Ticket: #{ticket.id} - {ticket.subject}',
            'status_changed': f'Ticket Status Updated: #{ticket.id} - {ticket.subject}',
            'assigned': f'Ticket Assigned: #{ticket.id} - {ticket.subject}',
            'assigned_to_you': f'Ticket Assigned to You: #{ticket.id} - {ticket.subject}',
            'agent_accepted': f'Agent Accepted Your Ticket: #{ticket.id} - {ticket.subject}',
            'escalated': f'Ticket Escalated: #{ticket.id} - {ticket.subject}',
            'video_call_started': f'Video Call Started: #{ticket.id} - {ticket.subject}'
        }

        subject = subject_map.get(event_type, f'Ticket Update: #{ticket.id} - {ticket.subject}')

        # Create email body based on event type
        if event_type == 'created':
            body = f"""
A new support ticket has been created.

Ticket Details:
- ID: #{ticket.id}
- Subject: {ticket.subject}
- Priority: {ticket.priority.title()}
- Category: {ticket.category.name}
- Created by: {ticket.creator.username}

Description:
{ticket.description}

You can view and respond to this ticket at: {url_for('tickets.view_ticket', id=ticket.id, _external=True)}

Best regards,
QuickDesk Support Team
"""

        elif event_type == 'assigned':
            agent_name = kwargs.get('agent_name', 'Unknown Agent')
            body = f"""
Your support ticket has been assigned to an agent.

Ticket Details:
- ID: #{ticket.id}
- Subject: {ticket.subject}
- Assigned to: {agent_name}

The agent will review your ticket and respond soon.

You can view the ticket status at: {url_for('tickets.view_ticket', id=ticket.id, _external=True)}

Best regards,
QuickDesk Support Team
"""

        elif event_type == 'agent_accepted':
            agent_name = kwargs.get('agent_name', 'Unknown Agent')
            agent_phone = kwargs.get('agent_phone', 'Not provided')
            agent_email = kwargs.get('agent_email', 'Not provided')
            body = f"""
Great news! Agent {agent_name} has accepted your problem for resolution.

Ticket Details:
- ID: #{ticket.id}
- Subject: {ticket.subject}
- Agent: {agent_name}
- Agent Contact: {agent_phone}
- Agent Email: {agent_email}

Your assigned agent will work on resolving your issue and will keep you updated on the progress.

You can view the ticket and communicate with your agent at: {url_for('tickets.view_ticket', id=ticket.id, _external=True)}

Best regards,
QuickDesk Support Team
"""

        elif event_type == 'assigned_to_you':
            assigner_name = kwargs.get('assigner_name', 'Administrator')
            body = f"""
A support ticket has been assigned to you by {assigner_name}.

Ticket Details:
- ID: #{ticket.id}
- Subject: {ticket.subject}
- Priority: {ticket.priority.title()}
- Category: {ticket.category.name}
- Created by: {ticket.creator.username}

Description:
{ticket.description}

Please review and respond to this ticket at: {url_for('tickets.view_ticket', id=ticket.id, _external=True)}

Best regards,
QuickDesk Support Team
"""

        elif event_type == 'status_changed':
            old_status = kwargs.get('old_status', 'Unknown')
            new_status = kwargs.get('new_status', 'Unknown')
            body = f"""
Your support ticket status has been updated.

Ticket Details:
- ID: #{ticket.id}
- Subject: {ticket.subject}
- Status changed from: {old_status.title()}
- Status changed to: {new_status.title()}

You can view the ticket at: {url_for('tickets.view_ticket', id=ticket.id, _external=True)}

Best regards,
QuickDesk Support Team
"""

        elif event_type in ['commented', 'comment_added']:
            commenter_name = kwargs.get('commenter_name', 'Unknown User')
            commenter_role = kwargs.get('commenter_role', 'User')
            body = f"""
A new comment has been added to your support ticket.

Ticket Details:
- ID: #{ticket.id}
- Subject: {ticket.subject}
- Comment by: {commenter_name} ({commenter_role})

You can view the comment and respond at: {url_for('tickets.view_ticket', id=ticket.id, _external=True)}

Best regards,
QuickDesk Support Team
"""

        elif event_type == 'escalated':
            escalation_reason = kwargs.get('escalation_reason', 'Manual escalation')
            body = f"""
Your support ticket has been escalated for priority handling.

Ticket Details:
- ID: #{ticket.id}
- Subject: {ticket.subject}
- Escalation Reason: {escalation_reason}
- New Priority: Urgent

Our team will prioritize this ticket and work on a resolution as soon as possible.

You can view the ticket at: {url_for('tickets.view_ticket', id=ticket.id, _external=True)}

Best regards,
QuickDesk Support Team
"""

        elif event_type == 'video_call_started':
            room_name = kwargs.get('room_name', 'Unknown Room')
            body = f"""
A video call has been started for your support ticket.

Ticket Details:
- ID: #{ticket.id}
- Subject: {ticket.subject}
- Video Call Room: {room_name}

Join the video call at: {url_for('tickets.video_call', id=ticket.id, _external=True)}

Best regards,
QuickDesk Support Team
"""

        else:
            body = f"""
Your ticket has been updated:

Ticket ID: #{ticket.id}
Subject: {ticket.subject}

You can view this ticket at: {url_for('tickets.view_ticket', id=ticket.id, _external=True)}

Best regards,
QuickDesk Support Team
"""

        msg = Message(
            subject=subject,
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[recipient_email],
            body=body
        )

        mail.send(msg)
        return True

    except Exception as e:
        # Log the error but don't break the application
        current_app.logger.error(f'Failed to send email: {str(e)}')
        return False

def format_datetime(dt):
    """Format datetime for display"""
    if dt:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return ''

def time_ago(dt):
    """Format datetime as 'time ago' (e.g., '2 hours ago')"""
    if not dt:
        return 'Unknown'

    from datetime import datetime, timezone
    import math

    # Ensure dt is timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    diff = now - dt

    seconds = diff.total_seconds()

    if seconds < 60:
        return 'Just now'
    elif seconds < 3600:  # Less than 1 hour
        minutes = math.floor(seconds / 60)
        return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
    elif seconds < 86400:  # Less than 1 day
        hours = math.floor(seconds / 3600)
        return f'{hours} hour{"s" if hours != 1 else ""} ago'
    elif seconds < 2592000:  # Less than 30 days
        days = math.floor(seconds / 86400)
        return f'{days} day{"s" if days != 1 else ""} ago'
    elif seconds < 31536000:  # Less than 1 year
        months = math.floor(seconds / 2592000)
        return f'{months} month{"s" if months != 1 else ""} ago'
    else:
        years = math.floor(seconds / 31536000)
        return f'{years} year{"s" if years != 1 else ""} ago'

def format_full_datetime(dt):
    """Format datetime for detailed display (e.g., 'Posted on Dec 15, 2024 at 3:30 PM')"""
    if not dt:
        return 'Unknown date'

    return dt.strftime('Posted on %b %d, %Y at %I:%M %p')

def get_user_role_display(user):
    """Get user role for display with proper formatting"""
    if not user:
        return 'Unknown'

    role_map = {
        'admin': 'Administrator',
        'agent': 'Support Agent',
        'user': 'End User'
    }

    return role_map.get(user.role, user.role.title())

def get_user_display_name(user):
    """Get user's display name (first name + last name or username)"""
    if not user:
        return 'Unknown User'

    if user.first_name and user.last_name:
        return f'{user.first_name} {user.last_name}'
    elif user.first_name:
        return user.first_name
    else:
        return user.username

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

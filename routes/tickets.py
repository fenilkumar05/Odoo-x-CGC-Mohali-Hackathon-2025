from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_from_directory, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import Ticket, Category, Comment, Vote, Attachment, User, Tag, TicketActivity, db
from forms import TicketForm, CommentForm
from utils import send_notification_email, allowed_file
import os
import uuid
from datetime import datetime

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(is_active=True).all()]

    if form.validate_on_submit():
        ticket = Ticket(
            subject=form.subject.data,
            description=form.description.data,
            category_id=form.category.data,
            user_id=current_user.id,
            priority=form.priority.data
        )

        db.session.add(ticket)
        db.session.flush()  # Get the ticket ID

        # Handle tags
        if form.tags.data:
            tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
            for tag_name in tag_names:
                # Get or create tag
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.flush()

                # Associate tag with ticket
                if tag not in ticket.tags:
                    ticket.tags.append(tag)

        # Handle file upload
        if form.attachment.data:
            file = form.attachment.data
            if file and allowed_file(file.filename):
                filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                attachment = Attachment(
                    filename=filename,
                    original_filename=file.filename,
                    file_size=os.path.getsize(file_path),
                    mime_type=file.content_type,
                    ticket_id=ticket.id,
                    user_id=current_user.id
                )
                db.session.add(attachment)

        # Create activity log
        activity = TicketActivity(
            ticket_id=ticket.id,
            user_id=current_user.id,
            activity_type='created',
            description=f'Ticket created by {current_user.username}'
        )
        db.session.add(activity)

        db.session.commit()

        # Send notification email
        send_notification_email(
            ticket=ticket,
            event_type='created',
            recipient_email=current_user.email
        )

        flash('Ticket created successfully!', 'success')
        return redirect(url_for('tickets.view_ticket', id=ticket.id))

    # Get popular tags for suggestions
    popular_tags = Tag.query.join(Tag.tickets).group_by(Tag.id).order_by(db.func.count(Ticket.id).desc()).limit(10).all()

    return render_template('tickets/create.html', form=form, popular_tags=popular_tags)

@tickets_bp.route('/<int:id>')
@login_required
def view_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    
    # Check permissions
    if not current_user.is_agent() and ticket.user_id != current_user.id:
        flash('You do not have permission to view this ticket.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get comments
    comments = Comment.query.filter_by(ticket_id=id).order_by(Comment.created_at.asc()).all()
    
    # Filter internal comments for non-agents
    if not current_user.is_agent():
        comments = [c for c in comments if not c.is_internal]
    
    # Get user's vote
    user_vote = None
    if current_user.is_authenticated:
        vote = Vote.query.filter_by(ticket_id=id, user_id=current_user.id).first()
        user_vote = vote.vote_type if vote else None
    
    form = CommentForm()
    
    return render_template('tickets/view.html', 
                         ticket=ticket, 
                         comments=comments, 
                         form=form,
                         user_vote=user_vote)

@tickets_bp.route('/<int:id>/comment', methods=['POST'])
@login_required
def add_comment(id):
    ticket = Ticket.query.get_or_404(id)
    
    # Check permissions
    if not current_user.is_agent() and ticket.user_id != current_user.id:
        flash('You do not have permission to comment on this ticket.', 'error')
        return redirect(url_for('main.dashboard'))
    
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            ticket_id=id,
            user_id=current_user.id,
            is_internal=form.is_internal.data if current_user.is_agent() else False
        )
        
        db.session.add(comment)
        
        # Update ticket timestamp
        ticket.updated_at = db.func.now()
        
        db.session.commit()
        
        flash('Comment added successfully!', 'success')
        
        # Send notification email
        recipient_email = ticket.creator.email if current_user.id != ticket.user_id else None
        if recipient_email:
            send_notification_email(
                ticket=ticket,
                event_type='commented',
                recipient_email=recipient_email
            )
    
    return redirect(url_for('tickets.view_ticket', id=id))

@tickets_bp.route('/<int:id>/vote', methods=['POST'])
@login_required
def vote_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    vote_type = request.json.get('vote_type')
    
    if vote_type not in ['up', 'down']:
        return jsonify({'error': 'Invalid vote type'}), 400
    
    # Check if user already voted
    existing_vote = Vote.query.filter_by(ticket_id=id, user_id=current_user.id).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Remove vote if clicking same vote
            db.session.delete(existing_vote)
            action = 'removed'
        else:
            # Change vote
            existing_vote.vote_type = vote_type
            action = 'changed'
    else:
        # Add new vote
        vote = Vote(ticket_id=id, user_id=current_user.id, vote_type=vote_type)
        db.session.add(vote)
        action = 'added'
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'action': action,
        'vote_score': ticket.vote_score
    })

@tickets_bp.route('/<int:id>/assign', methods=['POST'])
@login_required
def assign_ticket(id):
    if not current_user.is_agent():
        return jsonify({'error': 'Permission denied'}), 403

    ticket = Ticket.query.get_or_404(id)
    agent_id = request.json.get('agent_id')
    is_self_assignment = request.json.get('self_assign', False)

    # Handle self-assignment
    if is_self_assignment:
        agent_id = current_user.id
        agent = current_user
    else:
        if not agent_id:
            # Unassign ticket
            old_assignee = ticket.assignee
            ticket.assigned_to = None

            # Create activity log
            activity = TicketActivity(
                ticket_id=ticket.id,
                user_id=current_user.id,
                activity_type='unassigned',
                description=f'Ticket unassigned from {old_assignee.username if old_assignee else "unknown"}',
                old_value=old_assignee.username if old_assignee else None,
                new_value=None
            )
            db.session.add(activity)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Ticket unassigned'})

        agent = User.query.get(agent_id)
        if not agent or not agent.is_agent():
            return jsonify({'error': 'Invalid agent'}), 400

        # Only admins can assign to other agents
        if not current_user.is_admin() and agent_id != current_user.id:
            return jsonify({'error': 'Only admins can assign tickets to other agents'}), 403

    # Update ticket assignment
    old_assignee = ticket.assignee
    ticket.assigned_to = agent_id

    # Create activity log
    activity = TicketActivity(
        ticket_id=ticket.id,
        user_id=current_user.id,
        activity_type='assigned',
        description=f'Ticket assigned to {agent.username}' + (' (self-assigned)' if is_self_assignment else ''),
        old_value=old_assignee.username if old_assignee else None,
        new_value=agent.username
    )
    db.session.add(activity)
    db.session.commit()

    # Send notification to ticket creator
    try:
        if is_self_assignment:
            # Special notification for self-assignment
            send_notification_email(
                ticket=ticket,
                event_type='agent_accepted',
                recipient_email=ticket.creator.email,
                agent_name=agent.username,
                agent_phone=agent.phone or 'Not provided',
                agent_email=agent.email
            )
        else:
            # Regular assignment notification
            send_notification_email(
                ticket=ticket,
                event_type='assigned',
                recipient_email=ticket.creator.email,
                agent_name=agent.username
            )

        # Send notification to assigned agent if different from current user
        if agent_id != current_user.id:
            send_notification_email(
                ticket=ticket,
                event_type='assigned_to_you',
                recipient_email=agent.email,
                assigner_name=current_user.username
            )
    except Exception as e:
        print(f"Error sending assignment notification: {e}")

    return jsonify({
        'success': True,
        'agent_name': agent.username,
        'agent_phone': agent.phone,
        'agent_email': agent.email,
        'is_self_assignment': is_self_assignment,
        'message': f'Ticket assigned to {agent.username}' + (' (self-assigned)' if is_self_assignment else '')
    })

@tickets_bp.route('/<int:id>/self-assign', methods=['POST'])
@login_required
def self_assign_ticket(id):
    """Allow agents to self-assign tickets"""
    if not current_user.is_agent():
        return jsonify({'error': 'Permission denied'}), 403

    ticket = Ticket.query.get_or_404(id)

    # Check if ticket is already assigned
    if ticket.assigned_to:
        return jsonify({'error': 'Ticket is already assigned'}), 400

    # Assign to current user
    ticket.assigned_to = current_user.id

    # Create activity log
    activity = TicketActivity(
        ticket_id=ticket.id,
        user_id=current_user.id,
        activity_type='self_assigned',
        description=f'{current_user.username} accepted this ticket for resolution',
        new_value=current_user.username
    )
    db.session.add(activity)
    db.session.commit()

    # Send notification to ticket creator
    try:
        send_notification_email(
            ticket=ticket,
            event_type='agent_accepted',
            recipient_email=ticket.creator.email,
            agent_name=current_user.username,
            agent_phone=current_user.phone or 'Not provided',
            agent_email=current_user.email
        )
    except Exception as e:
        print(f"Error sending self-assignment notification: {e}")

    return jsonify({
        'success': True,
        'message': f'You have successfully accepted ticket #{ticket.id}',
        'agent_name': current_user.username,
        'agent_phone': current_user.phone,
        'agent_email': current_user.email
    })

@tickets_bp.route('/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    if not current_user.is_agent():
        return jsonify({'error': 'Permission denied'}), 403

    ticket = Ticket.query.get_or_404(id)
    new_status = request.json.get('status')

    if new_status not in ['open', 'in_progress', 'resolved', 'closed']:
        return jsonify({'error': 'Invalid status'}), 400

    # Check if agent can update status
    if not current_user.is_admin():
        # Agents can only update status if they are assigned to the ticket
        if ticket.assigned_to != current_user.id:
            return jsonify({
                'error': 'You must be assigned to this ticket to update its status. Please accept the ticket first.'
            }), 403

    old_status = ticket.status
    ticket.status = new_status
    ticket.updated_at = db.func.now()

    # Create activity log
    activity = TicketActivity(
        ticket_id=ticket.id,
        user_id=current_user.id,
        activity_type='status_changed',
        description=f'Status changed from {old_status} to {new_status} by {current_user.username}',
        old_value=old_status,
        new_value=new_status
    )
    db.session.add(activity)
    db.session.commit()

    # Send notification email
    send_notification_email(
        ticket=ticket,
        event_type='status_changed',
        recipient_email=ticket.creator.email,
        old_status=old_status,
        new_status=new_status
    )

    return jsonify({
        'success': True,
        'message': f'Ticket status updated to {new_status.replace("_", " ").title()}'
    })

@tickets_bp.route('/attachment/<filename>')
@login_required
def download_attachment(filename):
    attachment = Attachment.query.filter_by(filename=filename).first_or_404()
    ticket = attachment.ticket
    
    # Check permissions
    if not current_user.is_agent() and ticket.user_id != current_user.id:
        flash('You do not have permission to download this file.', 'error')
        return redirect(url_for('main.dashboard'))
    
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename,
                             as_attachment=True, download_name=attachment.original_filename)

# Video call functionality removed as requested

@tickets_bp.route('/<int:id>/escalate', methods=['POST'])
@login_required
def escalate_ticket(id):
    if not current_user.is_agent():
        return jsonify({'error': 'Permission denied'}), 403

    ticket = Ticket.query.get_or_404(id)
    reason = request.json.get('reason', 'Manual escalation')

    # Create escalation record
    from models import TicketEscalation
    escalation = TicketEscalation(
        ticket_id=ticket.id,
        escalated_by=current_user.id,
        escalation_reason=reason
    )
    db.session.add(escalation)

    # Update ticket priority if not already urgent
    if ticket.priority != 'urgent':
        old_priority = ticket.priority
        ticket.priority = 'urgent'

        # Create activity log
        activity = TicketActivity(
            ticket_id=ticket.id,
            user_id=current_user.id,
            activity_type='escalated',
            description=f'Ticket escalated by {current_user.username}',
            old_value=old_priority,
            new_value='urgent'
        )
        db.session.add(activity)

    db.session.commit()

    # Send notification
    send_notification_email(
        ticket=ticket,
        event_type='escalated',
        recipient_email=ticket.creator.email,
        escalation_reason=reason
    )

    return jsonify({'success': True})

@tickets_bp.route('/api/tags/search')
@login_required
def search_tags():
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])

    tags = Tag.query.filter(Tag.name.contains(query)).filter_by(is_active=True).limit(10).all()
    return jsonify([{'id': tag.id, 'name': tag.name, 'color': tag.color} for tag in tags])

@tickets_bp.route('/api/auto-assign')
@login_required
def auto_assign_tickets():
    if not current_user.is_admin():
        return jsonify({'error': 'Permission denied'}), 403

    # Get unassigned tickets
    unassigned_tickets = Ticket.query.filter(
        Ticket.assigned_to.is_(None),
        Ticket.status.in_(['open', 'in_progress'])
    ).all()

    # Get available agents
    agents = User.query.filter_by(role='agent', is_active=True).all()

    if not agents:
        return jsonify({'error': 'No available agents'}), 400

    assigned_count = 0
    for i, ticket in enumerate(unassigned_tickets):
        agent = agents[i % len(agents)]  # Round-robin assignment
        ticket.assigned_to = agent.id

        # Create activity log
        activity = TicketActivity(
            ticket_id=ticket.id,
            user_id=current_user.id,
            activity_type='auto_assigned',
            description=f'Auto-assigned to {agent.username}',
            new_value=agent.username
        )
        db.session.add(activity)

        assigned_count += 1

    db.session.commit()

    return jsonify({'success': True, 'assigned_count': assigned_count})

@tickets_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ticket(id):
    if not current_user.is_admin():
        flash('Permission denied. Only administrators can edit tickets.', 'error')
        return redirect(url_for('tickets.view_ticket', id=id))

    ticket = Ticket.query.get_or_404(id)
    form = TicketForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(is_active=True).all()]

    if form.validate_on_submit():
        # Store old values for activity log
        old_subject = ticket.subject
        old_description = ticket.description
        old_priority = ticket.priority
        old_category = ticket.category.name

        # Update ticket
        ticket.subject = form.subject.data
        ticket.description = form.description.data
        ticket.priority = form.priority.data
        ticket.category_id = form.category.data
        ticket.updated_at = db.func.now()

        # Handle tags
        if form.tags.data:
            # Clear existing tags
            ticket.tags.clear()

            tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
            for tag_name in tag_names:
                # Get or create tag
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.flush()

                # Associate tag with ticket
                if tag not in ticket.tags:
                    ticket.tags.append(tag)

        # Create activity log
        changes = []
        if old_subject != ticket.subject:
            changes.append(f'Subject: "{old_subject}" → "{ticket.subject}"')
        if old_description != ticket.description:
            changes.append(f'Description updated')
        if old_priority != ticket.priority:
            changes.append(f'Priority: {old_priority} → {ticket.priority}')
        if old_category != ticket.category.name:
            changes.append(f'Category: {old_category} → {ticket.category.name}')

        if changes:
            activity = TicketActivity(
                ticket_id=ticket.id,
                user_id=current_user.id,
                activity_type='edited',
                description=f'Ticket edited by {current_user.username}: {"; ".join(changes)}'
            )
            db.session.add(activity)

        db.session.commit()

        flash('Ticket updated successfully!', 'success')
        return redirect(url_for('tickets.view_ticket', id=ticket.id))

    # Pre-populate form
    if request.method == 'GET':
        form.subject.data = ticket.subject
        form.description.data = ticket.description
        form.priority.data = ticket.priority
        form.category.data = ticket.category_id
        form.tags.data = ', '.join([tag.name for tag in ticket.tags])

    return render_template('tickets/edit.html', form=form, ticket=ticket)

@tickets_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_ticket(id):
    if not current_user.is_admin():
        return jsonify({'error': 'Permission denied. Only administrators can delete tickets.'}), 403

    ticket = Ticket.query.get_or_404(id)

    try:
        # Delete related records first
        Comment.query.filter_by(ticket_id=ticket.id).delete()
        Vote.query.filter_by(ticket_id=ticket.id).delete()
        Attachment.query.filter_by(ticket_id=ticket.id).delete()
        TicketActivity.query.filter_by(ticket_id=ticket.id).delete()

        # Clear tag associations
        ticket.tags.clear()

        # Delete the ticket
        db.session.delete(ticket)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Ticket #{ticket.id} has been permanently deleted.'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Failed to delete ticket: {str(e)}'
        }), 500

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_from_directory, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import Ticket, Category, Comment, Vote, Attachment, User, db
from forms import TicketForm, CommentForm
from utils import send_notification_email, allowed_file
import os
import uuid

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
        
        db.session.commit()
        
        # Send notification email
        send_notification_email(
            ticket=ticket,
            event_type='created',
            recipient_email=current_user.email
        )
        
        flash('Ticket created successfully!', 'success')
        return redirect(url_for('tickets.view_ticket', id=ticket.id))
    
    return render_template('tickets/create.html', form=form)

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
    
    if agent_id:
        agent = User.query.get(agent_id)
        if not agent or not agent.is_agent():
            return jsonify({'error': 'Invalid agent'}), 400
        ticket.assigned_to = agent_id
    else:
        ticket.assigned_to = None
    
    db.session.commit()
    
    return jsonify({'success': True})

@tickets_bp.route('/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    if not current_user.is_agent():
        return jsonify({'error': 'Permission denied'}), 403
    
    ticket = Ticket.query.get_or_404(id)
    new_status = request.json.get('status')
    
    if new_status not in ['open', 'in_progress', 'resolved', 'closed']:
        return jsonify({'error': 'Invalid status'}), 400
    
    old_status = ticket.status
    ticket.status = new_status
    ticket.updated_at = db.func.now()
    
    db.session.commit()
    
    # Send notification email
    send_notification_email(
        ticket=ticket,
        event_type='status_changed',
        recipient_email=ticket.creator.email,
        old_status=old_status,
        new_status=new_status
    )
    
    return jsonify({'success': True})

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

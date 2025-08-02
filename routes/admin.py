from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from functools import wraps
from models import User, Category, Ticket, Comment, Vote, Attachment, TicketActivity, NotificationSettings, Tag, db
from forms import CategoryForm, UserForm
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def admin_dashboard():
    # Get statistics
    stats = {
        'total_users': User.query.count(),
        'total_tickets': Ticket.query.count(),
        'total_categories': Category.query.count(),
        'open_tickets': Ticket.query.filter_by(status='open').count(),
        'in_progress_tickets': Ticket.query.filter_by(status='in_progress').count(),
        'resolved_tickets': Ticket.query.filter_by(status='resolved').count(),
        'closed_tickets': Ticket.query.filter_by(status='closed').count(),
    }
    
    # Recent tickets
    recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(5).all()
    
    # Recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_tickets=recent_tickets,
                         recent_users=recent_users)

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    role_filter = request.args.get('role', 'all')
    
    query = User.query
    
    if search:
        query = query.filter(
            db.or_(
                User.username.contains(search),
                User.email.contains(search)
            )
        )
    
    if role_filter != 'all':
        query = query.filter_by(role=role_filter)
    
    users = query.paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/users.html', users=users, 
                         search=search, role_filter=role_filter)

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    form = UserForm()
    
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('admin/create_user.html', form=form)
        
        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username:
            flash('Username already taken', 'error')
            return render_template('admin/create_user.html', form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role=form.role.data
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('User created successfully!', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/create_user.html', form=form)

@admin_bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        # Check for duplicate email (excluding current user)
        existing_user = User.query.filter(User.email == form.email.data, User.id != id).first()
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('admin/edit_user.html', form=form, user=user)
        
        # Check for duplicate username (excluding current user)
        existing_username = User.query.filter(User.username == form.username.data, User.id != id).first()
        if existing_username:
            flash('Username already taken', 'error')
            return render_template('admin/edit_user.html', form=form, user=user)
        
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        user.is_active = form.is_active.data
        
        if form.password.data:
            user.password_hash = generate_password_hash(form.password.data)
        
        db.session.commit()
        
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/edit_user.html', form=form, user=user)

@admin_bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    """Delete a user and all associated data"""
    if id == current_user.id:
        return jsonify({'error': 'You cannot delete your own account.'}), 400

    user = User.query.get_or_404(id)

    try:
        # Delete user's tickets and associated data
        for ticket in user.tickets:
            # Delete ticket comments
            Comment.query.filter_by(ticket_id=ticket.id).delete()
            # Delete ticket votes
            Vote.query.filter_by(ticket_id=ticket.id).delete()
            # Delete ticket attachments
            Attachment.query.filter_by(ticket_id=ticket.id).delete()
            # Delete ticket activities
            TicketActivity.query.filter_by(ticket_id=ticket.id).delete()
            # Clear tag associations
            ticket.tags.clear()
            # Delete the ticket
            db.session.delete(ticket)

        # Delete user's comments on other tickets
        Comment.query.filter_by(user_id=user.id).delete()

        # Delete user's votes
        Vote.query.filter_by(user_id=user.id).delete()

        # Delete user's activities
        TicketActivity.query.filter_by(user_id=user.id).delete()

        # Delete user's notification settings
        NotificationSettings.query.filter_by(user_id=user.id).delete()

        # Update tickets assigned to this user
        Ticket.query.filter_by(assigned_to=user.id).update({'assigned_to': None})

        # Delete the user
        username = user.username
        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'User {username} and all associated data have been permanently deleted.'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Failed to delete user: {str(e)}'
        }), 500

@admin_bp.route('/categories')
@login_required
@admin_required
def manage_categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/categories/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_category():
    form = CategoryForm()
    
    if form.validate_on_submit():
        # Check if category already exists
        existing_category = Category.query.filter_by(name=form.name.data).first()
        if existing_category:
            flash('Category already exists', 'error')
            return render_template('admin/create_category.html', form=form)
        
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin.manage_categories'))
    
    return render_template('admin/create_category.html', form=form)

@admin_bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        # Check for duplicate name (excluding current category)
        existing_category = Category.query.filter(Category.name == form.name.data, Category.id != id).first()
        if existing_category:
            flash('Category name already exists', 'error')
            return render_template('admin/edit_category.html', form=form, category=category)
        
        category.name = form.name.data
        category.description = form.description.data
        category.is_active = form.is_active.data
        
        db.session.commit()
        
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin.manage_categories'))
    
    return render_template('admin/edit_category.html', form=form, category=category)

@admin_bp.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    
    # Check if category has tickets
    if category.tickets:
        return jsonify({'error': 'Cannot delete category with existing tickets'}), 400
    
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'success': True})

# Duplicate function removed - using the enhanced version above

@admin_bp.route('/assign-ticket', methods=['POST'])
@login_required
@admin_required
def assign_ticket_admin():
    """Admin assignment of tickets to agents"""
    ticket_id = request.json.get('ticket_id')
    agent_id = request.json.get('agent_id')

    if not ticket_id:
        return jsonify({'error': 'Ticket ID is required'}), 400

    ticket = Ticket.query.get_or_404(ticket_id)

    if agent_id:
        agent = User.query.get(agent_id)
        if not agent or not agent.is_agent():
            return jsonify({'error': 'Invalid agent selected'}), 400

        old_assignee = ticket.assignee
        ticket.assigned_to = agent_id

        # Create activity log
        activity = TicketActivity(
            ticket_id=ticket.id,
            user_id=current_user.id,
            activity_type='assigned',
            description=f'Ticket assigned to {agent.username} by admin {current_user.username}',
            old_value=old_assignee.username if old_assignee else None,
            new_value=agent.username
        )
        db.session.add(activity)
        db.session.commit()

        # Send notifications
        try:
            from utils import send_notification_email
            # Notify the assigned agent
            send_notification_email(
                ticket=ticket,
                event_type='assigned_to_you',
                recipient_email=agent.email,
                assigner_name=current_user.username
            )

            # Notify the ticket creator
            send_notification_email(
                ticket=ticket,
                event_type='assigned',
                recipient_email=ticket.creator.email,
                agent_name=agent.username
            )
        except Exception as e:
            print(f"Error sending assignment notification: {e}")

        return jsonify({
            'success': True,
            'message': f'Ticket assigned to {agent.username}',
            'agent_name': agent.username
        })
    else:
        # Unassign ticket
        old_assignee = ticket.assignee
        ticket.assigned_to = None

        # Create activity log
        activity = TicketActivity(
            ticket_id=ticket.id,
            user_id=current_user.id,
            activity_type='unassigned',
            description=f'Ticket unassigned by admin {current_user.username}',
            old_value=old_assignee.username if old_assignee else None,
            new_value=None
        )
        db.session.add(activity)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Ticket unassigned'
        })

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models import Ticket, Category, User, db
from sqlalchemy import or_, desc, asc

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    category_filter = request.args.get('category', 'all')
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'recent')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Base query
    if current_user.is_agent():
        # Agents can see all tickets
        query = Ticket.query
    else:
        # Regular users can only see their own tickets
        query = Ticket.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if status_filter != 'all':
        if status_filter == 'open':
            query = query.filter(Ticket.status.in_(['open', 'in_progress']))
        elif status_filter == 'closed':
            query = query.filter(Ticket.status.in_(['resolved', 'closed']))
        else:
            query = query.filter_by(status=status_filter)
    
    if category_filter != 'all':
        query = query.filter_by(category_id=category_filter)
    
    if search_query:
        query = query.filter(
            or_(
                Ticket.subject.contains(search_query),
                Ticket.description.contains(search_query)
            )
        )
    
    # Apply sorting
    if sort_by == 'recent':
        query = query.order_by(desc(Ticket.updated_at))
    elif sort_by == 'oldest':
        query = query.order_by(asc(Ticket.created_at))
    elif sort_by == 'most_replied':
        # This would need a more complex query in production
        query = query.order_by(desc(Ticket.updated_at))
    elif sort_by == 'votes':
        # This would need a more complex query in production
        query = query.order_by(desc(Ticket.created_at))
    
    # Paginate results
    tickets = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get categories for filter dropdown
    categories = Category.query.filter_by(is_active=True).all()
    
    # Get statistics
    stats = {}
    if current_user.is_agent():
        stats['total_tickets'] = Ticket.query.count()
        stats['open_tickets'] = Ticket.query.filter(Ticket.status.in_(['open', 'in_progress'])).count()
        stats['my_assigned'] = Ticket.query.filter_by(assigned_to=current_user.id).count()
    else:
        stats['my_tickets'] = Ticket.query.filter_by(user_id=current_user.id).count()
        stats['open_tickets'] = Ticket.query.filter_by(user_id=current_user.id).filter(
            Ticket.status.in_(['open', 'in_progress'])
        ).count()
    
    return render_template('dashboard.html', 
                         tickets=tickets, 
                         categories=categories,
                         stats=stats,
                         current_filters={
                             'status': status_filter,
                             'category': category_filter,
                             'search': search_query,
                             'sort': sort_by
                         })

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main_bp.route('/api/ticket-stats')
@login_required
def ticket_stats():
    """API endpoint for dashboard statistics"""
    if current_user.is_agent():
        stats = {
            'total': Ticket.query.count(),
            'open': Ticket.query.filter_by(status='open').count(),
            'in_progress': Ticket.query.filter_by(status='in_progress').count(),
            'resolved': Ticket.query.filter_by(status='resolved').count(),
            'closed': Ticket.query.filter_by(status='closed').count(),
        }
    else:
        user_tickets = Ticket.query.filter_by(user_id=current_user.id)
        stats = {
            'total': user_tickets.count(),
            'open': user_tickets.filter_by(status='open').count(),
            'in_progress': user_tickets.filter_by(status='in_progress').count(),
            'resolved': user_tickets.filter_by(status='resolved').count(),
            'closed': user_tickets.filter_by(status='closed').count(),
        }
    
    return jsonify(stats)

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models import Ticket, Category, User, Tag, TicketActivity, db
from sqlalchemy import or_, desc, asc, func
from datetime import datetime, timedelta

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

@main_bp.route('/agent-dashboard')
@login_required
def agent_dashboard():
    if not current_user.is_agent():
        flash('Access denied. Agent privileges required.', 'error')
        return redirect(url_for('main.dashboard'))

    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    category_filter = request.args.get('category', 'all')
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'recent')
    assigned_filter = request.args.get('assigned', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 15

    # Base query for all tickets (agents can see all)
    query = Ticket.query

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

    if assigned_filter == 'me':
        query = query.filter_by(assigned_to=current_user.id)
    elif assigned_filter == 'unassigned':
        query = query.filter(Ticket.assigned_to.is_(None))

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
    elif sort_by == 'priority':
        # Custom priority ordering
        priority_order = {'urgent': 4, 'high': 3, 'medium': 2, 'low': 1}
        query = query.order_by(
            func.case(
                (Ticket.priority == 'urgent', 4),
                (Ticket.priority == 'high', 3),
                (Ticket.priority == 'medium', 2),
                (Ticket.priority == 'low', 1),
                else_=0
            ).desc(),
            desc(Ticket.created_at)
        )

    # Paginate results
    tickets = query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Get categories for filter dropdown
    categories = Category.query.filter_by(is_active=True).all()

    # Get agent statistics
    stats = {
        'total_tickets': Ticket.query.count(),
        'open_tickets': Ticket.query.filter(Ticket.status.in_(['open', 'in_progress'])).count(),
        'my_assigned': Ticket.query.filter_by(assigned_to=current_user.id).count(),
        'unassigned': Ticket.query.filter(Ticket.assigned_to.is_(None)).count(),
        'resolved_today': Ticket.query.filter(
            Ticket.status == 'resolved',
            Ticket.updated_at >= datetime.utcnow().date()
        ).count(),
        'urgent_tickets': Ticket.query.filter_by(priority='urgent').filter(
            Ticket.status.in_(['open', 'in_progress'])
        ).count()
    }

    # Get recent activity
    recent_activity = TicketActivity.query.order_by(desc(TicketActivity.created_at)).limit(10).all()

    return render_template('agent_dashboard.html',
                         tickets=tickets,
                         categories=categories,
                         stats=stats,
                         recent_activity=recent_activity,
                         current_filters={
                             'status': status_filter,
                             'category': category_filter,
                             'search': search_query,
                             'sort': sort_by,
                             'assigned': assigned_filter
                         })

@main_bp.route('/analytics')
@login_required
def analytics():
    if not current_user.is_agent():
        flash('Access denied. Agent privileges required.', 'error')
        return redirect(url_for('main.dashboard'))

    # Get date range (default to last 30 days)
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)

    # Ticket statistics
    total_tickets = Ticket.query.count()
    tickets_in_period = Ticket.query.filter(Ticket.created_at >= start_date).count()

    # Status distribution
    status_stats = db.session.query(
        Ticket.status,
        func.count(Ticket.id).label('count')
    ).group_by(Ticket.status).all()

    # Category distribution
    category_stats = db.session.query(
        Category.name,
        func.count(Ticket.id).label('count')
    ).join(Ticket).group_by(Category.name).all()

    # Priority distribution
    priority_stats = db.session.query(
        Ticket.priority,
        func.count(Ticket.id).label('count')
    ).group_by(Ticket.priority).all()

    # Daily ticket creation (last 30 days)
    daily_stats = db.session.query(
        func.date(Ticket.created_at).label('date'),
        func.count(Ticket.id).label('count')
    ).filter(
        Ticket.created_at >= start_date
    ).group_by(func.date(Ticket.created_at)).order_by('date').all()

    # Agent performance
    agent_stats = db.session.query(
        User.username,
        func.count(Ticket.id).label('assigned_count'),
        func.count(func.case([(Ticket.status == 'resolved', 1)])).label('resolved_count')
    ).join(Ticket, User.id == Ticket.assigned_to).filter(
        User.role.in_(['agent', 'admin'])
    ).group_by(User.username).all()

    return render_template('analytics.html',
                         total_tickets=total_tickets,
                         tickets_in_period=tickets_in_period,
                         status_stats=status_stats,
                         category_stats=category_stats,
                         priority_stats=priority_stats,
                         daily_stats=daily_stats,
                         agent_stats=agent_stats,
                         days=days)

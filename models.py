from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Initialize db here, will be configured in app.py
db = SQLAlchemy()

# Association table for many-to-many relationship between tickets and tags
ticket_tags = db.Table('ticket_tags',
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, agent, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    avatar_url = db.Column(db.String(255))
    last_login = db.Column(db.DateTime)
    email_notifications = db.Column(db.Boolean, default=True)
    dark_mode = db.Column(db.Boolean, default=False)
    
    # Relationships
    tickets = db.relationship('Ticket', backref='creator', lazy=True, foreign_keys='Ticket.user_id')
    assigned_tickets = db.relationship('Ticket', backref='assignee', lazy=True, foreign_keys='Ticket.assigned_to')
    comments = db.relationship('Comment', backref='author', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_agent(self):
        return self.role in ['agent', 'admin']
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    tickets = db.relationship('Ticket', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Relationships
    comments = db.relationship('Comment', backref='ticket', lazy=True, cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='ticket', lazy=True, cascade='all, delete-orphan')
    attachments = db.relationship('Attachment', backref='ticket', lazy=True, cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary=ticket_tags, lazy='subquery', backref=db.backref('tickets', lazy=True))
    
    @property
    def vote_score(self):
        upvotes = Vote.query.filter_by(ticket_id=self.id, vote_type='up').count()
        downvotes = Vote.query.filter_by(ticket_id=self.id, vote_type='down').count()
        return upvotes - downvotes
    
    def __repr__(self):
        return f'<Ticket {self.subject}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_internal = db.Column(db.Boolean, default=False)  # Internal notes for agents
    
    # Foreign Keys
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.id}>'

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote_type = db.Column(db.String(10), nullable=False)  # up, down
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Unique constraint to prevent multiple votes from same user on same ticket
    __table_args__ = (db.UniqueConstraint('ticket_id', 'user_id', name='unique_vote'),)
    
    def __repr__(self):
        return f'<Vote {self.vote_type}>'

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Attachment {self.original_filename}>'

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(7), default='#007bff')  # Hex color code
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Tag {self.name}>'

class TicketEscalation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    escalated_at = db.Column(db.DateTime, default=datetime.utcnow)
    escalated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    escalation_reason = db.Column(db.String(255))
    resolved_at = db.Column(db.DateTime)

    # Relationships
    ticket = db.relationship('Ticket', backref='escalations')
    escalator = db.relationship('User', backref='escalations_created')

    def __repr__(self):
        return f'<TicketEscalation {self.id}>'

class NotificationSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    email_on_ticket_created = db.Column(db.Boolean, default=True)
    email_on_ticket_updated = db.Column(db.Boolean, default=True)
    email_on_comment_added = db.Column(db.Boolean, default=True)
    email_on_status_changed = db.Column(db.Boolean, default=True)
    email_on_assignment = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('notification_settings', uselist=False))

    def __repr__(self):
        return f'<NotificationSettings {self.user_id}>'

class TicketActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # created, updated, commented, assigned, etc.
    description = db.Column(db.Text)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    ticket = db.relationship('Ticket', backref='activities')
    user = db.relationship('User', backref='activities')

    def __repr__(self):
        return f'<TicketActivity {self.activity_type}>'

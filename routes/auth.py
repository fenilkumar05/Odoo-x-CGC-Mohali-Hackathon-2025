from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import User, db, NotificationSettings
from forms import LoginForm, RegisterForm, ProfileForm, PasswordChangeForm, NotificationSettingsForm
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Role-based dashboard redirect
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 'agent':
            return redirect(url_for('main.agent_dashboard'))
        else:
            return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact an administrator.', 'error')
                return render_template('auth/login.html', form=form)

            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()

            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('Logged in successfully!', 'success')

            # Role-based redirect after login
            if next_page:
                return redirect(next_page)
            elif user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            elif user.role == 'agent':
                return redirect(url_for('main.agent_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('auth/register.html', form=form)

        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username:
            flash('Username already taken', 'error')
            return render_template('auth/register.html', form=form)

        # Create new user with enhanced fields
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            department=form.department.data,
            role=form.role.data,
            password_hash=generate_password_hash(form.password.data),
            email_notifications=form.email_notifications.data
        )

        db.session.add(user)
        db.session.flush()  # Get user ID

        # Create default notification settings
        notification_settings = NotificationSettings(
            user_id=user.id,
            email_on_ticket_created=form.email_notifications.data,
            email_on_ticket_updated=form.email_notifications.data,
            email_on_comment_added=form.email_notifications.data,
            email_on_status_changed=form.email_notifications.data,
            email_on_assignment=form.email_notifications.data
        )

        db.session.add(notification_settings)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        # Check for duplicate email (excluding current user)
        existing_user = User.query.filter(User.email == form.email.data, User.id != current_user.id).first()
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('auth/profile.html', form=form)

        # Check for duplicate username (excluding current user)
        existing_username = User.query.filter(User.username == form.username.data, User.id != current_user.id).first()
        if existing_username:
            flash('Username already taken', 'error')
            return render_template('auth/profile.html', form=form)

        # Update user profile
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        current_user.department = form.department.data
        current_user.email_notifications = form.email_notifications.data
        current_user.dark_mode = form.dark_mode.data
        current_user.updated_at = datetime.utcnow()

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html', form=form)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect', 'error')
            return render_template('auth/change_password.html', form=form)

        current_user.password_hash = generate_password_hash(form.new_password.data)
        current_user.updated_at = datetime.utcnow()
        db.session.commit()

        flash('Password changed successfully!', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/change_password.html', form=form)

@auth_bp.route('/notification-settings', methods=['GET', 'POST'])
@login_required
def notification_settings():
    settings = current_user.notification_settings
    if not settings:
        settings = NotificationSettings(user_id=current_user.id)
        db.session.add(settings)
        db.session.commit()

    form = NotificationSettingsForm(obj=settings)

    if form.validate_on_submit():
        settings.email_on_ticket_created = form.email_on_ticket_created.data
        settings.email_on_ticket_updated = form.email_on_ticket_updated.data
        settings.email_on_comment_added = form.email_on_comment_added.data
        settings.email_on_status_changed = form.email_on_status_changed.data
        settings.email_on_assignment = form.email_on_assignment.data

        db.session.commit()
        flash('Notification settings updated successfully!', 'success')
        return redirect(url_for('auth.notification_settings'))

    return render_template('auth/notification_settings.html', form=form, settings=settings)

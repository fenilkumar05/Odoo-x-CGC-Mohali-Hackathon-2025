from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    department = StringField('Department', validators=[Optional(), Length(max=100)])
    role = SelectField('Role',
                      choices=[('user', 'End User - Submit and track tickets'),
                              ('agent', 'Support Agent - Manage and resolve tickets'),
                              ('admin', 'Administrator - Full system access')],
                      default='user')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password',
                             validators=[DataRequired(), EqualTo('password')])
    email_notifications = BooleanField('Receive Email Notifications', default=True)
    submit = SubmitField('Register')

class TicketForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()],
                               widget=TextArea(), render_kw={"rows": 6})
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    priority = SelectField('Priority',
                          choices=[('low', 'Low'), ('medium', 'Medium'),
                                 ('high', 'High'), ('urgent', 'Urgent')],
                          default='medium')
    tags = StringField('Tags', validators=[Optional()],
                      render_kw={"placeholder": "Enter tags separated by commas"})
    attachment = FileField('Attachment',
                          validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'txt'],
                                                'Invalid file type!')])
    submit = SubmitField('Create Ticket')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()], 
                           widget=TextArea(), render_kw={"rows": 4})
    is_internal = BooleanField('Internal Note (Agents Only)')
    submit = SubmitField('Add Comment')

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()], 
                               widget=TextArea(), render_kw={"rows": 3})
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Category')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    role = SelectField('Role', 
                      choices=[('user', 'User'), ('agent', 'Agent'), ('admin', 'Admin')],
                      default='user')
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save User')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[Optional()])
    category = SelectField('Category', coerce=int, validators=[Optional()])
    status = SelectField('Status',
                        choices=[('all', 'All'), ('open', 'Open'), ('in_progress', 'In Progress'),
                               ('resolved', 'Resolved'), ('closed', 'Closed')],
                        default='all')
    sort = SelectField('Sort By',
                      choices=[('recent', 'Most Recent'), ('oldest', 'Oldest'),
                             ('most_replied', 'Most Replied'), ('votes', 'Most Voted')],
                      default='recent')
    submit = SubmitField('Search')

class TagForm(FlaskForm):
    name = StringField('Tag Name', validators=[DataRequired(), Length(max=50)])
    color = StringField('Color', validators=[DataRequired()], default='#007bff')
    description = TextAreaField('Description', validators=[Optional()],
                               widget=TextArea(), render_kw={"rows": 2})
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Tag')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    department = StringField('Department', validators=[Optional(), Length(max=100)])
    email_notifications = BooleanField('Receive Email Notifications')
    dark_mode = BooleanField('Dark Mode')
    submit = SubmitField('Update Profile')

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password',
                                   validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class NotificationSettingsForm(FlaskForm):
    email_on_ticket_created = BooleanField('New ticket created')
    email_on_ticket_updated = BooleanField('Ticket updated')
    email_on_comment_added = BooleanField('New comment added')
    email_on_status_changed = BooleanField('Status changed')
    email_on_assignment = BooleanField('Ticket assigned to me')
    submit = SubmitField('Save Settings')

# Video call form removed as requested

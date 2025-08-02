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
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', 
                             validators=[DataRequired(), EqualTo('password')])
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

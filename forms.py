from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
# from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import URLField
from wtforms.validators import DataRequired, Email

class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', render_kw={"class": "mb-4", "placeholder": "Enter your full name"}, validators=[DataRequired()])
    username = StringField('Username', render_kw={"class": "mb-4", "placeholder": "Choose a username"}, validators=[DataRequired()])
    email = StringField('Email', render_kw={"class": "mb-4", "placeholder": "Enter your email"}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', render_kw={"class": "mb-4", "placeholder": "Create a password"}, validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={"class": "btn my-btn col-12"})

class LogInForm(FlaskForm):
    username = StringField('Username', render_kw={"class": "mb-4", "placeholder": "Enter your username"}, validators=[DataRequired()])
    password = PasswordField('Password', render_kw={"class": "mb-4","placeholder": "Enter your password"}, validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={"class": "btn my-btn col-12"})

class SearchForm(FlaskForm):
    query = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={"class": "btn my-btn col-6"})

class EditBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author_name = StringField('Author Name', validators=[DataRequired()])
    cover = URLField('Cover Url', validators=[DataRequired()])
    page_count = IntegerField('Page Count', validators=[])
    language = StringField('Language', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    published_date = StringField('Published Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
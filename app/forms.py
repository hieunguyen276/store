from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, InputRequired
from app.models import Admin


class signUpForm(FlaskForm):
    adminId = StringField('Admin Id', validators=[DataRequired(), Length(min=5, message=('Your id is too short.'))]) #thuộc tính kiểm tra giá trị nhập vào
    fullName = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message=('Your password is too short.'))])
    rePassword = PasswordField('reType Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_AdminId(self, adminId):
        adminId = Admin.query.filter_by(Admin_id=adminId.data).first()
        if adminId is not None:
            raise ValidationError('username has been already used! Please use a different username.')

#kiểm tra admin và email có bị trùng hay k

    def validate_email(self, email):
        email = Admin.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('email has been already used! Please use a different email.')
    
    
class loginForm(FlaskForm):
    adminId = StringField('Admin ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')
    
    
#chống tấn công phổ biến CRSF


class addstore(FlaskForm):
    id = StringField('id')
    store_name = StringField('Name')
    address = StringField('Address')
    image = StringField('Image')
    lat = StringField('Lat')
    lng = StringField('Lng')
    submit = SubmitField('Add')
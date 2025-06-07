from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional

"""
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Ingat Saya')
   """ 
# Bagian ini sengaja dilemahkan dengan menonaktifkan form validators
class LoginForm(FlaskForm):
    email = StringField('Email')  # Tidak ada DataRequired() dan Email()
    password = PasswordField('Password')  # Tidak ada DataRequired()
    remember_me = BooleanField('Ingat Saya')

class RegistrationForm(FlaskForm):
    first_name = StringField('Nama Depan', validators=[DataRequired(), Length(min=2, max=64)])
    last_name = StringField('Nama Belakang', validators=[DataRequired(), Length(min=2, max=64)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Konfirmasi Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    terms = BooleanField('Saya setuju dengan Syarat dan Ketentuan', validators=[DataRequired()])


class CheckoutForm(FlaskForm):
    first_name = StringField('Nama Depan', validators=[DataRequired()])
    last_name = StringField('Nama Belakang', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Alamat', validators=[DataRequired()])
    city = StringField('Kota', validators=[DataRequired()])
    state = StringField('Negara', validators=[DataRequired()])
    zip_code = StringField('Kode ZIP', validators=[DataRequired()])
    phone = StringField('Nomor HP', validators=[Optional()])


class CouponForm(FlaskForm):
    code = StringField('Kode Kupon', validators=[DataRequired()])

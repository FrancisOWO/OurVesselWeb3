from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, IntegerField, FileField, MultipleFileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, NumberRange, Length, Regexp

class RegisterForm(FlaskForm):
    user_id = StringField(
        '账号',
        validators=[
            DataRequired()           
            ],
        render_kw = {
            'class':'form-control',
            'placeholder':'请输入账号',
            'maxlength':'40'
            }
        )
    password1 = PasswordField(
        '密码',
        validators=[
            DataRequired(),
            Length(min=8,max=16,message="密码必须为8-16位")
            ],
        render_kw={
            'class':'form-control',
            'placeholder':'请输入密码',
            'maxlength':'40'
            }
        )
    password2 = PasswordField(
        '重复密码',
        validators=[
            DataRequired(),
            EqualTo('password1', message="两次输入的密码不一致!")
            ],
        render_kw={
            'class':'form-control',
            'placeholder':'请再次输入密码',
            'maxlength':'40'
            }
        )
    submit = SubmitField(
        '注册',
        render_kw={
            'class': 'btn btn-primary'
            }
        )

class LoginForm(FlaskForm):
    user_id = StringField(
        '账号',
        validators=[
            DataRequired()
            ],
        render_kw = {
            'class':'form-control',
            'placeholder':'请输入账号',
            'maxlength':'40'
            }
        )
    password = PasswordField(
        '密码',
        validators=[
            DataRequired()
        ],
        render_kw={
            'class':'form-control',
            'placeholder':'请输入密码',
            'maxlength': '40'
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            'class': 'btn btn-primary'
            }
        )

class ChangePwdForm(FlaskForm):
    oldpwd = PasswordField(
        '原密码',
        validators=[
            DataRequired()
        ],
        render_kw={
            'class':'form-control',
            'placeholder':'请输入原密码',
            'maxlength': '40'
        }
    )
    password1 = PasswordField(
        '新密码',
        validators=[
            DataRequired(),
            Length(min=8,max=16,message="密码必须为8-16位")
            ],
        render_kw={
            'class':'form-control',
            'placeholder':'请输入新密码',
            'maxlength':'40'
            }
        )
    password2 = PasswordField(
        '重复密码',
        validators=[
            DataRequired(),
            EqualTo('password1', message="两次输入的密码不一致!")
            ],
        render_kw={
            'class':'form-control',
            'placeholder':'请再次输入新密码',
            'maxlength':'40'
            }
        )
    submit = SubmitField(
        '修改密码',
        render_kw={
            'class': 'btn btn-primary'
            }
        )
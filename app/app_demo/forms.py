from flask_wtf import FlaskForm
# from flask_wtf.html5 import NumberInput       # 0.13 ==>wtforms
# from wtforms.fields.html5 import NumberInput  # 3.0.x fields.html5==>widgets
from wtforms.widgets import NumberInput
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, IntegerField, FileField, MultipleFileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, NumberRange, Length, Regexp

class DeleteForm(FlaskForm):
    number = IntegerField(
        '删除编号',
        widget=NumberInput(),
        render_kw={
            'class':'form-control',
            'style':"width:70px; height:25px",
            'placeholder':'0'
        }
    )
    submit = SubmitField(
    '确认',
    render_kw={
        'class': 'btn',
        'style': 'border:0px'
        }
    )

class ContentForm(FlaskForm):
    content = StringField(
        '输入',
        render_kw={
            'class':'form-control',
            'style':"width:110px; height:30px"
        }
    )

class TableActForm(FlaskForm):
    add = SubmitField(
        '添加',
        render_kw={
            'class': 'btn',
            'style': 'border:0px'
            }
        )
    delete = SubmitField(
        '删除',
        render_kw={
            'class': 'btn',
            'style': 'border:0px'
            }
        )
    save = SubmitField(
        '保存',
        render_kw={
            'class': 'btn',
            'style': 'border:0px'
            }
        )
    restore = SubmitField(
        '取消',
        render_kw={
            'class': 'btn',
            'style': 'border:0px'
            }
        )
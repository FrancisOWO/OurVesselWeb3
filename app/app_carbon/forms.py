from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, \
    IntegerField, FileField, MultipleFileField, FloatField, DateTimeField, DateTimeLocalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, NumberRange, Length, Regexp


class CarbonTransactionForm(FlaskForm):
    transaction_type = RadioField(
        "交易类型:",
        validators=[
            DataRequired()
        ],
        choices=[('1', "出售"), ('2', "买入"), ('3', "转账")],
    )

    transaction_buyer = StringField(
        "接收方mmsi:",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入接收方船舶mmsi',
            'maxlength': '16'
        }
    )

    transaction_price1 = FloatField(
        "价格(元/吨):",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入交易价格',
        }
    )

    transaction_price2 = FloatField(
        "价格(元/吨):",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入交易价格',
        }
    )

    transaction_number1 = IntegerField(
        "数量(吨):",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入交易数量',
        }
    )

    transaction_number2 = IntegerField(
        "数量(吨):",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入交易数量',
        }
    )

    transaction_number3 = IntegerField(
        "数量(吨):",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入交易数量',
        }
    )

    transaction_time1 = DateTimeLocalField(
        "截止时间",
        render_kw={
            'class': 'form-control',
            'placeholder': '请选择截止时间',
        }
    )

    transaction_time2 = DateTimeLocalField(
        "截止时间",
        render_kw={
            'class': 'form-control',
            'placeholder': '请选择截止时间',
        }
    )

    submit = SubmitField(
        '确认',
        render_kw={
            'class': 'btn btn-primary'
        }
    )


class CarbonTransactionOperateForm(FlaskForm):
    hash_cancel = StringField(
        "撤销交易的hash:",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入撤销交易的hash',
            'maxlength': '64'
        }
    )

    btn_cancel = SubmitField(
        '撤销',
        render_kw={
            'class': 'btn btn-primary'
        }
    )

    hash_buy = StringField(
        "购买交易的hash:",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入购买交易的hash',
            'maxlength': '64'
        }
    )

    btn_buy = SubmitField(
        '购买',
        render_kw={
            'class': 'btn btn-primary'
        }
    )

    hash_sell = StringField(
        "出售交易的hash:",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入出售交易的hash',
            'maxlength': '64'
        }
    )

    btn_sell = SubmitField(
        '出售',
        render_kw={
            'class': 'btn btn-primary'
        }
    )

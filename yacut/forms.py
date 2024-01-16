from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


MIN_LEN_STR: int = 1
LEN_ORIGINAL_LINK: int = 128
LEN_CUSTOM_ID: int = 16


class LinkForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(MIN_LEN_STR, LEN_ORIGINAL_LINK)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(MIN_LEN_STR, LEN_CUSTOM_ID),
            Optional()]
    )
    submit = SubmitField('Создать')

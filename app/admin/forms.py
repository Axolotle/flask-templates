from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    DateTimeField,
    StringField,
    SubmitField,
    TextAreaField,
    FieldList,
    FormField
)
from wtforms.validators import DataRequired, Length

required = DataRequired(message='Required field')


class UploadFileForm(FlaskForm):
    file = FileField('image', validators=[
        FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Upload')


class MediaForm(FlaskForm):
    filename = StringField('path', validators=[required])
    delete = SubmitField('Delete')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[required, Length(min=5)])
    timestamp = DateTimeField('Date', validators=[required], default=datetime.now)
    content = TextAreaField('Content')
    medias = FieldList(FormField(MediaForm))
    submit = SubmitField('Save')

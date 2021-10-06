from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateTimeField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

required = DataRequired(message='Champs Obligatoire')


class PostForm(FlaskForm):
    title = StringField('Titre', validators=[required, Length(min=5)])
    timestamp = DateTimeField('Date', validators=[required], default=datetime.now)
    content = TextAreaField('Contenu')
    submit = SubmitField('Enregistrer', render_kw={'class': 'button'})

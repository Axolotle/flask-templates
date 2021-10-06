from datetime import datetime

from app.extensions import db


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True)
    content = db.Column(db.UnicodeText, nullable=False, default='')

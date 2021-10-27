import os
from werkzeug.utils import secure_filename
from sqlalchemy.ext.mutable import MutableList
from flask import current_app

from app.extensions import db


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True)
    content = db.Column(db.UnicodeText, nullable=False, default="")
    medias = db.Column(MutableList.as_mutable(db.PickleType), default=[])

    def upload_file(self, file):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.instance_path, "uploads", filename)
        if os.path.exists(filepath):
            return ("ok", 200)
        file.save(filepath)
        media = {
            "filename": os.path.join('/uploads', filename),
            "mimetype": file.mimetype
        }
        self.medias.append(media)
        return media

    def delete_file(self, filename):
        filepath = os.path.join(current_app.instance_path, filename.lstrip('/'))
        for i, media in enumerate(self.medias):
            if filename == media["filename"]:
                self.medias.pop(i)
                os.remove(filepath)
                return True
        return False

    def delete_medias(self):
        for i, media in enumerate(self.medias):
            path = os.path.join(current_app.instance_path,
                                media["filename"].lstrip('/'))
            if os.path.exists(path):
                os.remove(path)
                return True

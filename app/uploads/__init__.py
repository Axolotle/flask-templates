import os
from flask import Blueprint, current_app, send_from_directory

# Faking another static folder for development but will be served by nginx on prod
bp = Blueprint('uploads', __name__, static_url_path='',
               static_folder=os.path.join(current_app.instance_path, 'uploads'))

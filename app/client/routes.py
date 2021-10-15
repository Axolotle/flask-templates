from flask import Blueprint, render_template

from app.admin.models import Post
from app.admin.routes import get_post

bp = Blueprint('client', __name__)


@bp.get('/')
@bp.get('/posts')
def posts():
    posts = Post.query.all()
    return render_template('client/posts.html', posts=posts)


@bp.get('/posts/<int:id>')
def post(id):
    post = get_post(id)
    return render_template('client/post.html', post=post)

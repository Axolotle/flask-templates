from flask import Blueprint, render_template

from app.admin.models import Post
from app.admin.routes import get_post

bp = Blueprint('base', __name__)


@bp.get('/')
@bp.get('/posts')
def posts():
    posts = Post.query.all()
    return render_template('base/posts.html', posts=posts)


@bp.get('/posts/<int:id>')
def post(id):
    post = get_post(id)
    return render_template('base/post.html', post=post)

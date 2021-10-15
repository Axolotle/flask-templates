from flask import Blueprint, render_template, redirect, url_for, abort, flash

from app.extensions import db
from app.admin.forms import PostForm
from app.admin.models import Post

bp = Blueprint('admin', __name__)


def get_post(id):
    post = Post.query.get(id)
    if post is None:
        abort(404, 'The post {} doesn\'t exists.'.format(id))
    return post


@bp.get('/')
@bp.get('/posts')
def posts():
    posts = Post.query.all()
    return render_template('admin/posts.html', posts=posts)


@bp.route('/posts/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post()
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('admin.posts'))

    return render_template('admin/post.html', title='New Post', form=form)


@bp.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = get_post(id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('admin.posts'))

    return render_template(
        'admin/post.html',
        title='Post edition',
        form=form,
    )


@bp.post('/posts/<int:id>/delete')
def delete_post(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('admin.posts'))

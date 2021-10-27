from flask import Blueprint, request, render_template, redirect, url_for, abort, flash

from app.extensions import db
from app.admin.forms import PostForm, UploadFileForm
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
        return redirect(url_for('admin.update_post', id=post.id))

    return render_template('admin/post.html', title='New Post', form=form)


@bp.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = get_post(id)
    form = PostForm(obj=post)
    upload = UploadFileForm()

    if form.validate_on_submit():
        del form.medias
        form.populate_obj(post)
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('admin.update_post', id=post.id))

    return render_template(
        'admin/post.html',
        title='Post edition',
        form=form,
        upload=upload,
        id=post.id
    )


@bp.post('/posts/<int:id>/delete')
def delete_post(id):
    post = get_post(id)
    post.delete_medias()
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('admin.posts'))


@bp.post('/posts/<int:id>/add_file')
def upload_file(id):
    form = UploadFileForm()
    post = get_post(id)
    if form.validate_on_submit():
        file = form.file.data
        if file:
            print("file:", file)
            post.upload_file(file)
            db.session.commit()
    return redirect(url_for('admin.update_post', id=post.id))


@bp.post('/posts/<int:id>/delete_file')
def delete_file(id):
    filename = request.form["filename"]
    post = get_post(id)
    post.delete_file(filename)
    db.session.commit()
    return redirect(url_for('admin.update_post', id=post.id))

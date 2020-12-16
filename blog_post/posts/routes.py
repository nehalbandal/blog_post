from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from blog_post import db
from blog_post.models import Post, Comment, PostLikes, Category
from blog_post.posts.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template('create_update_post.html', title="New Post", form=form, legend="New Post")


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_idx=post_id)
    likes = PostLikes.query.filter_by(liked_post_id=post_id).count()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment_body=form.comment.data, commented_user=current_user, commented_post=post)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added", "success")
        return redirect(url_for("posts.post", post_id=post_id))
    return render_template("post.html", title=post.title, post=post, form=form, comments=comments, likes=likes)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    selected_cats = []
    for cat in post.categories:
        selected_cats.append(cat.name)
    form = PostForm(category=selected_cats)
    if form.validate_on_submit():
        for cat in form.category.data:
            category = Category.query.filter_by(name=cat).first()
            if post.categories.count(category) == 0:  # if post doesn't have that category associated already
                category.posts.append(post)
            else:  # remove the selected category of the post if it is already available.
                category.posts.remove(post)
            db.session.add(category)
            db.session.commit()
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_update_post.html', title="Update Post", form=form, legend="Update Post")


@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))


@posts.route("/post/<int:post_id>/liked")
@login_required
def liked_post(post_id):
    post = Post.query.get_or_404(post_id)
    already_liked = PostLikes.query.filter_by(user=current_user, post=post).count() > 0
    if not already_liked:
        like = PostLikes(post=post, user=current_user)
        db.session.add(like)
        db.session.commit()
    return redirect(url_for("posts.post", post_id=post_id))

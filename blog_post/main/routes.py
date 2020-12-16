from flask import render_template, request, Blueprint, current_app, flash, g, url_for, redirect
from flask_login import current_user, login_required
from blog_post.models import Post, Category, PostLikes
from blog_post.main.forms import SearchForm
from sqlalchemy import func

main = Blueprint('main', __name__)


@main.before_app_request
def before_request():
    g.search_form = SearchForm()


@main.route("/", defaults={'cat_name': None})
@main.route("/home", defaults={'cat_name': None}, methods=['GET', 'POST'])
@main.route("/home/<string:cat_name>/", methods=['GET', 'POST'])
def home(cat_name):
    page = request.args.get('page', 1, type=int)
    if cat_name and not current_user.is_authenticated:
        flash("Please Login to see more results.", "info")
    elif cat_name:
        posts = Post.query.filter(Post.categories.any(Category.name == cat_name)).order_by(Post.date_posted.desc()). \
            paginate(page=page, per_page=int(current_app.config["PER_PAGE"]))
        return render_template('home.html', title=cat_name, posts=posts, cat=cat_name)

    if not current_user.is_authenticated:
        posts = Post.query.join(PostLikes).group_by(Post.id).order_by(func.count().desc()). \
            paginate(page=1, per_page=int(current_app.config["PER_PAGE"]))
    else:
        posts = current_user.followed_posts().order_by(Post.date_posted.desc()). \
            paginate(page=page, per_page=int(current_app.config["PER_PAGE"]))

    return render_template('home.html', title="Home", posts=posts, route_name='home')


@main.route("/explore", methods=['GET', 'POST'])
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()). \
        paginate(page=page, per_page=int(current_app.config["PER_PAGE"]))
    return render_template('home.html', title="Explore", posts=posts, route_name='explore')


@main.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)
    searched_posts, total = Post.search(g.search_form.q.data, page, int(current_app.config["PER_PAGE"]))
    if total == 0:
        return redirect(url_for('main.home'))
    if page == 1:
        flash("There are total {} results found...".format(total), "success")
    return render_template('home.html', title="Search",
                           posts=searched_posts.paginate(page=1, per_page=int(current_app.config["PER_PAGE"])),
                           route_name='search', q=g.search_form.q.data)


@main.route("/about")
def about():
    return render_template('about.html', title="About")

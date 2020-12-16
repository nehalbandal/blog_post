from blog_post import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from blog_post.search import add_to_index, remove_from_index, query_index


@login_manager.user_loader
def load_user(user_id):
    """
    Reloading user from user_id store in session. This is nothing but get user by id.
    """
    return User.query.get(int(user_id))


class SearchableMixin:
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0

        return cls.query.filter(cls.id.in_(ids)).order_by(cls.date_posted.desc()), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True, cascade="all, delete, delete-orphan")
    comment = db.relationship('Comment', backref='commented_user', lazy=True)
    liked = db.relationship('PostLikes', backref='user', lazy=True)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.date_posted.desc())

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return "User('{}','{}','{}')".format(self.username, self.email, self.image_file)


categories = db.Table('categories',
                      db.Column('cat_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
                      )


class Post(SearchableMixin, db.Model):
    __tablename__ = "post"
    __searchable__ = ['title', 'content']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.relationship('Comment', backref='commented_post', lazy=True)
    likes = db.relationship('PostLikes', backref="post", lazy=True)
    categories = db.relationship('Category', secondary=categories, backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return "Post('{}','{}')".format(self.title, self.date_posted)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def add_or_remove(self, cat, post):
        post_cat = self.query.filter_by(name=cat).first()
        if post.categories.count(post_cat) == 0:
            # if post doesn't have that category associated already
            post_cat.posts.append(post)
        else:
            # remove the selected category of the post if it is already available.
            post_cat.posts.remove(post)
        return post_cat


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    user_idx = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_idx = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_body = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Comment( {}, {}, {}, {})".format(self.user_idx, self.post_idx, self.comment_date, self.comment_body)


class PostLikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    liked_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return "PostLikes( {}, {})".format(self.liked_user_id, self.liked_post_id)

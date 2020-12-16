from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from blog_post import CATEGORIES


class PostForm(FlaskForm):
    title = StringField(label="Title", validators=[DataRequired()])
    content = TextAreaField(label="Content", validators=[DataRequired()])
    category = SelectMultipleField(label="Category", choices=CATEGORIES)
    submit = SubmitField(label="Post")


class CommentForm(FlaskForm):
    comment = TextAreaField(validators=[DataRequired()], render_kw={"placeholder": "Share your thoughts"})
    submit = SubmitField(label="Submit")

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:///database/site.db"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_ADDRESS')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    PER_PAGE = "3"
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    UPLOAD_FOLDER = "E:\GIT\StudyMaterials\Python\Flask\Blog_Post\\blog_post\static\profile_pics"

import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        HOST = os.environ['DB_HOST'],
        DATABASE = os.environ['DATABASE'],
        USER = os.environ['DB_USER'],
        PASSWORD = os.environ['DB_PASSWORD'],
        TEMP = os.path.join(app.root_path, 'temp'),
        AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY'],
        AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY'],
        AWS_S3_LINK = os.environ['AWS_S3_LINK']
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # call db package with our defined methods to init, close our db and add special command init-db
    from . import db
    db.init_app(app)


    # blueprint registration
    from . import auth
    app.register_blueprint(auth.bp)

    # blueprint blog with endpoint index
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    # blueprint likes
    from . import likes
    app.register_blueprint(likes.bp)

    # blueprint comment
    from . import comment
    app.register_blueprint(comment.bp)

    # upload image
    from . import upload_file
    app.register_blueprint(upload_file.bp)

    # search on article
    from . import search
    app.register_blueprint(search.bp)
   

    return app

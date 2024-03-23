import os

from flask import Flask

def create_app(test_config=None):
    #create and config the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )

    if test_config is None :
        #load the instance config
        app.config.from_pyfile('config.py', silent=True)
    else :
        #load the test config if passed
        app.config.from_mapping(test_config)

    #ensure the instance folder exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #simple route
    @app.route('/')
    def hello():
        return "hello World!"
    #db
    from . import db
    db.init_app(app)

    #auth
    from . import auth
    app.register_blueprint(auth.bp)
    
    #blog
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app


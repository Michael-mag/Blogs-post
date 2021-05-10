import os
from . import db
from flask import Flask
from . import auth
from . import blog
#create the application factory function
def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__,instance_relative_config=True)

    #setup some app default configurations
    app.config.from_mapping(
        SECRET_KEY = "dev", #just for now, for dev purposes only
        DATABASE = os.path.join(app.instance_path, "flaskr.sqlite")
    )

    #load the instance config if non-existent when not testing
    if test_config is None:
        app.config.from_pyfile("config.py",silent=True)
    else:
        #load the instance config if passed in
        app.config.from_mapping(test_config)

    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/welcome")
    def welcome():
        return "Hi...Welcome!"

    #initialize the database
    db.init_app(app)

    #register the bluebrint
    app.register_blueprint(auth.bp)

    #register the blog blueprint
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app

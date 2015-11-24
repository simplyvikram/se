
import os
from flask import Flask
from flask_jsglue import JSGlue
from flask.ext.script import Manager

from config import ProductionConfig, DevelopmentConfig
import database

def _create_app(app_name):
    app = Flask(app_name, template_folder='templates')
    jsglue = JSGlue()
    jsglue.init_app(app)
    if 'APP_ENV' in os.environ and os.environ['APP_ENV'] == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    database.create_db(app.config['DATABASE_URI'])

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        database.db_session.remove()

    return app


def _register_views(app):
    import views
    # app.json_encoder = views.CustomJSONEncoder
    app.register_blueprint(views.blueprint)


app = _create_app(app_name='expense_reporter')
manager = Manager(app)


@manager.command
def run_server():
    _register_views(app)
    app.run(host='127.0.0.1', port=5000, debug=app.config['DEBUG'])


# @manager.command
# def create_db():
#     database.create_db(app.config['DATABASE_URI'])


# @manager.command
# def drop_db():
#     database.drop_db(app.config['DATABASE_URI'])


if __name__ == '__main__':
    manager.run()

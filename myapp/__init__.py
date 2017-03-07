import flask

import myapp.views.auth
import myapp.views.report


def create_app():
    app = flask.Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    app.register_blueprint(myapp.views.auth.auth_view, url_prefix="/auth")
    app.register_blueprint(myapp.views.report.report_view, url_prefix="/report")

    return app



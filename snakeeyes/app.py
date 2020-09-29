import logging

from logging.handlers import SMTPHandler

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, render_template
from celery import Celery

from snakeeyes.blueprints.page import page
from snakeeyes.blueprints.contact import contact
from snakeeyes.extensions import debug_toolbar, mail, csrf

CELERY_TASK_LIST = [
    'snakeeyes.blueprints.contact.tasks',
]


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(settings_override=None):
    """
    Create a Flask app using the app factory pattern

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    app.logger.setLevel(app.config['LOG_LEVEL'])

    middleware(app)
    error_templates(app)
    exception_handler(app)

    app.register_blueprint(page)
    app.register_blueprint(contact)
    extensions(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    return None


def middleware(app):
    """
    Register 0 or more middleware (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # Swap request.remote_addr with the real IP address even if behind a proxy.
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return None


def error_templates(app):
    """
    Register 0 or more custom error pages (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """

    def render_status(status):
        """
         Render a custom template for a specific status.
           Source: http://stackoverflow.com/a/30108946

         :param status: Status as a written name
         :type status: str
         :return: None
         """
        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        code = getattr(status, 'code', 500)
        return render_template('errors/{0}.html'.format(code)), code

    for error in [404, 500]:
        app.errorhandler(error)(render_status)

    return None


def exception_handler(app):
    """
    Register 0 or more exception handlers (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # <rms/>
    secure = None

    mail_handler = SMTPHandler(mailhost=(app.config.get('MAIL_SERVER'), app.config.get('MAIL_PORT')),
                               fromaddr=app.config.get('MAIL_DEFAULT_SENDER'),
                               toaddrs=[app.config.get('MAIL_DEFAULT_SENDER')],
                               subject='5xx err',
                               credentials=(app.config.get('MAIL_USERNAME'), app.config.get('MAIL_PASSWORD')),
                               secure=secure)

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter("""
    Time:               %(asctime)s
    Message type:       %(levelname)s


    Message:

    %(message)s
    """))
    app.logger.addHandler(mail_handler)

    return None

# https://www.programcreek.com/python/example/5045/logging.handlers.SMTPHandler
# mail_handler = SMTPHandler(
#             mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
#             fromaddr=cls.MAIL_SENDER,
#             toaddrs=[cls.ADMINMAIL],
#             subject=cls.MAIL_SUBJECT_PREFIX + ' Application Error',
#             credentials=credentials,
#             secure=secure)

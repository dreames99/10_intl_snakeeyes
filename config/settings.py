DEBUG = True
LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

SERVER_NAME = 'localhost:8000'
SECRET_KEY = 'insecurekeyfordev'

# Flask-Mail
MAIL_DEFAULT_SENDER = 'info@rmsfinance.com'
# MAIL_SERVER = 'mail.webfaction.com'
MAIL_SERVER = 'smtp.webfaction.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
# MAIL_USERNAME = 'dreames@rmsfinance.com'
MAIL_USERNAME = 'dreames'
MAIL_PASSWORD = 'Ny1958Giants'

# Celery
CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5

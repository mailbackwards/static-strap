from werkzeug import SharedDataMiddleware
from flask import Flask

import config

app = Flask(__name__, static_path=config.STATIC_URL)
app.config.from_object(config)

# This gets us the proper url for the so-called "static" folder.
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
  '/': app.config.get('STATIC_FULL_URL')})

from app import views

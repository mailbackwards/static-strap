import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True  # we never run the app in a production environment :)

STATIC_URL = '/static'
STATIC_FULL_URL = os.path.join(BASE_DIR, 'app/static')
BOILER_FULL_URL = os.path.join(STATIC_FULL_URL, 'boiler')
BOILER_FILES = ['/robots.txt', '/favicon.ico', '/sitemap.xml']

FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FREEZER_DESTINATION =  os.path.join(BASE_DIR, 'app/freezer')
FREEZER_REMOVE_EXTRA_FILES = True

# Add these if you want to use the S3 deploy functionality

S3_BUCKET_NAME = ''
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
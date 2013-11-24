from flask import render_template, request, send_from_directory
from flask.views import View
from flask_flatpages import FlatPages

from app import app

pages = FlatPages(app)

def render_page(pagename, **kwargs):
	current_page = pages.get_or_404(pagename)
	title = current_page.meta.get('title')
	return render_template('page.html', 
		pages=pages, 
		current_page=current_page, 
		body=current_page.html, 
		title=title, 
		**kwargs)

@app.route('/')
def index():
	return render_page('index')

@app.route('/<path:path>/')
def page(path):
	return render_page(path)

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
	return send_from_directory(app.config.get('BOILER_FULL_URL'), request.path[1:])

@app.route('/error.html')
def generate_404_page():
	return 'Whoops that was a 404, sorry'
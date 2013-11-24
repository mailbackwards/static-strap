from flask.ext.script import Manager
from flask_frozen import Freezer
from app import app

manager = Manager(app)

@manager.command
def freeze(*args):
	import shutil
	from flask import url_for

	freezer = Freezer(app)
	freezer.freeze()
	# Copy the boilerplate files (favicon, robots.txt) to the freezer
	for filename in app.config.get('BOILER_FILES'):
		shutil.copy(app.config.get('BOILER_FULL_URL') + filename, app.config.get('FREEZER_DESTINATION'))

@manager.command
def deploy(*args, **kwargs):
	from modules.deployutils import BucketConn
	initial_kwargs = {
		'access_secret': app.config.get('AWS_SECRET_ACCESS_KEY'), 
		'access_key': app.config.get('AWS_ACCESS_KEY_ID'), 
		'bucket_name': app.config.get('S3_BUCKET_NAME'), 
		'working_directory': app.config.get('FREEZER_DESTINATION'), 
		'interactive': True
	}
	bucket = BucketConn(**initial_kwargs)
	bucket.rebuild_from_working_directory()

@manager.command
def frozenserver():
	freezer = Freezer(app)
	freezer.run(debug=True)
	
if __name__ == "__main__":
    manager.run()
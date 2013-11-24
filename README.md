static-strap
======================

static-strap is a [Flask](http://flask.pocoo.org/) app skeleton that is optimized for rapid prototyping and deploying of static websites.

### About

This app can be thought of as divided into two parts:

- A static website generator inspired by [this post](https://nicolas.perriault.net/code/2012/dead-easy-yet-powerful-static-website-generator-with-flask/) and the magic of [Frozen-Flask](https://github.com/SimonSapin/Frozen-Flask)/[Flask-FlatPages](https://github.com/SimonSapin/Flask-FlatPages)
- An optional hook into an Amazon S3 account for easy command-line "deployment" of a static website (built on [boto](https://github.com/boto/boto)).

This allows for all the perks of a modern development framework (routes, templates, [bootstrap](https://github.com/twbs/bootstrap)), and even a [pseudo-database](http://pythonhosted.org/Flask-FlatPages/). Good for personal webpages, hackathons, frontend playgrounds, etc.

### Starting up

This is assuming [virtualenv](https://pypi.python.org/pypi/virtualenv).

	$ git clone https://github.com/mailbackwards/static-strap.git
	$ cd static-strap
	$ virtualenv .
	$ . bin/activate
	$ pip install -r requirements.txt
	$ cp config.sample.py config.py
	$ python manage.py runserver

This starts a local development server at [localhost:5000](http://127.0.0.1:5000). There's already a pair of sample bootstrapped pages to get started. Then run

	$ python manage.py freeze

This generates a static site from the existing app, which puts a "frozen" version of it into the `./app/freezer` directory; this directory can now be uploaded as a valid site to any server.

### Deploying

To use the S3 deploy functionality, copy `config.py` from the root folder and fill in these variables:

	S3_BUCKET_NAME = ''         # a new or existing (empty) bucket, usually your site's name
	AWS_ACCESS_KEY_ID = ''      # your access key from Amazon
	AWS_SECRET_ACCESS_KEY = ''  # your secret key from Amazon

Then close the file and run:

	$ python manage.py deploy

to upload the folder containing the static site (whatever is in `./app/freezer`) to the configured Amazon S3 bucket.

> N.B.: This command deletes all existing files from the bucket before it deploys, so don't store any non-site-related files there.

### Further reading

static-strap is built on:

- [Flask](http://flask.pocoo.org/docs/)
- [Frozen-Flask](http://pythonhosted.org/Frozen-Flask/)
- [Flask-FlatPages](http://pythonhosted.org/Flask-FlatPages/)
- [flask-script](http://flask-script.readthedocs.org/en/latest/)
- [boto S3](http://boto.readthedocs.org/en/latest/s3_tut.html)
- [helpful blog post](https://nicolas.perriault.net/code/2012/dead-easy-yet-powerful-static-website-generator-with-flask/)

I highly recommend Flask, it's a small (in a good way), powerful framework that seemed a perfect fit for making a small but powerful webpage. It's also written in the greatest language in the world.

### Want list

- More seamless testing framework for the static page (right now it's wonky as described [here](http://pythonhosted.org/Frozen-Flask/#testing-url-generators))
- Git integration on deploy function
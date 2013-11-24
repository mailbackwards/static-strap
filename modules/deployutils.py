import os
import boto

class BucketConn(object):
	"""
	Connects to the S3 bucket and ties a local directory to it for quick recursive uploading/deleting.

	Used as a "deploy" engine for static files. Requires boto.
	"""

	def __init__(self, 
			working_directory=None,
			bucket_name=None, 
			access_key=None, 
			access_secret=None, 
			interactive=False
			):
		self.working_directory = working_directory or os.getcwd()
		self.bucket_name = bucket_name
		self.access_key = access_key
		self.access_secret = access_secret
		self.interactive = interactive
		
		self.conn = boto.connect_s3(self.access_key, self.access_secret)
		self.bucket = self._get_or_create_bucket(self.conn)

	def _get_or_create_bucket(self, conn):
		""" 
		Connect to the bucket specified in self.bucket_name. If it's not found, create it and set as a website. 
		"""
		bucket = conn.lookup(self.bucket_name)
		if bucket is None:
			print 'No exiting bucket found with the name "%s". Creating it.' % self.bucket_name
			bucket = conn.create_bucket(self.bucket_name, policy='public-read')
			bucket.configure_website('index.html', 'error.html')
			print 'New bucket created and configured as a website. Name is "%s", endpoint is "%s"' % \
				  (self.bucket_name, bucket.get_website_endpoint())
		else:
			print 'Found existing bucket with the name "%s" at endpoint "%s". Using this one.' % \
				  (self.bucket_name, bucket.get_website_endpoint())
		return bucket

	def _get_filenames_recursive(self, directory='current'):
		""" 
		Walk through a directory and return a list of all filenames with full paths. 
		"""
		if directory == 'current':
			directory = self.working_directory
		all_files = []
		for root, subFolders, files in os.walk(directory):
			for filename in files:
				full_filepath = os.path.join(root, filename)
				all_files.append(full_filepath)
		return all_files

	def upload_file(self, filename, policy='public-read'):
		"""
		Upload a single file (full path) to the bucket.
		"""
		aws_relative_path = filename[len(self.working_directory):]
		key = self.bucket.new_key(aws_relative_path)
		key.set_contents_from_filename(filename, policy=policy)

	def upload_working_directory(self, policy='public-read'):
		"""
		Takes a local directory and uploads all its files to the bucket.
		"""
		filenames_to_upload = self._get_filenames_recursive(self.working_directory)
		print 'Uploading %d files...' % (len(filenames_to_upload))
		for index, filename in enumerate(filenames_to_upload):
			print '%s -- %d' % (filename, index+1)
			self.upload_file(filename, policy=policy)

	def delete_all_files(self):
		""" 
		Deletes ALL files from the bucket. Prompts first if self.interactive is True. 
		"""
		all_keys = self.bucket.get_all_keys()
		if not all_keys:
			print 'No keys found in the bucket.'
			return
		if self.interactive:
			confirm = raw_input('Do you want to delete %d existing files? (y/n): ' % len(all_keys))
			if confirm.lower() != 'y':
				return
		self.bucket.delete_keys(all_keys)
		return

	def rebuild_from_working_directory(self):
		""" 
		Deletes all files from the S3 server, then uploads the local directory. 
		"""
		self.delete_all_files()
		self.upload_working_directory()
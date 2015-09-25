from django.core.management.base import BaseCommand, CommandError
from experiments.models import Experiment
from django.core import exceptions
from django.conf import settings
from django.core import management
import shutil
import sys
import os

class NotRunningInTTYException(Exception):
    pass

class Command(BaseCommand):
	help = 'Adds a new Experment App'

	def execute(self, *args, **options):
		self.stdin = options.get('stdin', sys.stdin)  # Used for testing
		return super(Command, self).execute(*args, **options)

	def handle(self, *args, **options):
		try:
			user_data = {}
			if hasattr(self.stdin, 'isatty') and not self.stdin.isatty():
				raise NotRunningInTTYException("Not running in a TTY")

			for field_name in Experiment.REQUIRED_FIELDS:
				field = Experiment._meta.get_field(field_name)
				user_data[field_name] = None
				while user_data[field_name] is None:
					message = field_name.upper() + ': '
					user_data[field_name] = self.get_input_data(field, message)

		except KeyboardInterrupt:
			self.stderr.write("\nOperation cancelled.")
			sys.exit(1)

		except NotRunningInTTYException:
			self.stdout.write(
			"Experiment creation skipped due to not running in a TTY. "
			"You can run `manage.py create_exp` in your project "
			"to create one manually."
			)

		app_name = user_data['name']
		if app_name not in settings.INSTALLED_APPS:
			try:
				src = 'exp0'
				dest = app_name
				shutil.copytree(src, dest)
			except Exception as e:
				self.stderr.write("Directory not copied. Error: %s" % str(e))
			try:
				template_dir = app_name + '/templates/' + app_name
				os.makedirs(template_dir)
				with open("vlab/settings.py", "a") as myFile:
					myFile.write("INSTALLED_APPS += ('%s',)\n" % app_name)
					myFile.close()
				experiment = Experiment(**user_data)
				experiment.save()
			except Exception as e:
				self.stderr.write("Directory not copied. Error 1: %s" % str(e))
				shutil.rmtree(app_name)	
			#management.call_command('makemigrations', app_name)
			#management.call_command('migrate')

	def get_input_data(self, field, message, default=None):
		raw_value = raw_input(message)
		if default and raw_value == '':
			raw_value = default
		try:
			val = field.clean(raw_value, None)
		except exceptions.ValidationError as e:
			self.stderr.write("Error: %s" % '; '.join(e.messages))
			val = None	
		return val

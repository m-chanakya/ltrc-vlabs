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
	help = 'Remove an existing Experiment'

	def execute(self, *args, **options):
		self.stdin = options.get('stdin', sys.stdin)  # Used for testing
		return super(Command, self).execute(*args, **options)

	def handle(self, *args, **options):
		try:
			user_data = {}
			if hasattr(self.stdin, 'isatty') and not self.stdin.isatty():
				raise NotRunningInTTYException("Not running in a TTY")

			user_data['experiment'] = None
			while user_data['experiment'] is None:
				message = 'EXPERIMENT NAME: '
				user_data['experiment'] = raw_input(message)
				try:
					user_data['experiment'] = Experiment.objects.get(name = user_data['experiment'])
				except:
					self.stderr.write("Invalid experiment name")
					user_data['experiment'] = None

		except KeyboardInterrupt:
			self.stderr.write("\nOperation cancelled.")
			sys.exit(1)

		except NotRunningInTTYException:
			self.stdout.write(
			"Experiment removal skipped due to not running in a TTY. "
			"You can run `manage.py delete_exp` in your project "
			"to create one manually."
			)

		app_name = user_data['experiment'].name
		user_data['experiment'].delete()
		try:
			shutil.rmtree(app_name)
		except Exception as e:
			self.stderr.write("Directory not deleted. Error: %s" % str(e))
			pass
		if app_name in settings.INSTALLED_APPS:
			try:
				app_line = "INSTALLED_APPS += ('%s',)\n" % app_name
				f = open("vlab/settings.py", "r+")
				data = f.readlines()
				f.seek(0)
				for line in data:
					if line != app_line:
						f.write(line)
				f.truncate()
				f.close()
			except Exception as e:
				self.stderr.write("Settings couldn't be updated. Error 1: %s" % str(e))

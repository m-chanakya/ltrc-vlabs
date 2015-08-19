from django.core.management.base import BaseCommand, CommandError
from experiments.models import Experiment, ExperimentStage
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

			user_data['experiment'] = None
			while user_data['experiment'] is None:
				message = 'EXPERIMENT NAME: '
				user_data['experiment'] = raw_input(message)
				try:
					user_data['experiment'] = Experiment.objects.get(name = user_data['experiment'])
				except:
					self.stderr.write("Invalid experiment name")
					user_data['experiment'] = None

			for field_name in ExperimentStage.REQUIRED_FIELDS:
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

		experiment = user_data['experiment']
		stage_name = user_data['name']
		template = experiment.name + '/templates/' + experiment.name + '/' + stage_name + '.html'
		try:
			open(template, 'a').close()
			experiment_stage = ExperimentStage(**user_data)
			experiment_stage.save()
		except Exception as e:
			self.stderr.write("Error: %s" % str(e))
			os.remove(template)

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

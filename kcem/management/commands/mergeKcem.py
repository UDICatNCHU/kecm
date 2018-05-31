from django.core.management.base import BaseCommand, CommandError
from udic_nlp_API.settings_database import uri
from kcem.apps import KCEM

class Command(BaseCommand):
	help = 'merge duplicate key of kcem'
		
	def add_arguments(self, parser):
		# Positional arguments
		parser.add_argument('--lang', type=str)

	def handle(self, *args, **options):
		k = KCEM(options['lang'], uri)
		for index, key in pickle.load(open('duplicate_key_{}.pkl'.format(options['lang']), 'rb')):
			if index % 100:
				logging.info('merge {} duplicate key {}'.format(index, key))
				k.get(key)
		self.stdout.write(self.style.SUCCESS('merge KCEM success!!!'))
from login_app.models import PublishingTime
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from datetime import  timedelta


class Command(BaseCommand):
	args=''
	help ='Check the scedule post, and update necessary post'

	def handle(self, *args, **options):
		for pt in PublishingTime.objects.filter(status=False):
			if pt.datetime < (timezone.now()):
				pt.publish()

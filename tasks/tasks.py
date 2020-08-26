from __future__ import absolute_import, unicode_literals
from .celery import app
from planning.models import Plan


@app.task
def send_mails():
	emails = tuple()
	for user in User.objects.all():
		num_plans = Plan.objects.filter(consolidated_on=None, incharge=user).count()
		if num_plans:
			email = ("PROCUREMENT PLAN ACTION",
				f'''Hello {user}''') 


def send_sms():
    print("sending sms...")

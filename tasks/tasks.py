from PMS.celery import app
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django.conf import settings
from django.core.mail import send_mail
from django import template

from PMS import sms
from models import User
from utils import get_user_actions

@app.task
def send_auth_mail(username):
    user = User.objects.get(username=username)
    if user.token:
        password_set_email_template = template.loader.get_template(f'emails/password-set-email.html')
        send_mail(
            'SET PASSWORD',
            "",
            'samuelitwaru@gmail.com',
            ['samuelitwaru@yahoo.com'],
            fail_silently=False,
            html_message = password_set_email_template.render({"token": user.token.token})
        )


@periodic_task(run_every=(crontab(day_of_week='1')), name="send_emails", ignore_result=True)
def send_emails():
    action_notifications_template = template.loader.get_template(f'emails/action-notifications.html')
    for user in User.objects.all():
        actions = get_user_actions(user)
        plan_actions = actions.get("plan_actions")
        requisition_actions = actions.get("requisition_actions")
        if plan_actions.count() or requisition_actions.count():
            send_mail(
                'SET PASSWORD',
                "",
                'samuelitwaru@gmail.com',
                [user.username],
                fail_silently=False,
                html_message = action_notifications_template.render({
                        "plan_actions":plan_actions, "requisition_actions":requisition_actions
                    })
            )


@periodic_task(run_every=(crontab(day_of_week='1')), name="send_SMSs", ignore_result=True)
def send_SMSs():
    sms_action_notification_template = template.loader.get_template(f'emails/sms-action-notification.html')
    for user in User.objects.all():
        actions = get_user_actions(user)
        plan_actions = actions.get("plan_actions").count()
        requisition_actions = actions.get("requisition_actions").count()
        if plan_actions or requisition_actions:
            sms.send(
                sms_action_notification_template.render({"plan_actions":plan_actions, "requisition_actions":requisition_actions}), 
                [user.profile.telephone]
            )




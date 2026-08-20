from celery import shared_task
from time import sleep


@shared_task
def send_email_notification(user_id):
    sleep(10)
    print(f"Sending email notification to {user_id}")

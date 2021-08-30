from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from config.celery import app


@app.task(name="tasks.send_email_stats")
def send_email_stats(data: dict, email: str):
    content = render_to_string("tasks/email.html", data)

    email = EmailMessage(
        subject="Статистика по задачам",
        body=content,
        to=[email],
    )
    email.content_subtype = "html"
    email.send()

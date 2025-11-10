import json

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from Application.tasks import libro_del_dia

schedule, _ = CrontabSchedule.objects.get_or_create(
    minute="*/5",
    hour="*",
    day_of_week="*",
    day_of_month="*",
    month_of_year="*",
)

PeriodicTask.objects.update_or_create(
    crontab=schedule,
    name="Daily task - Book of the minute",
    task="Application.tasks.libro_del_dia",
)

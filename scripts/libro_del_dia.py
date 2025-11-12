from django_celery_beat.models import CrontabSchedule, PeriodicTask

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

from django_celery_beat.models import PeriodicTask, CrontabSchedule
from Application.tasks import libro_del_dia
import json

schedule, _ = CrontabSchedule.objects.get_or_create(
    minute='*/5',
    hour='*',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)

PeriodicTask.objects.update_or_create(
    crontab=schedule,
    name='Tarea diaria - Libro del minuto',
    task='Application.tasks.libro_del_dia',
)

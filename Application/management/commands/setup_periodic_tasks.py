from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule

class Command(BaseCommand):
    help = 'Configura la tarea periódica libro_del_dia'

    def handle(self, *args, **kwargs):
        from Application.tasks import libro_del_dia

        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='*/5',
            hour='*',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )

        # Como se actualiza o crea, no se crea siempre una nueva tarea
        PeriodicTask.objects.update_or_create(
            name='Tarea diaria - Libro del minuto',
            defaults={
                'crontab': schedule,
                'task': 'Application.tasks.libro_del_dia',
                'enabled': True,
            }
        )

        self.stdout.write(self.style.SUCCESS('✅ Tarea periódica configurada.'))

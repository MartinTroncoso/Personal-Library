# mypy: ignore-errors

from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Configures the periodic task libro_del_dia"

    def handle(self, *args, **kwargs) -> None:
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute="*/1",
            hour="*",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        )

        # Since it updates or creates, a new task is not always created
        PeriodicTask.objects.update_or_create(
            name="Daily task - Book of the minute",
            defaults={
                "crontab": schedule,
                "task": "Application.tasks.libro_del_dia",
                "enabled": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("✅ Periodic task configured."))

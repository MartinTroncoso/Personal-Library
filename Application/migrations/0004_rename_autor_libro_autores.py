# Generated by Django 5.2 on 2025-04-22 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0003_libro_descripción'),
    ]

    operations = [
        migrations.RenameField(
            model_name='libro',
            old_name='autor',
            new_name='autores',
        ),
    ]

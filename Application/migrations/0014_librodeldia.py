# Generated by Django 5.2.1 on 2025-05-19 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0013_alter_libro_autores'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibroDelDia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('subtitulo', models.CharField(blank=True, max_length=150, null=True)),
                ('descripcion', models.TextField()),
                ('autores', models.CharField(max_length=500)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('portada', models.URLField(blank=True, null=True)),
                ('visibilidad', models.CharField(default='UNKNOWN', max_length=10)),
                ('link_lectura', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'LibroDelDia',
                'db_table': 'LibroDelDia',
            },
        ),
    ]

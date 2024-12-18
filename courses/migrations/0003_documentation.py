# Generated by Django 4.1 on 2024-11-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_completed_course_completed_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('framework', 'Framework'), ('language', 'Lenguaje de Programación'), ('library', 'Librería'), ('tool', 'Herramienta'), ('other', 'Otro')], max_length=20)),
                ('icon_url', models.URLField(blank=True, help_text='URL de un ícono representativo (opcional)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('favorite', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-favorite', '-created_at'],
            },
        ),
    ]

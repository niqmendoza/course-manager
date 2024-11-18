from django.db import migrations, models
import django.db.models.deletion

def create_default_platforms(apps, schema_editor):
    Platform = apps.get_model('courses', 'Platform')
    Course = apps.get_model('courses', 'Course')
    
    # Crear plataformas por defecto
    platforms = {
        'youtube': Platform.objects.create(name='YouTube'),
        'udemy': Platform.objects.create(name='Udemy'),
        'platzi': Platform.objects.create(name='Platzi'),
        'otros': Platform.objects.create(name='Otros'),
    }
    
    # Actualizar los cursos existentes
    for course in Course.objects.all():
        platform_name = course.platform.lower() if course.platform else 'otros'
        platform = platforms.get(platform_name) or platforms['otros']
        course.new_platform = platform
        course.save()

def reverse_platforms(apps, schema_editor):
    Platform = apps.get_model('courses', 'Platform')
    Platform.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_programminglanguage_alter_course_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.RenameModel(
            old_name='Route',
            new_name='LearningPath',
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='learningpath',
            options={'ordering': ['name']},
        ),
        migrations.RenameField(
            model_name='course',
            old_name='route',
            new_name='learning_path',
        ),
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='difficulty',
            field=models.CharField(choices=[('principiante', 'Principiante'), ('intermedio', 'Intermedio'), ('avanzado', 'Avanzado')], default='principiante', max_length=20),
        ),
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='course',
            name='new_platform',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='courses.platform'),
        ),
        migrations.RunPython(create_default_platforms, reverse_platforms),
        migrations.RemoveField(
            model_name='course',
            name='platform',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='new_platform',
            new_name='platform',
        ),
    ]

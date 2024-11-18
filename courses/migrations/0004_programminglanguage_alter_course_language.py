from django.db import migrations, models
import django.db.models.deletion

def migrate_languages_forward(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    ProgrammingLanguage = apps.get_model('courses', 'ProgrammingLanguage')
    db_alias = schema_editor.connection.alias
    
    # Obtener todos los lenguajes únicos existentes
    existing_languages = set()
    for course in Course.objects.using(db_alias).all():
        if course.language:
            existing_languages.add(course.language)
    
    # Crear los objetos ProgrammingLanguage
    language_mapping = {}
    for lang in existing_languages:
        if lang:  # Solo si el lenguaje no es None
            language_obj = ProgrammingLanguage.objects.using(db_alias).create(name=lang)
            language_mapping[lang] = language_obj.id
    
    # Actualizar los cursos con las nuevas referencias usando SQL directo
    for old_lang, new_id in language_mapping.items():
        Course.objects.using(db_alias).filter(language=old_lang).update(language_id=new_id)

def migrate_languages_backward(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    ProgrammingLanguage = apps.get_model('courses', 'ProgrammingLanguage')
    db_alias = schema_editor.connection.alias
    
    # Convertir las referencias de nuevo a strings
    for course in Course.objects.using(db_alias).all():
        if course.language_id:
            lang = ProgrammingLanguage.objects.using(db_alias).get(id=course.language_id)
            course.language = lang.name
            course.save()

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_documentation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammingLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        # Agregar campo temporal language_id
        migrations.AddField(
            model_name='course',
            name='language_id',
            field=models.IntegerField(null=True),
        ),
        # Ejecutar la migración de datos
        migrations.RunPython(
            migrate_languages_forward,
            migrate_languages_backward,
        ),
        # Eliminar el campo language original
        migrations.RemoveField(
            model_name='course',
            name='language',
        ),
        # Renombrar language_id a language y convertirlo en ForeignKey
        migrations.AlterField(
            model_name='course',
            name='language_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='courses.programminglanguage'),
        ),
        migrations.RenameField(
            model_name='course',
            old_name='language_id',
            new_name='language',
        ),
    ]

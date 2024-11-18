# Gestor de Cursos

Una aplicación web desarrollada con Django para gestionar y organizar enlaces a cursos en línea de diferentes plataformas.

## Características

- Almacenamiento de URLs de cursos de YouTube, Udemy, Platzi y otras plataformas
- Generación automática de miniaturas para videos de YouTube
- Categorización por rutas de aprendizaje
- Filtrado por lenguaje de programación y plataforma
- Interfaz moderna y responsive

## Requisitos

- Python 3.8+
- Django 4.2+
- Pillow
- Requests

## Instalación

1. Crea un entorno virtual:
```bash
python -m venv venv
```

2. Activa el entorno virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Realiza las migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crea un superusuario (opcional):
```bash
python manage.py createsuperuser
```

6. Inicia el servidor:
```bash
python manage.py runserver
```

## Uso

1. Accede a la aplicación en `http://localhost:8000`
2. Usa el botón "Agregar Curso" para añadir nuevos cursos
3. Crea rutas de aprendizaje usando el botón "Nueva Ruta"
4. Filtra los cursos por ruta, lenguaje o plataforma

## Estructura del Proyecto

- `courses/`: Aplicación principal
  - `models.py`: Definición de modelos (Course, Route)
  - `views.py`: Lógica de la aplicación
  - `forms.py`: Formularios para crear cursos y rutas
  - `urls.py`: Configuración de URLs
- `templates/`: Plantillas HTML
- `static/`: Archivos estáticos (CSS, JS, iconos)
- `media/`: Archivos subidos por usuarios (miniaturas)



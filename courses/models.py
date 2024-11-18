from django.db import models
from django.utils import timezone
import requests
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
import os

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class LearningPath(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Platform(models.Model):
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('udemy', 'Udemy'),
        ('platzi', 'Platzi'),
        ('otros', 'Otros'),
    ]

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  
    url = models.URLField()
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='courses')
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.SET_NULL, null=True, related_name='courses')
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='courses')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='principiante')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def toggle_completion(self):
        self.completed = not self.completed
        self.completed_at = timezone.now() if self.completed else None
        self.save()

    def save(self, *args, **kwargs):
        if not self.thumbnail:
            self.generate_thumbnail()
        super().save(*args, **kwargs)

    def get_youtube_video_id(self):
        parsed_url = urlparse(self.url)
        if 'youtube.com' in parsed_url.netloc:
            if 'v=' in parsed_url.query:
                return parsed_url.query.split('v=')[1].split('&')[0]
        elif 'youtu.be' in parsed_url.netloc:
            return parsed_url.path[1:]
        return None

    def generate_thumbnail(self):
        video_id = self.get_youtube_video_id()
        if video_id:
            try:
                thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
                response = requests.get(thumbnail_url)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    output = BytesIO()
                    img.save(output, format='JPEG')
                    output.seek(0)
                    self.thumbnail.save(f'{video_id}.jpg', output)
            except Exception as e:
                print(f"Error al generar la miniatura: {e}")
        else:
            platform_icons = {
                'udemy': 'udemy_icon.png',
                'platzi': 'platzi_icon.png',
                'otros': 'course_icon.png'
            }
            icon_path = f'static/icons/{platform_icons.get(self.platform.name.lower(), "course_icon.png")}'
            if os.path.exists(icon_path):
                self.thumbnail.save(
                    f'{self.platform.name.lower()}_icon.png',
                    open(icon_path, 'rb')
                )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Documentation(models.Model):
    CATEGORY_CHOICES = [
        ('framework', 'Framework'),
        ('language', 'Lenguaje de Programación'),
        ('library', 'Librería'),
        ('tool', 'Herramienta'),
        ('other', 'Otro'),
    ]

    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon_url = models.URLField(blank=True, help_text="URL de un ícono representativo (opcional)")
    created_at = models.DateTimeField(auto_now_add=True)
    favorite = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-favorite', '-created_at']
        
    def __str__(self):
        return self.title

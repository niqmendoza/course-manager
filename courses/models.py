from django.db import models
import requests
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
import os

class Route(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('udemy', 'Udemy'),
        ('platzi', 'Platzi'),
        ('otros', 'Otros'),
    ]

    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('csharp', 'C#'),
        ('php', 'PHP'),
        ('ruby', 'Ruby'),
        ('swift', 'Swift'),
        ('otros', 'Otros'),
    ]

    title = models.CharField(max_length=200)
    url = models.URLField()
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='courses')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.thumbnail:
            self.generate_thumbnail()
        super().save(*args, **kwargs)

    def generate_thumbnail(self):
        if 'youtube.com' in self.url or 'youtu.be' in self.url:
            video_id = self.get_youtube_video_id()
            if video_id:
                thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
                self.save_thumbnail_from_url(thumbnail_url)
        else:
            # Para otras plataformas, usar un ícono predeterminado según la plataforma
            platform_icons = {
                'udemy': 'udemy_icon.png',
                'platzi': 'platzi_icon.png',
                'otros': 'course_icon.png'
            }
            icon_path = f'static/icons/{platform_icons.get(self.platform, "course_icon.png")}'
            if os.path.exists(icon_path):
                self.thumbnail.save(
                    f'{self.platform}_icon.png',
                    open(icon_path, 'rb')
                )

    def get_youtube_video_id(self):
        parsed_url = urlparse(self.url)
        if 'youtube.com' in self.url:
            query = parsed_url.query
            return query.split('v=')[1].split('&')[0] if 'v=' in query else None
        elif 'youtu.be' in self.url:
            return parsed_url.path[1:]
        return None

    def save_thumbnail_from_url(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img_io = BytesIO()
                img.save(img_io, format='PNG')
                self.thumbnail.save(
                    f'thumbnail_{self.id}.png',
                    BytesIO(img_io.getvalue()),
                    save=False
                )
        except Exception as e:
            print(f"Error al generar la miniatura: {e}")

    def __str__(self):
        return self.title

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

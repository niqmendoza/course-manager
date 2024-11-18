from googleapiclient.discovery import build
from django.conf import settings
from .models import Course
import re
from urllib.parse import urlparse, parse_qs

class YouTubeRecommender:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    
    def extract_video_id(self, url):
        """Extrae el ID del video de una URL de YouTube."""
        try:
            parsed_url = urlparse(url)
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
                if parsed_url.path == '/watch':
                    return parse_qs(parsed_url.query)['v'][0]
                elif parsed_url.path.startswith('/embed/'):
                    return parsed_url.path.split('/')[2]
                elif parsed_url.path.startswith('/v/'):
                    return parsed_url.path.split('/')[2]
            elif parsed_url.hostname == 'youtu.be':
                return parsed_url.path[1:]
        except:
            return None
        return None
    
    def clean_text(self, text):
        """Limpia el texto de caracteres especiales y palabras comunes."""
        # Eliminar caracteres especiales
        text = re.sub(r'[^\w\s]', '', text)
        # Convertir a minúsculas
        text = text.lower()
        # Eliminar palabras comunes en español e inglés
        stop_words = {'curso', 'tutorial', 'aprende', 'learn', 'complete', 'guide', 'how', 'to', 'de', 'la', 'el', 'en', 'y', 'a'}
        return ' '.join(word for word in text.split() if word not in stop_words)
    
    def get_search_query(self, course):
        """Genera una consulta de búsqueda basada en el curso."""
        # Combinar título y lenguaje
        query_parts = []
        
        # Agregar lenguaje si está disponible
        if course.language:
            query_parts.append(course.language.name)
        
        # Limpiar y agregar el título
        cleaned_title = self.clean_text(course.title)
        query_parts.append(cleaned_title)
        
        # Agregar términos relacionados con programación
        query_parts.append("programming tutorial")
        
        return ' '.join(query_parts)
    
    def get_video_details(self, video_id):
        """Obtiene detalles adicionales de un video."""
        try:
            video_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=video_id
            ).execute()
            
            if video_response['items']:
                video = video_response['items'][0]
                return {
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'thumbnail': video['snippet']['thumbnails']['high']['url'],
                    'channel_title': video['snippet']['channelTitle'],
                    'view_count': int(video['statistics'].get('viewCount', 0)),
                    'like_count': int(video['statistics'].get('likeCount', 0)),
                    'duration': video['contentDetails']['duration'],
                    'published_at': video['snippet']['publishedAt']
                }
        except Exception as e:
            print(f"Error al obtener detalles del video: {e}")
        return None
    
    def get_recommendations(self, course, max_results=6):
        """Obtiene recomendaciones de videos basadas en un curso."""
        try:
            # Generar consulta de búsqueda
            search_query = self.get_search_query(course)
            
            # Obtener los IDs de videos existentes en la biblioteca
            existing_video_ids = set()
            for existing_course in Course.objects.all():
                video_id = self.extract_video_id(existing_course.url)
                if video_id:
                    existing_video_ids.add(video_id)
            
            # Realizar búsqueda en YouTube
            search_response = self.youtube.search().list(
                q=search_query,
                part='id,snippet',
                maxResults=max_results * 2,  # Pedimos el doble para tener margen después de filtrar
                type='video',
                relevanceLanguage='es',  # Preferencia por videos en español
                videoDefinition='high',  # Preferencia por videos de alta calidad
                order='relevance'  # Ordenar por relevancia
            ).execute()
            
            recommendations = []
            for item in search_response['items']:
                video_id = item['id']['videoId']
                
                # Saltar si el video ya está en la biblioteca de cursos
                if video_id in existing_video_ids:
                    continue
                
                # Obtener detalles adicionales del video
                video_details = self.get_video_details(video_id)
                if video_details:
                    recommendations.append({
                        'video_id': video_id,
                        'url': f'https://www.youtube.com/watch?v={video_id}',
                        **video_details
                    })
                
                # Si ya tenemos suficientes recomendaciones, paramos
                if len(recommendations) >= max_results:
                    break
            
            return recommendations[:max_results]  # Asegurarnos de devolver exactamente max_results
            
        except Exception as e:
            print(f"Error al obtener recomendaciones: {e}")
            return []
    
    def get_recommendations_for_all_courses(self, max_results_per_course=6):
        """Obtiene recomendaciones para todos los cursos en la base de datos."""
        all_recommendations = {}
        courses = Course.objects.all()
        
        for course in courses:
            recommendations = self.get_recommendations(course, max_results_per_course)
            if recommendations:
                all_recommendations[course.id] = recommendations
        
        return all_recommendations

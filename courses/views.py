from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Course, Documentation, ProgrammingLanguage, LearningPath, Platform
from .forms import CourseForm, DocumentationForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from collections import Counter
from .youtube_recommendations import YouTubeRecommender

def home(request):
    learning_paths = LearningPath.objects.all()
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses/home.html', {
        'learning_paths': learning_paths,
        'courses': courses
    })

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'Curso agregado exitosamente.')
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CourseForm()

    context = {
        'form': form,
        'languages': ProgrammingLanguage.objects.all().order_by('name'),
        'learning_paths': LearningPath.objects.all().order_by('name'),
        'platforms': Platform.objects.all().order_by('name'),
    }
    return render(request, 'courses/add_course.html', context)

def add_learning_path(request):
    if request.method == 'POST':
        form = LearningPathForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'learning_path_name': form.cleaned_data['name']})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, 'Curso eliminado exitosamente!')
    return redirect('home')

def filter_courses(request):
    learning_path_id = request.GET.get('learning_path')
    language = request.GET.get('language')
    platform = request.GET.get('platform')
    
    courses = Course.objects.all()
    
    if learning_path_id:
        courses = courses.filter(learning_path_id=learning_path_id)
    if language:
        courses = courses.filter(language=language)
    if platform:
        courses = courses.filter(platform=platform)
        
    return render(request, 'courses/course_list_partial.html', {
        'courses': courses
    })

def toggle_course_completion(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.completed = not course.completed
    course.completed_at = timezone.now() if course.completed else None
    course.save()
    return JsonResponse({
        'status': 'success',
        'completed': course.completed,
        'completed_at': course.completed_at.strftime('%d/%m/%Y %H:%M') if course.completed_at else None
    })

def recommendations(request):
    """Vista para mostrar recomendaciones de cursos y videos relacionados."""
    try:
        # Obtener recomendaciones de YouTube
        recommender = YouTubeRecommender()
        all_recommendations = recommender.get_recommendations_for_all_courses(max_results_per_course=6)
        
        # Preparar el contexto
        courses_with_recommendations = []
        for course_id, videos in all_recommendations.items():
            try:
                course = Course.objects.get(id=course_id)
                # Solo agregar cursos que tengan al menos una recomendación
                if videos:
                    courses_with_recommendations.append({
                        'course': course,
                        'videos': videos
                    })
            except Course.DoesNotExist:
                continue
        
        context = {
            'courses_with_recommendations': courses_with_recommendations,
        }
        
        return render(request, 'courses/recommendations.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al obtener recomendaciones: {str(e)}')
        return redirect('home')

def documentation_list(request):
    docs = Documentation.objects.all()
    
    if request.method == 'POST':
        form = DocumentationForm(request.POST)
        if form.is_valid():
            doc = form.save()
            return JsonResponse({
                'status': 'success',
                'doc': {
                    'id': doc.id,
                    'title': doc.title,
                    'description': doc.description,
                    'category': doc.category,
                    'icon_url': doc.icon_url,
                    'url': doc.url,
                    'favorite': doc.favorite
                }
            })
        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        }, status=400)
    
    return render(request, 'courses/documentation_list.html', {
        'docs': docs
    })

def toggle_favorite(request, doc_id):
    doc = get_object_or_404(Documentation, id=doc_id)
    doc.favorite = not doc.favorite
    doc.save()
    return JsonResponse({
        'status': 'success',
        'favorite': doc.favorite
    })

def delete_documentation(request, doc_id):
    if request.method == 'POST':
        doc = get_object_or_404(Documentation, id=doc_id)
        doc.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def update_icon_url(request, doc_id):
    if request.method == 'POST':
        doc = get_object_or_404(Documentation, id=doc_id)
        new_icon_url = request.POST.get('icon_url', '')
        doc.icon_url = new_icon_url
        doc.save()
        return JsonResponse({
            'status': 'success',
            'icon_url': doc.icon_url
        })
    return JsonResponse({'status': 'error'}, status=400)

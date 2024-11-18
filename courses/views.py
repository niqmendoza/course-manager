from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Course, Route, Documentation
from .forms import CourseForm, RouteForm, DocumentationForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from collections import Counter

def home(request):
    routes = Route.objects.all()
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses/home.html', {
        'routes': routes,
        'courses': courses
    })

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso agregado exitosamente!')
            return redirect('home')
    else:
        form = CourseForm()
    
    return render(request, 'courses/add_course.html', {
        'form': form
    })

def add_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'route_name': form.cleaned_data['name']})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, 'Curso eliminado exitosamente!')
    return redirect('home')

def filter_courses(request):
    route_id = request.GET.get('route')
    language = request.GET.get('language')
    platform = request.GET.get('platform')
    
    courses = Course.objects.all()
    
    if route_id:
        courses = courses.filter(route_id=route_id)
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
    # Obtener las rutas más frecuentes del usuario
    user_routes = Course.objects.values('route').annotate(
        total_courses=Count('id')
    ).order_by('-total_courses')[:3]
    
    # Obtener los lenguajes más frecuentes del usuario
    user_languages = Course.objects.values_list('language', flat=True)
    common_languages = Counter(user_languages).most_common(3)
    
    recommendations = {
        'by_route': {},
        'by_language': {},
        'similar_courses': []
    }
    
    # Recomendaciones por ruta
    for route_data in user_routes:
        route = Route.objects.get(id=route_data['route'])
        # Obtener cursos de la misma ruta que no estén en la biblioteca del usuario
        route_courses = Course.objects.filter(route=route)
        
        # Aquí podrías implementar lógica adicional para filtrar o priorizar cursos
        recommendations['by_route'][route.name] = route_courses[:3]
    
    # Recomendaciones por lenguaje
    for language, count in common_languages:
        language_display = dict(Course.LANGUAGE_CHOICES)[language]
        # Obtener cursos del mismo lenguaje
        language_courses = Course.objects.filter(language=language)
        recommendations['by_language'][language_display] = language_courses[:3]
    
    # Recomendaciones generales basadas en similitud
    if user_routes.exists():
        main_route = Route.objects.get(id=user_routes[0]['route'])
        # Encontrar cursos similares basados en la ruta principal y lenguajes comunes
        similar_courses = Course.objects.filter(
            route=main_route
        ).exclude(
            id__in=Course.objects.values_list('id', flat=True)
        )
        
        if common_languages:
            similar_courses = similar_courses.filter(
                language__in=[lang for lang, _ in common_languages]
            )
        
        recommendations['similar_courses'] = similar_courses[:6]
    
    # Obtener estadísticas generales
    stats = {
        'total_courses': Course.objects.count(),
        'completed_courses': Course.objects.filter(completed=True).count(),
        'total_routes': Route.objects.count(),
        'most_used_platform': Course.objects.values('platform').annotate(
            total=Count('id')
        ).order_by('-total').first()
    }
    
    return render(request, 'courses/recommendations.html', {
        'recommendations': recommendations,
        'stats': stats,
        'routes': Route.objects.all(),  # Para el filtro de rutas
    })

def documentation_list(request):
    documentations = Documentation.objects.all()
    form = DocumentationForm()
    
    if request.method == 'POST':
        form = DocumentationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('documentation_list')
    
    # Agrupar documentaciones por categoría
    docs_by_category = {}
    for doc in documentations:
        category = doc.get_category_display()
        if category not in docs_by_category:
            docs_by_category[category] = []
        docs_by_category[category].append(doc)
    
    return render(request, 'courses/documentation_list.html', {
        'docs_by_category': docs_by_category,
        'form': form
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
        return redirect('documentation_list')
    return redirect('documentation_list')

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

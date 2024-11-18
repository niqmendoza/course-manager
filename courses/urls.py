from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-course/', views.add_course, name='add_course'),
    path('add-learning-path/', views.add_learning_path, name='add_learning_path'),
    path('toggle-completion/<int:course_id>/', views.toggle_course_completion, name='toggle_course_completion'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('filter-courses/', views.filter_courses, name='filter_courses'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('documentation/', views.documentation_list, name='documentation_list'),
    path('documentation/toggle-favorite/<int:doc_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('documentation/delete/<int:doc_id>/', views.delete_documentation, name='delete_documentation'),
    path('documentation/update-icon/<int:doc_id>/', views.update_icon_url, name='update_icon_url'),
]

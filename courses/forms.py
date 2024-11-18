from django import forms
from .models import Course, Route, Documentation

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'url', 'platform', 'language', 'route']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'route': forms.Select(attrs={'class': 'form-control'}),
        }

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class DocumentationForm(forms.ModelForm):
    class Meta:
        model = Documentation
        fields = ['title', 'url', 'description', 'category', 'icon_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'icon_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

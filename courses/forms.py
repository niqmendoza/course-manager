from django import forms
from .models import Course, Documentation, ProgrammingLanguage, LearningPath, Platform

class ProgrammingLanguageForm(forms.ModelForm):
    class Meta:
        model = ProgrammingLanguage
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class LearningPathForm(forms.ModelForm):
    class Meta:
        model = LearningPath
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class CourseForm(forms.ModelForm):
    new_language = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'O ingresa un nuevo lenguaje'
        })
    )
    new_learning_path = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'O ingresa una nueva ruta'
        })
    )
    new_platform = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'O ingresa una nueva plataforma'
        })
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'url', 'language', 'learning_path', 'platform', 'difficulty']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'learning_path': forms.Select(attrs={'class': 'form-control'}),
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Manejar nuevo lenguaje
        new_language = cleaned_data.get('new_language')
        language = cleaned_data.get('language')
        
        if new_language and not language:
            language, _ = ProgrammingLanguage.objects.get_or_create(name=new_language.strip())
            cleaned_data['language'] = language
        elif not language and not new_language:
            raise forms.ValidationError('Debes seleccionar un lenguaje o crear uno nuevo')

        # Manejar nueva ruta de aprendizaje
        new_learning_path = cleaned_data.get('new_learning_path')
        learning_path = cleaned_data.get('learning_path')
        
        if new_learning_path and not learning_path:
            learning_path, _ = LearningPath.objects.get_or_create(name=new_learning_path.strip())
            cleaned_data['learning_path'] = learning_path
        elif not learning_path and not new_learning_path:
            raise forms.ValidationError('Debes seleccionar una ruta de aprendizaje o crear una nueva')

        # Manejar nueva plataforma
        new_platform = cleaned_data.get('new_platform')
        platform = cleaned_data.get('platform')
        
        if new_platform and not platform:
            platform, _ = Platform.objects.get_or_create(name=new_platform.strip())
            cleaned_data['platform'] = platform
        elif not platform and not new_platform:
            raise forms.ValidationError('Debes seleccionar una plataforma o crear una nueva')

        return cleaned_data

class DocumentationForm(forms.ModelForm):
    class Meta:
        model = Documentation
        fields = ['title', 'url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

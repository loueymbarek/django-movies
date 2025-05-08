from django import forms
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'description', 'image', 'genres']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'genres': forms.CheckboxSelectMultiple(),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer_name', 'rating', 'comment']
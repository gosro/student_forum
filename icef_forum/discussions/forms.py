from django import forms
from .models import Post,Rating,Vacancy, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text','title','professor','course','job']
        labels = {
           'text': ('Текст поста'),
        }
        help_texts = {
            'text': ('Текст нового поста '),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': ('Comment text')
        }
        help_texts = {
            'text': ('Comment text')
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.Select(choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])
        }

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['text', 'title', 'company','link','job']
        labels = {
            'text': ('Vacancy text'),
            'title':('Vacancy title'),
            'company': ('Hiring company'),
            'link':('Link')
        }
        help_texts = {
            'text': ('Text of the vacancy '),
            'company': ('What company is hiring '),
            'link':('Link to the original vacancy or hiring company web site')
        }
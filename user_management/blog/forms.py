from django import forms
from .models import BlogPost, Category

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content', 'is_draft']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 
                                            'placeholder': 'Write a brief summary (15 words recommended)'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 
                                            'placeholder': 'Write your blog content here'}),
            'is_draft': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

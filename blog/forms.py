from django import forms
from .models import Blog
from tinymce.widgets import TinyMCE

class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Blog
        fields = ['title', 'category', 'image', 'content', 'published', 'meta_title', 'meta_description', 'focus_keyword']
        widgets = {
            'category': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500',
                'placeholder': 'eg "Food"',
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500',
                'placeholder': ' eg "The Secret Recipe to a Perfect Pizza"',
            }),
            'published': forms.CheckboxInput(attrs={
                'class': 'toggle toggle-success',
            }),
            'meta_description': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500',
                'placeholder': 'A brief description of the blog post for SEO purposes.',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500',
                'placeholder': '10 Pizza Recipes You Must Try',
            }),
            'focus_keyword': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500',
                'placeholder': 'homemade pizza',
            }),
            

        }
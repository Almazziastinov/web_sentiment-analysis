from .models import Articles
from django.forms import ModelForm, Textarea

class ArticleForms(ModelForm):
    class Meta:
        model = Articles
        fields = ['content']

        widgets = {
            "content": Textarea(attrs ={
                "placeholder": 'Введите текст',
                'class': "tar"
            } )

        }
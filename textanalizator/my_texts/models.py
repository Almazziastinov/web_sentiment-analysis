from django.db import models
from django.utils import timezone



class Articles(models.Model):
    text_id = models.IntegerField('ID текста', default= 0)
    source = models.CharField('Источник', max_length = 250,default='client')
    query = models.CharField('Запрос', max_length = 250,default='client')
    content = models.TextField('Содержание')
    tone = models.CharField('Тональность', max_length = 50)
    date = models.DateTimeField('Дата анализа', default=timezone.now)


    def __str__(self):
        return self.source

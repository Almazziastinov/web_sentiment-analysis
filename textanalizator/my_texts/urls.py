from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_texts_home, name = 'texts'),
    path('create', views.create, name = 'create'),
    path('find', views.find, name = 'find'),
    path('some_content', views.get_some_content, name = 'some_content'),
    path('content', views.cont_, name = 'content'),
    path('dynamic_analysis', views.dynamic_analysis, name = 'dynamics')
]



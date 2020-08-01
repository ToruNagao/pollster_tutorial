from  django.urls import path
from . import views

# Create route
urlpatterns = [
    path('', views.index, name='index'),
]
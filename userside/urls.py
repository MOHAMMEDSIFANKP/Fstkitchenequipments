from django.urls import path
from .views import *
urlpatterns = [
    path('', Home.as_view(), name='Home'),
    path('category/', Category.as_view(), name='Category'),
    path('sifan/', sifan.as_view(), name='sifan'),
]

from django.urls import path
from .views import *
urlpatterns = [
    path('', Home.as_view(), name='Home'),
    path('category/', Category_User.as_view(), name='Category_User'),
    path('sifan/', sifan.as_view(), name='sifan'),
]

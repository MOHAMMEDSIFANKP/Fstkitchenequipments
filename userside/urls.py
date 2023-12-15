from django.urls import path
from .views import *
urlpatterns = [
    path('', Home.as_view(), name='Home'),
    path('category/', Category_List.as_view(), name='Category_List'),
    path('products/<int:pk>/', Product_List.as_view(), name='Product_List'),
    path('products/', Product_List.as_view(), name='Product_List'),
]

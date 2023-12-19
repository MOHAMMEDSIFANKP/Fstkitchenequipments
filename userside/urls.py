from django.urls import path
from .views import *
urlpatterns = [
    path('', Home.as_view(), name='Home'),
    path('category/', Category_List.as_view(), name='Category_List'),
    path('products/<int:pk>/', Product_List.as_view(), name='Product_List'),
    path('products/', Product_List.as_view(), name='Product_List'),
    path('about/', About_Us.as_view(), name='About_Us'),
    path('careers/', Careers_Page.as_view(), name='Careers_Page'),
    path('contact/', Contact_Page.as_view(), name='Contact_Page'),
]


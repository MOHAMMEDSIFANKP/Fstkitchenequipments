from django.urls import path
from .views import *
urlpatterns = [
    path('',DashboardHome.as_view(), name='DashboardHome'),
    path('signin/',Signin.as_view(), name='Signin'),
    path('signout/',CustomLogoutView.as_view(), name='CustomLogoutView'),
    
    path('backgroudimages/',BackgroudImages.as_view(), name='BackgroudImages'),
    path('category/',Category.as_view(), name='Category'),
    path('product/',Product.as_view(), name='Product'),

]

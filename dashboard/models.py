from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class BgImages(models.Model):
    image = models.ImageField(upload_to='backgroundimages/')
    sub_heading = models.CharField(max_length=150,blank=True,null=True)
    main_heading = models.CharField(max_length=150,blank=True,null=True)

    def __str__(self):
        return self.main_heading
    
class Categories(models.Model):
    image = models.ImageField(upload_to='category/')
    name = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Clients(models.Model):
    image = models.ImageField(upload_to='clients/')
    name = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Careers(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20, verbose_name="Mobile Number")
    cv = models.FileField(upload_to='cv/')
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class About_Story(models.Model):
    image = models.ImageField(upload_to='story/')
    body = RichTextField(blank=True,null=True)
    is_show = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

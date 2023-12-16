from django.db import models

# Create your models here.

class BgImages(models.Model):
    image = models.ImageField(upload_to='media/backgroundimages/')
    sub_heading = models.CharField(max_length=150,blank=True,null=True)
    main_heading = models.CharField(max_length=150,blank=True,null=True)

    def __str__(self):
        return self.main_heading
    
class Categories(models.Model):
    image = models.ImageField(upload_to='media/category/')
    name = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    image = models.ImageField(upload_to='media/products/')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Clients(models.Model):
    image = models.ImageField(upload_to='media/clients/')
    name = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
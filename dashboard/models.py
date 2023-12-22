from django.db import models
from ckeditor.fields import RichTextField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.

class BgImages(models.Model):
    image = models.ImageField(upload_to='backgroundimages/')
    sub_heading = models.CharField(max_length=150,blank=True,null=True)
    main_heading = models.CharField(max_length=150,blank=True,null=True)
    cropped_image = ImageSpecField(source='image',
                                   processors=[ResizeToFill(1200, 525)],
                                   format='JPEG',
                                   options={'quality': 100})

    def __str__(self):
        return self.main_heading
    
class Categories(models.Model):
    image = models.ImageField(upload_to='category/')
    name = models.CharField(max_length=150,null=True,blank=True)
    cropped_image = ImageSpecField(source='image',
                                   processors=[ResizeToFill(864, 432)],
                                   format='JPEG',
                                   options={'quality': 100})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    image = models.ImageField(upload_to='products/')
    cropped_image = ImageSpecField(source='image',
                                   processors=[ResizeToFill(300, 400)],
                                   format='JPEG',
                                   options={'quality': 100})
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
    

class Clients(models.Model):
    image = models.ImageField(upload_to='clients/')
    cropped_image = ImageSpecField(source='image',
                                   processors=[ResizeToFill(626, 626)],
                                   format='JPEG',
                                   options={'quality': 100})
    name = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Careers(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20, verbose_name="Mobile Number")
    cv = models.FileField(upload_to='cv/')
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Contacts(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20, verbose_name="Mobile Number")
    subject = models.CharField(max_length=250)
    address = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class About_Story(models.Model):
    image = models.ImageField(upload_to='story/')
    body = RichTextField(blank=True,null=True)
    is_show = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


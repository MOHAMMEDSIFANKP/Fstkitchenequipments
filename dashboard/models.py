from django.db import models

# Create your models here.

class BgImages(models.Model):
    image = models.ImageField(upload_to='media/backgroundimages/')
    sub_heading = models.CharField(max_length=150,blank=True,null=True)
    main_heading = models.CharField(max_length=150,blank=True,null=True)

    def __str__(self):
        return self.main_heading
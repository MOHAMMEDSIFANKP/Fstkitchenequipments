# Generated by Django 4.2.7 on 2023-12-05 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BgImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/backgroundimages/')),
                ('sub_headding', models.CharField(blank=True, max_length=150, null=True)),
                ('main_headding', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
    ]

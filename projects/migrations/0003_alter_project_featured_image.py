# Generated by Django 4.0.4 on 2022-05-07 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='default.JPG', null=True, upload_to=''),
        ),
    ]
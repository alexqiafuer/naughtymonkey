# Generated by Django 4.0.4 on 2022-05-11 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_location_skill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='social_github',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Github'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='social_twitter',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Twitter'),
        ),
    ]
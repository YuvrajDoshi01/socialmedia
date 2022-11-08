# Generated by Django 4.0.2 on 2022-07-09 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('social', '0004_alter_comment_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('name', models.CharField(max_length=64)),
                ('bio', models.TextField(blank=True, max_length=512)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to='uploads/profile_picutres')),
            ],
        ),
    ]
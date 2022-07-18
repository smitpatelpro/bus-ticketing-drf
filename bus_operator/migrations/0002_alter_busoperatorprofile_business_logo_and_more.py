# Generated by Django 4.0.6 on 2022-07-18 08:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_user_created_at_user_deleted_at_user_updated_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bus_operator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busoperatorprofile',
            name='business_logo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='busoperatorprofile_business_logos', to='common.media'),
        ),
        migrations.AlterField(
            model_name='busoperatorprofile',
            name='ratings',
            field=models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='busoperatorprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='busoperatorprofile_user', to=settings.AUTH_USER_MODEL),
        ),
    ]

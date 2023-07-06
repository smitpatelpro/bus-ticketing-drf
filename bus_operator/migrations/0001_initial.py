# Generated by Django 4.0.6 on 2022-08-24 05:43

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('REGULAR', 'REGULAR'), ('SLEEPER', 'SLEEPER'), ('SLEEPER_DUPLEX', 'SLEEPER_DUPLEX')], max_length=20)),
                ('capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('per_km_fare', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BusAmenity',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BusStoppage',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('count', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('name', models.CharField(max_length=255)),
                ('arrival_time', models.TimeField()),
                ('departure_time', models.TimeField()),
                ('distance_from_last_stop', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2000)])),
                ('journey_type', models.CharField(choices=[('UP', 'UP'), ('DOWN', 'DOWN')], max_length=20)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='busstoppage_bus', to='bus_operator.bus')),
            ],
            options={
                'verbose_name': 'Bus Stop',
                'verbose_name_plural': 'Bus Stops',
                'ordering': ['bus', 'count', 'journey_type'],
                'unique_together': {('bus', 'count')},
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('journey_date', models.DateField()),
                ('number', models.CharField(max_length=255)),
                ('seats', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('invoice_number', models.CharField(blank=True, max_length=255)),
                ('transaction_id', models.CharField(blank=True, max_length=255)),
                ('rating', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('payment_status', models.CharField(choices=[('PENDING', 'PENDING'), ('SUCCESSFUL', 'SUCCESSFUL'), ('FAILED', 'FAILED')], max_length=20)),
                ('payment_link', models.URLField(blank=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_bus', to='bus_operator.bus')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_customer', to='customer.customerprofile')),
                ('end_bus_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_end_bus_stop', to='bus_operator.busstoppage')),
                ('start_bus_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_start_bus_stop', to='bus_operator.busstoppage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BusOperatorProfile',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business_name', models.CharField(max_length=255)),
                ('office_address', models.TextField()),
                ('ratings', models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('approval_status', models.CharField(choices=[('APPROVED', 'APPROVED'), ('PENDING_APPROVAL', 'PENDING_APPROVAL'), ('REJECTED', 'REJECTED')], max_length=20)),
                ('rejection_comment', models.TextField(blank=True)),
                ('business_logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='busoperatorprofile_business_logo', to='common.media')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='busoperatorprofile_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bus',
            name='amenities',
            field=models.ManyToManyField(blank=True, to='bus_operator.busamenity'),
        ),
        migrations.AddField(
            model_name='bus',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bus_operator', to='bus_operator.busoperatorprofile'),
        ),
        migrations.AddField(
            model_name='bus',
            name='photos',
            field=models.ManyToManyField(blank=True, to='common.media'),
        ),
        migrations.CreateModel(
            name='BusUnavailability',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('reason', models.TextField()),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='busunavailability_bus', to='bus_operator.bus')),
            ],
            options={
                'unique_together': {('bus', 'date')},
            },
        ),
        migrations.CreateModel(
            name='BusJourney',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sequence', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('from_place', models.CharField(max_length=255)),
                ('to_place', models.CharField(max_length=255)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('distance', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2000)])),
                ('journey_type', models.CharField(choices=[('UP', 'UP'), ('DOWN', 'DOWN')], max_length=20)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='busjourney_bus', to='bus_operator.bus')),
            ],
            options={
                'ordering': ['sequence'],
                'unique_together': {('bus', 'sequence', 'from_place', 'to_place')},
            },
        ),
    ]

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('institution', models.CharField(blank=True, max_length=180)),
                ('profession', models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher')], max_length=20)),
                ('needs_accommodation', models.BooleanField(default=False)),
                ('fee_category', models.CharField(max_length=80)),
                ('fee_amount', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Conference Registration',
                'verbose_name_plural': 'Conference Registrations',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AccommodationBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(choices=[('ac', 'AC Room'), ('non_ac', 'Non-AC Room')], max_length=20)),
                ('checkin', models.DateField()),
                ('checkout', models.DateField()),
                ('guests', models.PositiveSmallIntegerField(default=1)),
                ('meal_preference', models.CharField(choices=[('vegetarian', 'Vegetarian'), ('non_vegetarian', 'Non-Vegetarian'), ('vegan', 'Vegan')], max_length=30)),
                ('special_requests', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('registration', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='accommodation_booking', to='myapp.conferenceregistration')),
            ],
            options={
                'verbose_name': 'Accommodation Booking',
                'verbose_name_plural': 'Accommodation Bookings',
                'ordering': ['-created_at'],
            },
        ),
    ]

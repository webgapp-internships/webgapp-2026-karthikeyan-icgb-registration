from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_cms_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="accommodationbooking",
            name="breakfast_count",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="accommodationbooking",
            name="checkin_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="accommodationbooking",
            name="checkout_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="accommodationbooking",
            name="dinner_count",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="accommodationbooking",
            name="lunch_count",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="accommodationbooking",
            name="non_vegetarian_meals",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="accommodationbooking",
            name="rooms_needed",
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="accommodationbooking",
            name="vegan_meals",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="accommodationbooking",
            name="vegetarian_meals",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.CreateModel(
            name="StudentRegistration",
            fields=[],
            options={
                "verbose_name": "Student",
                "verbose_name_plural": "Students",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("myapp.conferenceregistration",),
        ),
        migrations.CreateModel(
            name="TeacherRegistration",
            fields=[],
            options={
                "verbose_name": "Teacher",
                "verbose_name_plural": "Teachers",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("myapp.conferenceregistration",),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommitteeMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=140)),
                ("role", models.CharField(choices=[("chief_patron", "Chief Patron"), ("patron", "Patron"), ("convener", "Convener"), ("organising_secretary", "Organising Secretary"), ("treasurer", "Treasurer"), ("committee_member", "Organising Committee Member"), ("student_team", "Student / Scholar Team")], max_length=40)),
                ("designation", models.CharField(blank=True, max_length=220)),
                ("phone", models.CharField(blank=True, max_length=24)),
                ("display_order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["display_order", "name"]},
        ),
        migrations.CreateModel(
            name="ImportantDate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=140)),
                ("date", models.DateField()),
                ("time_text", models.CharField(blank=True, max_length=80)),
                ("description", models.TextField(blank=True)),
                ("display_order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"verbose_name": "Important Date", "verbose_name_plural": "Important Dates", "ordering": ["display_order", "date"]},
        ),
        migrations.CreateModel(
            name="SiteContent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.SlugField(max_length=80, unique=True)),
                ("label", models.CharField(max_length=120)),
                ("content", models.TextField()),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "Website Text", "verbose_name_plural": "Website Texts", "ordering": ["label"]},
        ),
        migrations.CreateModel(
            name="Speaker",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=140)),
                ("initials", models.CharField(max_length=8)),
                ("role", models.CharField(max_length=140)),
                ("institution", models.CharField(max_length=240)),
                ("topic", models.CharField(max_length=260)),
                ("display_order", models.PositiveSmallIntegerField(default=0)),
                ("is_featured", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["display_order", "name"]},
        ),
        migrations.CreateModel(
            name="VenueInfo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("location", models.CharField(max_length=220)),
                ("help_phone", models.CharField(blank=True, max_length=24)),
                ("help_email", models.EmailField(blank=True, max_length=254)),
                ("details", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"verbose_name": "Venue Information", "verbose_name_plural": "Venue Information", "ordering": ["name"]},
        ),
    ]

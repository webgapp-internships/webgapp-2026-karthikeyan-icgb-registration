from django.db import models

class ConferenceRegistration(models.Model):
    PROFESSION_STUDENT = "student"
    PROFESSION_TEACHER = "teacher"

    PROFESSION_CHOICES = [
        (PROFESSION_STUDENT, "Student"),
        (PROFESSION_TEACHER, "Teacher"),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    institution = models.CharField(max_length=180, blank=True)
    profession = models.CharField(max_length=20, choices=PROFESSION_CHOICES)
    needs_accommodation = models.BooleanField(default=False)
    fee_category = models.CharField(max_length=80)
    fee_amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Conference Registration"
        verbose_name_plural = "Conference Registrations"

    def __str__(self):
        return f"{self.name} - {self.get_profession_display()}"


class StudentRegistration(ConferenceRegistration):
    class Meta:
        proxy = True
        verbose_name = "Student"
        verbose_name_plural = "Students"


class TeacherRegistration(ConferenceRegistration):
    class Meta:
        proxy = True
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"


class AccommodationBooking(models.Model):
    ROOM_AC = "ac"
    ROOM_NON_AC = "non_ac"

    ROOM_CHOICES = [
        (ROOM_AC, "AC Room"),
        (ROOM_NON_AC, "Non-AC Room"),
    ]

    MEAL_CHOICES = [
        ("vegetarian", "Vegetarian"),
        ("non_vegetarian", "Non-Vegetarian"),
        ("vegan", "Vegan"),
    ]

    registration = models.OneToOneField(
        ConferenceRegistration,
        on_delete=models.CASCADE,
        related_name="accommodation_booking",
    )
    room_type = models.CharField(max_length=20, choices=ROOM_CHOICES)
    rooms_needed = models.PositiveSmallIntegerField(default=1)
    checkin = models.DateField()
    checkin_time = models.TimeField(null=True, blank=True)
    checkout = models.DateField()
    checkout_time = models.TimeField(null=True, blank=True)
    guests = models.PositiveSmallIntegerField(default=1)
    meal_preference = models.CharField(max_length=30, choices=MEAL_CHOICES)
    vegetarian_meals = models.PositiveSmallIntegerField(default=0)
    non_vegetarian_meals = models.PositiveSmallIntegerField(default=0)
    vegan_meals = models.PositiveSmallIntegerField(default=0)
    breakfast_count = models.PositiveSmallIntegerField(default=0)
    lunch_count = models.PositiveSmallIntegerField(default=0)
    dinner_count = models.PositiveSmallIntegerField(default=0)
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Accommodation Booking"
        verbose_name_plural = "Accommodation Bookings"

    def __str__(self):
        return f"{self.registration.name} - {self.get_room_type_display()}"


class SiteContent(models.Model):
    key = models.SlugField(max_length=80, unique=True)
    label = models.CharField(max_length=120)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["label"]
        verbose_name = "Website Text"
        verbose_name_plural = "Website Texts"

    def __str__(self):
        return self.label


class VenueInfo(models.Model):
    name = models.CharField(max_length=160)
    location = models.CharField(max_length=220)
    help_phone = models.CharField(max_length=24, blank=True)
    help_email = models.EmailField(blank=True)
    details = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Venue Information"
        verbose_name_plural = "Venue Information"

    def __str__(self):
        return self.name


class ImportantDate(models.Model):
    title = models.CharField(max_length=140)
    date = models.DateField()
    time_text = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "date"]
        verbose_name = "Important Date"
        verbose_name_plural = "Important Dates"

    def __str__(self):
        return f"{self.title} - {self.date:%d %b %Y}"


class Speaker(models.Model):
    name = models.CharField(max_length=140)
    initials = models.CharField(max_length=8)
    role = models.CharField(max_length=140)
    institution = models.CharField(max_length=240)
    topic = models.CharField(max_length=260)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class CommitteeMember(models.Model):
    ROLE_CHOICES = [
        ("chief_patron", "Chief Patron"),
        ("patron", "Patron"),
        ("convener", "Convener"),
        ("organising_secretary", "Organising Secretary"),
        ("treasurer", "Treasurer"),
        ("committee_member", "Organising Committee Member"),
        ("student_team", "Student / Scholar Team"),
    ]

    name = models.CharField(max_length=140)
    role = models.CharField(max_length=40, choices=ROLE_CHOICES)
    designation = models.CharField(max_length=220, blank=True)
    phone = models.CharField(max_length=24, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"

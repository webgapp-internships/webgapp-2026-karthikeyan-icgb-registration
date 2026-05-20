from django.contrib import admin

from .models import (
    AccommodationBooking,
    CommitteeMember,
    ConferenceRegistration,
    ImportantDate,
    SiteContent,
    Speaker,
    StudentRegistration,
    TeacherRegistration,
    VenueInfo,
)


admin.site.site_header = "ICGB 2026 Parent Control"
admin.site.site_title = "ICGB Admin"
admin.site.index_title = "Website Control Panel"


class AccommodationInline(admin.StackedInline):
    model = AccommodationBooking
    extra = 0
    max_num = 1
    can_delete = False
    fieldsets = (
        ("Room Details", {"fields": ("room_type", "rooms_needed", "guests")}),
        ("Stay Timing", {"fields": ("checkin", "checkin_time", "checkout", "checkout_time")}),
        (
            "Meal Counts",
            {
                "fields": (
                    "meal_preference",
                    "vegetarian_meals",
                    "non_vegetarian_meals",
                    "vegan_meals",
                    "breakfast_count",
                    "lunch_count",
                    "dinner_count",
                )
            },
        ),
        ("Notes", {"fields": ("special_requests",)}),
    )


@admin.register(ConferenceRegistration)
class ConferenceRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "profession",
        "needs_accommodation",
        "fee_category",
        "fee_amount",
        "created_at",
    )
    list_filter = ("profession", "needs_accommodation", "fee_category", "created_at")
    search_fields = ("name", "email", "phone", "institution")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"


@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "institution",
        "fee_category",
        "fee_amount",
        "created_at",
    )
    list_filter = ("fee_category", "created_at")
    search_fields = ("name", "email", "phone", "institution")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            profession=ConferenceRegistration.PROFESSION_STUDENT
        )

    def save_model(self, request, obj, form, change):
        obj.profession = ConferenceRegistration.PROFESSION_STUDENT
        obj.needs_accommodation = False
        super().save_model(request, obj, form, change)


@admin.register(TeacherRegistration)
class TeacherRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "institution",
        "needs_accommodation",
        "room_summary",
        "stay_summary",
        "meal_summary",
        "created_at",
    )
    list_filter = ("needs_accommodation", "created_at", "accommodation_booking__room_type")
    search_fields = ("name", "email", "phone", "institution")
    readonly_fields = ("created_at",)
    inlines = (AccommodationInline,)
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            profession=ConferenceRegistration.PROFESSION_TEACHER
        ).select_related("accommodation_booking")

    def save_model(self, request, obj, form, change):
        obj.profession = ConferenceRegistration.PROFESSION_TEACHER
        super().save_model(request, obj, form, change)

    @admin.display(description="Rooms")
    def room_summary(self, obj):
        booking = getattr(obj, "accommodation_booking", None)
        if not booking:
            return "No room"
        return f"{booking.rooms_needed} room(s), {booking.get_room_type_display()}, {booking.guests} guest(s)"

    @admin.display(description="Check-in / Check-out")
    def stay_summary(self, obj):
        booking = getattr(obj, "accommodation_booking", None)
        if not booking:
            return "-"
        checkin_time = booking.checkin_time.strftime("%I:%M %p") if booking.checkin_time else "time not set"
        checkout_time = booking.checkout_time.strftime("%I:%M %p") if booking.checkout_time else "time not set"
        return f"{booking.checkin} {checkin_time} to {booking.checkout} {checkout_time}"

    @admin.display(description="Meals")
    def meal_summary(self, obj):
        booking = getattr(obj, "accommodation_booking", None)
        if not booking:
            return "-"
        return (
            f"Veg {booking.vegetarian_meals}, Non-Veg {booking.non_vegetarian_meals}, "
            f"Vegan {booking.vegan_meals}; "
            f"Breakfast {booking.breakfast_count}, Lunch {booking.lunch_count}, Dinner {booking.dinner_count}"
        )


@admin.register(AccommodationBooking)
class AccommodationBookingAdmin(admin.ModelAdmin):
    list_display = (
        "registration",
        "room_type",
        "rooms_needed",
        "checkin",
        "checkin_time",
        "checkout",
        "checkout_time",
        "guests",
        "meal_preference",
        "vegetarian_meals",
        "non_vegetarian_meals",
        "vegan_meals",
        "breakfast_count",
        "lunch_count",
        "dinner_count",
        "created_at",
    )
    list_filter = ("room_type", "meal_preference", "checkin", "created_at")
    search_fields = (
        "registration__name",
        "registration__email",
        "registration__phone",
        "registration__institution",
    )
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ("label", "key", "updated_at")
    search_fields = ("label", "key", "content")
    readonly_fields = ("updated_at",)
    fieldsets = (
        ("Editable Website Text", {"fields": ("label", "key", "content")}),
        ("System", {"fields": ("updated_at",)}),
    )


@admin.register(VenueInfo)
class VenueInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "help_phone", "help_email", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "location", "help_phone", "help_email", "details")


@admin.register(ImportantDate)
class ImportantDateAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "time_text", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active", "date")
    search_fields = ("title", "description", "time_text")
    date_hierarchy = "date"


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "institution", "topic", "display_order", "is_featured", "is_active")
    list_editable = ("display_order", "is_featured", "is_active")
    list_filter = ("is_featured", "is_active")
    search_fields = ("name", "role", "institution", "topic")


@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "designation", "phone", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("name", "designation", "phone")

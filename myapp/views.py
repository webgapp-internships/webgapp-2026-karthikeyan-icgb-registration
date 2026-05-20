from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import (
    AccommodationBooking,
    CommitteeMember,
    ConferenceRegistration,
    ImportantDate,
    SiteContent,
    Speaker,
    VenueInfo,
)


PRICING = {
    "student": ("Student Regular Registration", 1500),
    "teacher": ("Teacher Regular Registration", 3000),
}

DEFAULT_SPEAKERS = [
    {
        "name": "Prof. Dr. K. Muruga Poopathi Raja",
        "initials": "KR",
        "role": "Professor & Head",
        "institution": "Department of Chemistry, School of Physical Sciences, Central University of Kerala",
        "topic": "Design of Antiviral Peptides to Combat SARS-CoV-2",
        "is_featured": True,
    },
    {
        "name": "Dr. R. Shyam Kumar",
        "initials": "RS",
        "role": "Professor & Head",
        "institution": "Department of Biotechnology, Kamaraj College of Engineering and Technology, Madurai",
        "topic": "Bioprospecting Lichens: Discovering New Leads for Pharmaceuticals and Beyond",
        "is_featured": False,
    },
    {
        "name": "Dr. S. Kathiresan",
        "initials": "SK",
        "role": "Professor",
        "institution": "Department of Biotechnology, School of Integrative Biology, Central University of Tamil Nadu",
        "topic": "Marine Microalgae: A Potential Reservoir for Crop Improvement",
        "is_featured": False,
    },
    {
        "name": "Dr. Suresh Govindan",
        "initials": "SG",
        "role": "Former Research Head",
        "institution": "N. Rama Varier Ayurveda Foundation, A VN Ayurveda Formulations Pvt. Ltd., Madurai",
        "topic": "Gut Microbiome: Health & Disease",
        "is_featured": False,
    },
]

DEFAULT_DATES = [
    {
        "title": "Abstract Submission Deadline",
        "date": "27 October 2025",
        "day": "27",
        "month": "October 2025",
        "time_text": "",
        "description": "Final date for submitting original research abstracts related to the conference theme.",
    },
    {
        "title": "Abstract Acceptance Intimation",
        "date": "28 October 2025",
        "day": "28",
        "month": "October 2025",
        "time_text": "",
        "description": "Selected presenters receive confirmation for oral or poster presentation participation.",
    },
    {
        "title": "Online Oral Presentation",
        "date": "29 October 2025",
        "day": "29",
        "month": "October 2025",
        "time_text": "",
        "description": "Oral presentation session for selected participants in virtual mode.",
    },
    {
        "title": "Registration Deadline",
        "date": "30 October 2025",
        "day": "30",
        "month": "October 2025",
        "time_text": "",
        "description": "Last date for participant registration and payment confirmation.",
    },
    {
        "title": "Main Conference and Poster Presentation",
        "date": "31 October 2025",
        "day": "31",
        "month": "October 2025",
        "time_text": "10:00 AM - 05:30 PM IST",
        "description": "Offline conference sessions, expert talks, poster presentation, certification, lunch, and delegate interaction at CVR Hall, School of Biological Sciences, MKU.",
    },
]

DEFAULT_LEADERS = [
    {"name": "Prof. Dr. M. Ramakrishnan", "role": "chief_patron", "role_label": "Chief Patron", "designation": "Registrar, Madurai Kamaraj University"},
    {"name": "Prof. Dr. S. Chandrasekaran", "role": "patron", "role_label": "Patron", "designation": "Chairperson, School of Biological Sciences, Madurai Kamaraj University"},
    {"name": "Prof. Dr. B. Mayilvaganan", "role": "convener", "role_label": "Convener", "designation": "Member of Convener Committee, Madurai Kamaraj University"},
    {"name": "Dr. M. Murugan", "role": "organising_secretary", "role_label": "Organising Secretary", "designation": "Department of Microbial Technology, School of Biological Sciences"},
    {"name": "Dr. N. Sivakumar", "role": "organising_secretary", "role_label": "Organising Secretary", "designation": "Department of Molecular Microbiology, School of Biotechnology"},
    {"name": "Dr. U. Ramesh", "role": "organising_secretary", "role_label": "Organising Secretary", "designation": "Department of Molecular Biology, School of Biological Sciences"},
]

DEFAULT_COMMITTEE = [
    "Dr. R. Sankar",
    "Dr. J. Rajendhran",
    "Dr. M. Rajan",
    "Dr. S. Ramasamy",
    "Dr. T. Jebasingh",
    "Dr. M. Jayalakshmi",
    "Dr. C. Amutha",
    "Dr. P. Gopal",
    "Prof. Dr. G. Kumaresan",
    "Dr. V. Shanmugiah",
    "Prof. K. Sivakumar",
    "Dr. B. Ashok Kumar",
    "Dr. Justin Thenmozhi",
    "M.Sc. Microbiology Students",
    "Ph.D. Scholars",
]


def content_map():
    return {item.key: item.content for item in SiteContent.objects.all()}


def cms_dates():
    items = list(ImportantDate.objects.filter(is_active=True))
    if not items:
        return DEFAULT_DATES
    return [
        {
            "title": item.title,
            "date": item.date.strftime("%d %B %Y"),
            "day": item.date.strftime("%d"),
            "month": item.date.strftime("%B %Y"),
            "time_text": item.time_text,
            "description": item.description,
        }
        for item in items
    ]


def cms_speakers():
    items = list(Speaker.objects.filter(is_active=True))
    if not items:
        return DEFAULT_SPEAKERS
    return items


def index(request):
    return render(request, "index.html")


def about(request):
    committee = list(CommitteeMember.objects.filter(is_active=True))
    leaders = [member for member in committee if member.role != "committee_member"]
    members = [member.name for member in committee if member.role == "committee_member"]
    return render(
        request,
        "about.html",
        {
            "content": content_map(),
            "leaders": leaders or DEFAULT_LEADERS,
            "committee_members": members or DEFAULT_COMMITTEE,
        },
    )


def important_dates(request):
    venue = VenueInfo.objects.filter(is_active=True).first()
    return render(
        request,
        "impdates.html",
        {"content": content_map(), "important_dates": cms_dates(), "venue": venue},
    )


def speakers(request):
    return render(
        request,
        "speakerslist.html",
        {"content": content_map(), "speakers": cms_speakers()},
    )


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        profession = request.POST.get("profession", "student")
        needs_accommodation = (
            profession == ConferenceRegistration.PROFESSION_TEACHER
            and request.POST.get("accommodation") == "yes"
        )
        fee_category, fee_amount = PRICING.get(profession, PRICING["student"])

        registration = ConferenceRegistration.objects.create(
            name=request.POST.get("name", "").strip(),
            email=request.POST.get("email", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            institution=request.POST.get("institution", "").strip(),
            profession=profession,
            needs_accommodation=needs_accommodation,
            fee_category=fee_category,
            fee_amount=fee_amount,
        )

        if needs_accommodation:
            return redirect(f"{reverse('accommodation')}?registration={registration.id}")

        messages.success(
            request,
            "Registration submitted successfully. Your details are now available in the admin panel.",
        )
        return redirect("register")

    return render(request, "register.html")


@require_http_methods(["GET", "POST"])
def accommodation(request):
    registration_id = request.GET.get("registration") or request.POST.get("registration_id")
    registration = get_object_or_404(
        ConferenceRegistration,
        id=registration_id,
        profession=ConferenceRegistration.PROFESSION_TEACHER,
        needs_accommodation=True,
    )

    if request.method == "POST":
        def posted_int(field_name, default=0):
            value = request.POST.get(field_name, "")
            return int(value) if value else default

        AccommodationBooking.objects.update_or_create(
            registration=registration,
            defaults={
                "room_type": request.POST.get("room_type", AccommodationBooking.ROOM_AC),
                "rooms_needed": posted_int("rooms_needed", 1),
                "checkin": request.POST.get("checkin"),
                "checkin_time": request.POST.get("checkin_time") or None,
                "checkout": request.POST.get("checkout"),
                "checkout_time": request.POST.get("checkout_time") or None,
                "guests": posted_int("guests", 1),
                "meal_preference": request.POST.get("meal_preference", "vegetarian"),
                "vegetarian_meals": posted_int("vegetarian_meals"),
                "non_vegetarian_meals": posted_int("non_vegetarian_meals"),
                "vegan_meals": posted_int("vegan_meals"),
                "breakfast_count": posted_int("breakfast_count"),
                "lunch_count": posted_int("lunch_count"),
                "dinner_count": posted_int("dinner_count"),
                "special_requests": request.POST.get("special_requests", "").strip(),
            },
        )
        messages.success(
            request,
            "Accommodation request submitted successfully. It is now available in the admin panel.",
        )
        return redirect("register")

    return render(request, "accommodation.html", {"registration": registration})

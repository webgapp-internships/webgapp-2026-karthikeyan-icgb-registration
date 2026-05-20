from datetime import date

from django.core.management.base import BaseCommand

from myapp.models import CommitteeMember, ImportantDate, SiteContent, Speaker, VenueInfo


class Command(BaseCommand):
    help = "Seed editable conference content for the admin control panel."

    def handle(self, *args, **options):
        contents = {
            "about_hero": (
                "About hero text",
                "ICGB 2026 is hosted within the School of Biological Sciences at Madurai Kamaraj University, a NAAC A++ accredited institution with a strong record in advanced biological research, postgraduate training, and scientific collaboration.",
            ),
            "institution_intro": (
                "Institution intro",
                "A concise view of the university, school, and department behind the conference.",
            ),
            "university_summary": (
                "University summary",
                "A public university known for postgraduate education, research culture, and academic access for students across social backgrounds.",
            ),
            "school_summary": (
                "School summary",
                "An eminent school supported through UGC programmes including DRS, DSA, CAS, CEGS, and NRCBS.",
            ),
            "department_summary": (
                "Department summary",
                "A department focused on research, teaching, mentoring, and advanced biological approaches in microbial and non-microbial systems.",
            ),
            "conference_focus": (
                "Conference focus",
                "The conference brings together students, research scholars, faculty, academicians, and industry participants for scientific sessions, presentations, and expert interaction.",
            ),
            "dates_hero": (
                "Dates page hero text",
                "Track registration, abstract submission, presentation dates, and the main conference day with a clear academic schedule.",
            ),
            "speakers_hero": (
                "Speakers page hero text",
                "The conference speaker programme brings together faculty and experts across chemistry, biotechnology, crop improvement, pharmaceutical discovery, and microbiome science.",
            ),
            "speakers_intro": (
                "Speakers intro",
                "A premium speaker directory with institution, designation, and lecture topic at a glance.",
            ),
        }

        for key, (label, content) in contents.items():
            SiteContent.objects.update_or_create(
                key=key,
                defaults={"label": label, "content": content},
            )

        VenueInfo.objects.update_or_create(
            name="CVR Hall",
            defaults={
                "location": "School of Biological Sciences, Madurai Kamaraj University",
                "help_phone": "+91 8838738559",
                "help_email": "imdmicconsbs@mkuniversity.ac.in",
                "details": "Main conference venue for offline scientific sessions and poster presentation.",
                "is_active": True,
            },
        )

        dates = [
            ("Abstract Submission Deadline", date(2025, 10, 27), "", "Final date for submitting original research abstracts related to the conference theme."),
            ("Abstract Acceptance Intimation", date(2025, 10, 28), "", "Selected presenters receive confirmation for oral or poster presentation participation."),
            ("Online Oral Presentation", date(2025, 10, 29), "", "Oral presentation session for selected participants in virtual mode."),
            ("Registration Deadline", date(2025, 10, 30), "", "Last date for participant registration and payment confirmation."),
            ("Main Conference and Poster Presentation", date(2025, 10, 31), "10:00 AM - 05:30 PM IST", "Offline conference sessions, expert talks, poster presentation, certification, lunch, and delegate interaction at CVR Hall, School of Biological Sciences, MKU."),
        ]
        for order, (title, event_date, time_text, description) in enumerate(dates, start=1):
            ImportantDate.objects.update_or_create(
                title=title,
                defaults={
                    "date": event_date,
                    "time_text": time_text,
                    "description": description,
                    "display_order": order,
                    "is_active": True,
                },
            )

        speakers = [
            ("Prof. Dr. K. Muruga Poopathi Raja", "KR", "Professor & Head", "Department of Chemistry, School of Physical Sciences, Central University of Kerala", "Design of Antiviral Peptides to Combat SARS-CoV-2", True),
            ("Dr. R. Shyam Kumar", "RS", "Professor & Head", "Department of Biotechnology, Kamaraj College of Engineering and Technology, Madurai", "Bioprospecting Lichens: Discovering New Leads for Pharmaceuticals and Beyond", False),
            ("Dr. S. Kathiresan", "SK", "Professor", "Department of Biotechnology, School of Integrative Biology, Central University of Tamil Nadu", "Marine Microalgae: A Potential Reservoir for Crop Improvement", False),
            ("Dr. Suresh Govindan", "SG", "Former Research Head", "N. Rama Varier Ayurveda Foundation, A VN Ayurveda Formulations Pvt. Ltd., Madurai", "Gut Microbiome: Health & Disease", False),
        ]
        for order, (name, initials, role, institution, topic, featured) in enumerate(speakers, start=1):
            Speaker.objects.update_or_create(
                name=name,
                defaults={
                    "initials": initials,
                    "role": role,
                    "institution": institution,
                    "topic": topic,
                    "display_order": order,
                    "is_featured": featured,
                    "is_active": True,
                },
            )

        leaders = [
            ("Prof. Dr. M. Ramakrishnan", "chief_patron", "Registrar, Madurai Kamaraj University"),
            ("Prof. Dr. S. Chandrasekaran", "patron", "Chairperson, School of Biological Sciences, Madurai Kamaraj University"),
            ("Prof. Dr. B. Mayilvaganan", "convener", "Member of Convener Committee, Madurai Kamaraj University"),
            ("Dr. M. Murugan", "organising_secretary", "Department of Microbial Technology, School of Biological Sciences"),
            ("Dr. N. Sivakumar", "organising_secretary", "Department of Molecular Microbiology, School of Biotechnology"),
            ("Dr. U. Ramesh", "organising_secretary", "Department of Molecular Biology, School of Biological Sciences"),
        ]
        for order, (name, role, designation) in enumerate(leaders, start=1):
            CommitteeMember.objects.update_or_create(
                name=name,
                defaults={"role": role, "designation": designation, "display_order": order, "is_active": True},
            )

        members = [
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
        for offset, name in enumerate(members, start=20):
            CommitteeMember.objects.update_or_create(
                name=name,
                defaults={"role": "committee_member", "display_order": offset, "is_active": True},
            )

        self.stdout.write(self.style.SUCCESS("Conference content seeded for admin editing."))

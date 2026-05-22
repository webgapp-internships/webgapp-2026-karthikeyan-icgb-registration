from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index.html", views.index, name="index_html"),
    path("about/", views.about, name="about"),
    path("about.html", views.about, name="about_html"),
    path("dates/", views.important_dates, name="important_dates"),
    path("impdates.html", views.important_dates, name="important_dates_html"),
    path("speakers/", views.speakers, name="speakers"),
    path("speakerslist.html", views.speakers, name="speakers_html"),
    path("register/", views.register, name="register"),
    path("register.html", views.register, name="register_html"),
]

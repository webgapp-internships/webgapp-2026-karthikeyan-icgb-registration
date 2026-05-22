from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def important_dates(request):
    return render(request, "impdates.html")


def speakers(request):
    return render(request, "speakerslist.html")


def register(request):
    return render(request, "register.html")

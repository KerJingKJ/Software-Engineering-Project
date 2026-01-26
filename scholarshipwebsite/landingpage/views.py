from django.shortcuts import render
from django.http import HttpResponse
from committee.models import Scholarship


def index(response):
    scholarships = Scholarship.objects.all()
    return render(response, "landingpage/landing.html", {
        'scholarships': scholarships
    })
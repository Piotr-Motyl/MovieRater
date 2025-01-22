from django.contrib import admin
from .models import Movie, AdditionalInfo, Review

admin.site.register(Movie)
admin.site.register(AdditionalInfo)
admin.site.register(Review)

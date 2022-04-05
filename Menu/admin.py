from django.contrib import admin

from .models import librarian, book

# Register your models here.
admin.site.register(book)
admin.site.register(librarian)

from django.contrib import admin
from .models import Ticket, Status

admin.site.register(Ticket)
admin.site.register(Status)
from django.contrib import admin
from .models import Event , TicketType , Booking , BookingItem
# Register your models here.

admin.site.register(Event)
admin.site.register(TicketType)
admin.site.register(Booking)
admin.site.register(BookingItem)
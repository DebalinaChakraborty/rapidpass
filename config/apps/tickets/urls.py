from django.urls import path
from .views import CreateBookingAPIView

urlpatterns = [
    path('bookings/', CreateBookingAPIView.as_view()),
]
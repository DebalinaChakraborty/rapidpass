from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.tickets.services.booking_service import BookingService

# Create your views here.
User = get_user_model()

class CreateBookingAPIView(APIView):

    def post(self, request):
        user = User.objects.first()
        if not user:
            return Response(
                {"error": "No user found. Please create a user first."},
                status=status.HTTP_400_BAD_REQUEST
            )
        items = request.data.get('items', [])

        try:
            booking = BookingService.create_booking(user, items)

            return Response(
                {
                    "booking_id": booking.id,
                    "status": booking.status,
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
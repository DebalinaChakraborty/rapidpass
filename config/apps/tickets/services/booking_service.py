from django.db import transaction
from django.core.exceptions import ValidationError

from apps.tickets.models import TicketType, Booking, BookingItem

class BookingService:

    @staticmethod
    def create_booking(user, items_data):
        """
        items_data = [
            {
                "ticket_type_id": 1,
                "quantity": 2
            }
        ]

        """
        with transaction.atomic():
            booking = Booking.objects.create(user=user, status='PENDING')

            for item in items_data:

                ticket_type = (TicketType.objects
                               .select_for_update()
                               .get(id=item["ticket_type_id"]))

                quantity_requested = item["quantity"]

                if ticket_type.quantity_available < quantity_requested:
                    raise ValidationError(f"Not enough tickets available for {ticket_type.name}")

                ticket_type.quantity_available -= quantity_requested
                ticket_type.save()

                BookingItem.objects.create(
                    booking=booking,
                    ticket_type=ticket_type,
                    quantity=quantity_requested
                )

            booking.status = 'CONFIRMED'
            booking.save()

        return booking
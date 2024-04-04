from django.urls import path
from .views import *


urlpatterns = [
    path('tickets/', TicketList.as_view(), name='tickets'),
    path('event/', AddEvents.as_view(), name='add-events'),
    path('list_event/', EventsList.as_view(), name='events-list'),
    path('list_event/<int:event_id>', EventsList.as_view(), name='event-detail'),
    path('update_event/<int:event_id>', EventsUpdateView.as_view(), name='update-event'),
    path('bookings/', BookingAPIView.as_view(), name='booking'),
    path('all_bookings/', BookingDetailView.as_view(), name='all-booking'),
]
from django.urls import path
from .views import *


urlpatterns = [
    path('tickets/', TicketList.as_view(), name='tickets'),
    path('event/', AddEvents.as_view(), name='add-events'),
    path('listevent/', EventsList.as_view(), name='events-list'),
    path('listevent/<int:event_id>', EventsList.as_view(), name='event-detail'),
    path('bookings/', BookingAPIView.as_view(), name='booking'),
    path('all_bookings/', BookingDetailView.as_view(), name='all-booking'),
]
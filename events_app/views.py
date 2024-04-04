from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EventSerializer, TicketsSerializer, BookingSerializer
from django.http import JsonResponse
from configuration import message, constants
from .models import *
from .permissions import IsOrganizer, IsUser, IsCustomer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .tasks import send_email_on_booking, send_email_on_update_event
from .logger import logger


class TicketList(APIView):
    permission_classes = [IsOrganizer]
    def post(self,request):
        try:
            ticket_serializer = TicketsSerializer(data=request.data)            
            if ticket_serializer.is_valid():
                ticket_serializer.save()
                response = {
                    constants.MESSAGE: message.TICKETS_ADDED,
                    constants.STATUS: status.HTTP_201_CREATED
                }
                return Response(response)
            else:
                error_response = {constants.MESSAGE: message.BAD_REQUEST, constants.STATUS: status.HTTP_400_BAD_REQUEST}
                return Response(error_response)
                
        except Exception as error:
            print('Error in add tickets: ', error)
            error_response = {
                constants.MESSAGE: message.INTERNAL_SERVER_ERROR,
                constants.STATUS: status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(error_response)

class AddEvents(APIView):
    permission_classes = [IsOrganizer]
    def post(self,request):
        try:
            request.data['organizer'] = request.user.id
            event_serializer = EventSerializer(data=request.data)
            if event_serializer.is_valid():
                print('1')
                event = event_serializer.save()
                tickets_data = request.data.get('ticket_type',[])
                for ticket_id in tickets_data:
                    ticket = Tickets.objects.get(id=ticket_id)
                    event.ticket_type.add(ticket)
                response = {
                    constants.MESSAGE: message.EVENT_CREATED,
                    "status": status.HTTP_200_OK
                }
                return Response(response)
            else:
                print(event_serializer.errors)
                error_response = {"status": status.HTTP_400_BAD_REQUEST, constants.MESSAGE: message.BAD_REQUEST}
                return Response(error_response)
                
        except Exception as error:
            print('Error in add events: ', error)
            error_response = {
                constants.MESSAGE: message.INTERNAL_SERVER_ERROR,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(error_response)

# To View All Events
class EventsList(APIView):
    permission_classes = [IsUser]
    def get(self,request,event_id=None):
        try:
            if event_id is not None:
                event = Events.objects.filter(pk=event_id,active=True)
                if event:
                    event_serializer = EventSerializer(event,many=True)
                    return Response({"status":status.HTTP_200_OK, constants.MESSAGE:message.EVENTS_FETCHED, constants.DATA: event_serializer.data})
                else:
                    return Response({"status": status.HTTP_404_NOT_FOUND, "message": message.EVENT_NOT_FOUND})
            else:
                all_events = Events.objects.filter(active=True)
                event_serializer = EventSerializer(all_events, many=True)
                return Response({"status":status.HTTP_200_OK, constants.MESSAGE:message.EVENTS_FETCHED, constants.DATA: event_serializer.data})
        except Exception as error:
            print('Error in get events: ', error)
            error_response = {
                constants.MESSAGE: message.INTERNAL_SERVER_ERROR,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(error_response)

    def put(self,request,event_id):
        try:
            event = Events.objects.get(pk=event_id)
            if event:
                event_serializer = EventSerializer(event,data=request.data,partial=True)
                if event_serializer.is_valid():
                    event_serializer.save()
                    result = send_email_on_update_event.delay(request.data)
                return Response({"status":status.HTTP_200_OK, constants.MESSAGE:message.EVENT_UPDATED})
            else:
                return Response({"status": status.HTTP_404_NOT_FOUND, "message": message.EVENT_NOT_FOUND})
        except:
            error_response = {
                constants.MESSAGE: message.INTERNAL_SERVER_ERROR,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(error_response)

class BookingAPIView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request):
        event_id = request.data.get('event')
        try:
            current_capacity = Events.objects.get(pk = event_id)
        except Events.DoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND, "message": message.EVENT_NOT_FOUND})
        
        available_seats = current_capacity.capacity
        no_of_seats = request.data['no_of_seats']

        if no_of_seats > available_seats:
            return Response({constants.MESSAGE: message.NO_OF_SEATS, constants.STATUS:status.HTTP_403_FORBIDDEN})

        serializer = BookingSerializer(data=request.data, context={'request': request})

        updated_capacity = available_seats - no_of_seats
        current_capacity.capacity = updated_capacity
        current_capacity.save()
        if serializer.is_valid():
            serializer.save()
            result = send_email_on_booking.delay(request.user.first_name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        bookings = Booking.objects.filter(customer=request.user)
        self.check_object_permissions(request, bookings)

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated,IsOrganizer]
    def get(self,request):
        bookings = Booking.objects.filter(event__organizer=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework import serializers
from .models import *
from user_auth.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.first_name',read_only=True)
    ticket_type_names = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Events
        fields = '__all__'
    
    def get_ticket_type_names(self,obj):
        return [ticket.type for ticket in obj.ticket_type.all()]

class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = ['customer', 'event', 'transaction_amt', 'status', 'ticket_type', 'no_of_seats']

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)
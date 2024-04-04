from django.db import models
from user_auth.models import Customer


TICKET_TYPE = [
    ("VIP","VIP"),
    ("Executive", "Executive"),
    ("General", "General")
]

class Tickets(models.Model):    
    type = models.CharField(max_length=50, choices=TICKET_TYPE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.type
    
class Events(models.Model):
    organizer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100, null=False)
    capacity = models.IntegerField()
    date = models.DateField()
    venue = models.CharField(max_length=1000,null=False)
    ticket_type = models.ManyToManyField(Tickets,related_name='events')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.event_name

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    event = models.ForeignKey(Events, on_delete = models.CASCADE)
    no_of_seats = models.IntegerField(null=True)
    transaction_amt = models.FloatField(null=True)
    ticket_type = models.CharField(max_length=100,null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.customer.first_name + " " + self.customer.last_name
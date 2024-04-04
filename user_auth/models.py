from django.db import models
from django.contrib.auth.models import AbstractUser


CUST_TYPE = (
    (True, "Organizer"),
    (False, "User"),
)

class Customer(AbstractUser):
    cust_type = models.BooleanField(choices= CUST_TYPE, default=False)
    
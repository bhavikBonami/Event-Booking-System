# Generated by Django 5.0.3 on 2024-04-03 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0004_booking_no_of_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='ticket_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

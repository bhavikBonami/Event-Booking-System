from celery import shared_task
from django.conf import settings
# from .logger import logger
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def send_email_on_booking(name):
    logger.info('Sending email for booking:')
    return f'Booking Successful for {name}'
    
@shared_task
def send_email_on_update_event(event):
    logger.info(f'Sending email for updating event: {event}')
    return f'Some changes in your booked event here are the details: {event}'

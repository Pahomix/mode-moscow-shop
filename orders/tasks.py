from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order #. {order.id}'
    message = f'{order.full_name}, \n\n Заказ успешно размещен. Ваш ID заказа {order.id}'
    mail_sent = send_mail(subject, message, 'modemoscowsup@gmail.com', [order.email])
    
    return mail_sent
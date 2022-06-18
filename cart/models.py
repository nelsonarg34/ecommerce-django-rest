from django.db import models

from order.models import Order, OrderDetail


class Cart(models.Model):
    order = models.ForeignKey(Order, related_name='cart_order', on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart {} - Order: {}".format(self.id, self.order.id)


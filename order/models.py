import requests
from django.db import models
from django.conf import settings
from product.models import Product

class Order(models.Model):
    PENDING_STATE = "p"
    COMPLETED_STATE = "c"
    CANCELLED_STATE = "x"

    ORDER_CHOICES = (
        (PENDING_STATE, "pending"),
        (COMPLETED_STATE, "completed"),
        (CANCELLED_STATE, "cancelled")
        )
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="order", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ORDER_CHOICES, default=PENDING_STATE)
    is_paid = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_order(buyer, status, is_paid=False):
        order = Order()
        order.buyer = buyer
        order.status = status
        order.is_paid = is_paid
        order.save()
        return order

    @property
    def get_total(self):
        order_items = self.order_items.all()
        total = 0
        for item in order_items:
            total = total + item.get_order_item_total
        return total

    @property
    def get_total_usd(self):
        total_usd = None
        try:
            response = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales').json()
            for d  in response:
                if d['casa']['nombre'] == "Dolar Blue":
                    usd_blue = d['casa']['compra']
            order_items = self.order_items.all()
            total = 0
            for item in order_items:
                total_arg = total + item.get_order_item_total
            total_usd = round(total_arg / float(usd_blue.replace(',','.')), 2)

            return total_usd

        except:

            return total_usd

    def __str__(self):
        return "Order {} - Buyer: {}".format(self.id, self.buyer)
    
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, related_name="product_order", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_order_item(order, product, quantity):
        order_item = OrderDetail()
        order_item.order = order
        order_item.product = product
        order_item.quantity = quantity
        order_item.save()
        return order_item

    @property
    def get_order_item_total(self):
        price = self.product.price
        quantity = self.quantity
        total = price * quantity
        return total

    def __str__(self):
        return "Order: {} - Product: {}".format(self.order, self.product)
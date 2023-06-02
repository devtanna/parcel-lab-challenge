from django.db import models


class Carrier(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Address(models.Model):
    address = models.TextField()

    def __str__(self):
        return self.address


class Article(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Shipment(models.Model):
    tracking_number = models.CharField(max_length=255)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    sender_address = models.ForeignKey(
        Address, 
        related_name='sender_shipments', 
        on_delete=models.CASCADE
    )
    receiver_address = models.ForeignKey(
        Address, 
        related_name='receiver_shipments', 
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.tracking_number
from django.db import models

# Create your models here.

# class Delivery(models.Model):
#     DELIVERY_TYPE_CHOICES = [
#         ('dispatch', 'Dispatch'),
#         ('bus', 'Bus'),
#     ]

#     pickup_name = models.CharField(max_length=100)
#     pickup_location = models.CharField(max_length=255)
#     pickup_number = models.CharField(max_length=15)
#     dropoff_location = models.CharField(max_length=255)
#     dropoff_name = models.CharField(max_length=100)
#     dropoff_number = models.CharField(max_length=15)
#     items_worth = models.DecimalField(max_length=10, decimal_places=2)
#     item_parcel_name = models.CharField(max_length=100)
#     delivery_type = models.CharField(max_length=10, choices=DELIVERY_TYPE_CHOICES)
#     weight = models.DecimalField(max_digits=10, decimal_places=2)  # Add weight field

#     def calculate_total_cost(self):
#         if self.delivery_type == 'dispatch':
#             shipping_cost = 3000
#         else:
#             shipping_cost = 8000

#         total_cost = self.items_worth + self.weight * 100 + shipping_cost
#         return total_cost

#     def save(self, *args, **kwargs):
#         self.total_cost = self.calculate_total_cost()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.pickup_name} to {self.dropoff_name} ({self.delivery_type})"


from django.db import models

class Delivery(models.Model):
    DELIVERY_TYPE_CHOICES = [
        ('dispatch', 'Dispatch'),
        ('bus', 'Bus'),
    ]

    pickup_name = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=255)
    pickup_number = models.CharField(max_length=15)
    dropoff_location = models.CharField(max_length=255)
    dropoff_name = models.CharField(max_length=100)
    dropoff_number = models.CharField(max_length=15)
    items_worth = models.DecimalField(max_digits=10, decimal_places=2)
    item_parcel_name = models.CharField(max_length=100)
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_TYPE_CHOICES, default='dispatch')
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def calculate_total_cost(self):
        shipping_cost = 1500 if self.delivery_type == 'dispatch' else 3500
        return (self.items_worth / 2) + (self.weight * 100) + shipping_cost

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pickup_name} to {self.dropoff_name} ({self.delivery_type})"

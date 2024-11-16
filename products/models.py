from django.db import models
from cloudinary.models import CloudinaryField
from uuid import uuid4

# Create your models here.
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.UUIDField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    unit_of_measurement = models.CharField(max_length=20)
    perishable = models.BooleanField()
    expiration_date = models.DateField()
    image = CloudinaryField('image', folder="gofoods_product_images", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
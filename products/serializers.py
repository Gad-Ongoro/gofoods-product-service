from rest_framework import serializers
from . import models

# product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'
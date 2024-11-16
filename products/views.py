from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from . import models, serializers
from django.core.cache import cache

# Create your views here.
# product view
class ProductCreateView(generics.CreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        new_product = serializer.save(user=self.request.user)
        cache.delete('ProductListView_cache')
        return new_product

class ProductListView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_cache_key(self):
        return f"ProductListView_cache"
    
    def list(self, request, *args, **kwargs):
        cache_key = self.get_cache_key()
        products = cache.get(cache_key)

        if not products:
            products = self.get_queryset().all()
            cache.set(cache_key, products, timeout=60*15)
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        return queryset

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Product.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        cache.delete('ProductListView_cache')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        cache.delete('ProductListView_cache')
        super().perform_destroy(instance)
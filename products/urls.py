from django.urls import path
from  . import views

urlpatterns = [
    path('products/create/', views.ProductCreateView.as_view(), name='Product Create'),
    path('products/', views.ProductListView.as_view(), name='Product List'),
    path('products/<uuid:pk>/', views.ProductDetailView.as_view(), name='Product Detail'),
]

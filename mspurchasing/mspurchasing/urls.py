from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from mspurchasingapp.views import ProductViewSet, PurchaseOrderViewSet, VendorViewSet, search_by_product_name, search_by_vendor_name, ProductByNameView, search_by_order_name


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'purchase-orders', PurchaseOrderViewSet)
router.register(r'vendors', VendorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls), name='home'),
    path('products/<int:pk>/', ProductViewSet.as_view(
        {'get': 'retrieve', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='product-detail'),
    path('api/search-by-product-name/', search_by_product_name,
         name='search-by-product-name'),

    path('product/<str:name>/',
         ProductByNameView.as_view(), name='product-by-name'),
    path('purchase-orders/<int:pk>/', PurchaseOrderViewSet.as_view(
        {'get': 'retrieve', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='purchaseorder-detail'),
    path('api/search-by-vendor-name/', search_by_vendor_name,
         name='search-by-vendor-name'),

    path('api/search-by-order-name/', search_by_order_name,
         name='search-by-order-name'),

    path('vendors/<int:pk>/', VendorViewSet.as_view(
        {'get': 'retrieve',  'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='vendor-detail'),
]

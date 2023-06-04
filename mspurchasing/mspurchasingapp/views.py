from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from rest_framework import viewsets, response
from .models import Product, PurchaseOrder, Vendor
from .serializers import ProductSerializer, PurchaseOrderSerializer, VendorSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=201)
            else:
                return response.Response(serializer.errors, status=400)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=500)

    def get_object(self):
        try:
            return super().get_object()
        except ObjectDoesNotExist:
            raise response.Response(
                {"detail": "Product not found."}, status=404)

    def retrieve(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            serializer = ProductSerializer(product)
            return response.Response(serializer.data, status=200)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=500)

    def destroy(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            product.delete()
            return response.Response(status=204)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=500)

    def update(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=200)
            else:
                return response.Response(serializer.errors, status=400)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        try:
            return super().get_object()
        except ObjectDoesNotExist:
            raise response.Response(
                {"detail": "Purchase Order not found."}, status=404)

    def retrieve(self, request, *args, **kwargs):
        try:
            purchase_order = self.get_object()
            vendor = get_object_or_404(Vendor, pk=purchase_order.vendor_id)
            vendor_serializer = VendorSerializer(vendor)
            purchase_order_data = PurchaseOrderSerializer(purchase_order).data
            purchase_order_data['vendor'] = vendor_serializer.data['name']
            print('Purchase Order data', purchase_order_data)
            return response.Response(purchase_order_data, status=200)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=500)

    def destroy(self, request, *args, **kwargs):
        try:
            purchase_order = self.get_object()
            purchase_order.delete()
            return response.Response(status=204)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=500)

    def update(self, request, *args, **kwargs):
        try:
            purchase_order = self.get_object()
            serializer = PurchaseOrderSerializer(
                purchase_order, data=request.data, partial=True)  # Add partial=True to allow partial updates
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=200)
            else:
                return response.Response(serializer.errors, status=400)
        except Exception as e:
            print(e)
            return response.Response({"detail": str(e)}, status=500)

    def create(self, request, *args, **kwargs):
        try:
            serializer = PurchaseOrderSerializer(data=request.data)
            # Validate the serializer and raise an exception if it's not valid
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(serializer.data, status=201)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_object(self):
        try:
            return super().get_object()
        except ObjectDoesNotExist:
            raise response.Response(
                {"detail": "Vendor not found."}, status=404)

    def retrieve(self, request, *args, **kwargs):
        try:
            vendor = self.get_object()
            serializer = VendorSerializer(vendor)
            return response.Response(serializer.data, status=200)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=500)

    def destroy(self, request, *args, **kwargs):
        try:
            vendor = self.get_object()
            vendor.delete()
            return response.Response(status=204)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=500)

    def update(self, request, *args, **kwargs):
        try:
            vendor = self.get_object()
            # Add partial=True to allow partial updates
            serializer = VendorSerializer(
                vendor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=200)
            else:
                return response.Response(serializer.errors, status=400)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=500)

    def create(self, request, *args, **kwargs):
        try:
            serializer = VendorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=201)
            else:
                return response.Response(serializer.errors, status=400)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


def search_by_product_name(request):
    if request.method == 'GET':
        # Get the name parameter from the query string
        name = request.GET.get('name', '')

        # Perform the search query
        products = Product.objects.filter(name__icontains=name)

        # Serialize the products and return as JSON response
        data = [{'name': product.name, 'id': product.id, 'cost': product.cost, 'favorite': product.favorite, 'responsible': product.responsible, 'product_type': product.product_type}
                for product in products]
        return JsonResponse(data, safe=False)


def search_by_vendor_name(request):
    if request.method == 'GET':
        # Get the name parameter from the query string
        name = request.GET.get('name', '')

        # Perform the search query
        vendors = Vendor.objects.filter(name__icontains=name)

        # Serialize the vendors and return as JSON response
        data = [{'name': vendor.name, 'id': vendor.id, 'related_company': vendor.related_company, 'address_type': vendor.address_type,  'street': vendor.street, 'city': vendor.city, 'state': vendor.state, 'country': vendor.country, 'state': vendor.state, }
                for vendor in vendors]
        return JsonResponse(data, safe=False)


def search_by_order_name(request):
    order_name = request.GET.get('order', '')
    orders = PurchaseOrder.objects.filter(
        order_reference__name__icontains=order_name)

    # Convert queryset to a list of dictionaries, excluding the source_document field
    orders_data = [model_to_dict(
        order, exclude=['source_document']) for order in orders]

    return JsonResponse(orders_data, safe=False)


class ProductByNameView(APIView):
    def get(self, request, name):
        try:
            product = get_object_or_404(Product, name=name)
            serializer = ProductSerializer(product)
            return response.Response(serializer.data, status=200)
        except Product.DoesNotExist:
            return response.Response({"detail": "Product not found."}, status=404)
        except Exception as e:
            return response.Response({"detail": str(e)}, status=500)

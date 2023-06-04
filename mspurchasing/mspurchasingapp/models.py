from django.db import models


class Product(models.Model):
    favorite = models.CharField(max_length=255)
    name = models.CharField(max_length=255, unique=True)
    internal_reference = models.CharField(max_length=255)
    responsible = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    product_category = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    quantity_on_hand = models.IntegerField()
    forecasted_quantity = models.IntegerField()
    activity_exception_decoration = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    priority = models.CharField(max_length=255)
    order_reference = models.OneToOneField(
        Product, on_delete=models.CASCADE, to_field='name', unique=True)
    vendor = models.ForeignKey(
        'Vendor', on_delete=models.CASCADE, )
    purchase_representative = models.CharField(max_length=255)
    order_deadline = models.DateField()
    activities = models.CharField(max_length=255)
    source_document = models.FileField(
        upload_to='purchase_orders/source_document/', blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255)


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    is_company = models.BooleanField()
    related_company = models.CharField(max_length=255)
    address_type = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

class Products(models.Model):
    # Basic Fields
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='products'
    )
    
    # Product Details
    productname = models.CharField(
        max_length=150,
        verbose_name='Product Name'
    )
    productbrand = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name='Brand'
    )
    productcategory = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name='Category'
    )
    productinfo = models.TextField(
        null=True, 
        blank=True,
        verbose_name='Product Information'
    )
    
    # Media
    image = models.ImageField(
        null=True, 
        blank=True,
        upload_to='products/',
        default='products/placeholder.png'
    )
    
    # Metrics
    rating = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        null=True, 
        blank=True,
        default=0.00
    )
    numReviews = models.IntegerField(
        null=True, 
        blank=True, 
        default=0,
        verbose_name='Number of Reviews'
    )
    
    # Inventory
    price = models.DecimalField(
        max_digits=7, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    stockcount = models.IntegerField(
        null=True, 
        blank=True, 
        default=0,
        verbose_name='Stock Count'
    )
    
    # Timestamps
    createdAt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updatedAt = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Updated'
    )
    
    # Metadata
    current_time = "2025-06-08 23:09:48"
    current_user = "Gps-Gaurav"

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-createdAt']
        indexes = [
            models.Index(fields=['productname']),
            models.Index(fields=['productbrand']),
            models.Index(fields=['productcategory']),
        ]

    def __str__(self):
        return f"{self.productname} - {self.productbrand or 'No Brand'}"

    def save(self, *args, **kwargs):
        # Update timestamp before saving
        if not self.pk:  # New instance
            self.createdAt = timezone.now()
        self.updatedAt = timezone.now()
        super().save(*args, **kwargs)

    @property
    def get_timestamp(self):
        """Return current timestamp"""
        return self.current_time

    @property
    def get_current_user(self):
        """Return current user"""
        return self.current_user

    @property
    def image_url(self):
        """Return full image URL"""
        try:
            url = self.image.url
        except:
            url = '/images/placeholder.png'
        return url

    @property
    def in_stock(self):
        """Check if product is in stock"""
        return self.stockcount > 0

    def get_absolute_url(self):
        """Return absolute URL for product"""
        from django.urls import reverse
        return reverse('product-detail', args=[str(self._id)])

class Review(models.Model):
    
    
    """Model for product reviews"""
    product = models.ForeignKey(
        Products, 
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    name = models.CharField(max_length=200)
    rating = models.IntegerField(
        null=True, 
        blank=True, 
        default=0
    )
    comment = models.TextField(
        null=True, 
        blank=True
    )
    createdAt = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-createdAt']
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.name}\'s review of {self.product.productname}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    itemsPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    taxPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(default=datetime(2025, 6, 16, 20, 28, 5))
    updatedAt = models.DateTimeField(auto_now=True)
    createdBy = models.CharField(max_length=200, default="gps-rajput")
    updatedBy = models.CharField(max_length=200, default="gps-rajput")

    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        ordering = ['-createdAt']

class OrderItem(models.Model):
    product = models.ForeignKey('Products', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='items')
    productname = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    createdAt = models.DateTimeField(default=datetime(2025, 6, 16, 20, 28, 5))
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.qty} x {self.productname}"

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='shipping')
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    createdAt = models.DateTimeField(default=datetime(2025, 6, 16, 20, 28, 5))
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address}, {self.city}"
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='shipping')
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    createdAt = models.DateTimeField(default=datetime(2025, 6, 16, 20, 24, 49))
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address}, {self.city}"
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.address)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderItems')
    name = models.CharField(max_length=200)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=200, null=True, blank=True)  # store image url/path

    def __str__(self):
        return f"{self.qty} x {self.name}"
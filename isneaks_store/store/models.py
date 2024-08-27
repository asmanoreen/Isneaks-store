from django.db import models
from .model_utils import Auditable, BaseModel
from django.contrib.auth.models import User

# Create your models here.


class Category(Auditable, BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Branding(Auditable, BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Branding'

    def __str__(self):
        return self.name


class Product(Auditable, BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    branding = models.ForeignKey(
        Branding, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Product'

    def __str__(self):
        return self.name

    def default_image(self):
        image = self.productimage_set.first()
        if image:
            return image.image.url
        return None


class Size(Auditable, BaseModel):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Color(Auditable, BaseModel):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Review(Auditable, BaseModel):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Feedback(Auditable, BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'FeedBack'

    def __str__(self):
        return self.product.name


class ProductImage(Auditable, BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    class Meta:
        verbose_name_plural = 'Product Image'

    def __str__(self):
        return self.product.name


class Cart(Auditable, BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def add_item(self, product, quantity):
        cart_item, created = self.cartitem_set.get_or_create(
            product=product,
            defaults={
                'quantity': quantity,
            }
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        self.calculate_total()

    def remove_item(self, cart_item):
        cart_item.delete()
        self.calculate_total()

    def update_item_quantity(self, cart_item, quantity):
        cart_item.quantity = quantity
        cart_item.save()
        self.calculate_total()

    def calculate_total(self):
        self.total = sum(item.subtotal() for item in self.cartitem_set.all())
        self.save()


class CartItem(Auditable, BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def subtotal(self):
        return self.product.price * self.quantity


class ShipmentDetails(Auditable, BaseModel):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    Country = models.CharField(max_length=200)
    Address = models.CharField(max_length=200)
    Phone = models.CharField(max_length=200)
    Email = models.EmailField(blank=True, null=True)
    OrderNotes = models.CharField(max_length=200)


class Order(Auditable, BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderstatus = models.CharField(max_length=30, default="Order Processed")
    shipmentorder = models.ForeignKey(
        ShipmentDetails, on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Total = models.PositiveBigIntegerField()

    def __str__(self):
        return str(self.id)


class OrderItem(Auditable, BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def subtotal(self):
        return self.product.price * self.quantity


class banner(Auditable, BaseModel):
    image = models.ImageField(upload_to='banner/')
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    promotionaltext = models.CharField(max_length=300)

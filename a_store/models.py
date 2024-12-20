from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.conf import settings


if settings.ENVIRONMENT == 'production' or settings.POSTGRES_LOCALLY == True:
    from cloudinary.models import CloudinaryField
    

STATUS_CHOICE = (
    ("procesando", "Procesando"),
    ("enviado", "Enviado"),
    ("entregado", "Entregado"),
)

STATUS = (
    ("borrador", "Borrador"),
    ("inhabilitado", "Inhabilitado"),
    ("rechazado", "Rechazado"),
    ("en_revision", "En revisión"),
    ("publicado", "Publicado"),
)


RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

# Create your models here.

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat', alphabet='abcdefgh12345')
    title = models.CharField(max_length=100, default='Sneaker')
    description = models.CharField(max_length=100, default='lo mejor de lo mejor')
    detail = models.CharField(max_length=100, default='lomejor de lomejor')
    if settings.ENVIRONMENT == 'production' or settings.POSTGRES_LOCALLY == True:
        image = CloudinaryField(default='category.jpg')
    else:    
        image = models.ImageField(upload_to='category', default='category.jpg')
    
    class Meta:
        verbose_name_plural = 'Categories'
        
        
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height"50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    
    def get_absolute_url(self):
        return f'/category/{self.cid}'
    
    
class Tags(models.Model):
    pass
    
    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven', alphabet='abcdefgh12345')
    
    title = models.CharField(max_length=100, default='Nestify')
    if settings.ENVIRONMENT == 'production' or settings.POSTGRES_LOCALLY == True:
        image = CloudinaryField(default='vendor.jpg')
        cover_image = CloudinaryField(default='vendor.jpg')
    else:
        image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
        cover_image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
        
    description = models.TextField(null=True, blank=True, default='I am an Amazing Vendor')
    
    address = models.CharField(max_length=100, default='9 de julio, Mendoza')
    contact = models.CharField(max_length=100, default='+54 23134211')
    chat_resp_time = models.CharField(max_length=100, default='100')
    shipping_on_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='100')
    warranty_period = models.CharField(max_length=100, default='100')
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Vendors'
        
        
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height"50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
  

 
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20,  alphabet='abcdefgh12345')
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='product')
    
    title = models.CharField(max_length=100, default='Nike Air Force 1')
    if settings.ENVIRONMENT == 'production' or settings.POSTGRES_LOCALLY == True:
        image = CloudinaryField(default='product.jpg')
    else:
        image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    description = models.TextField(null=True, blank=True, default='This is the product')
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default='1.99')
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default='2.99')
    
    specifications = models.TextField(null=True, blank=True)
    
    tags = TaggableManager(blank=True)
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    
    product_status = models.CharField(choices=STATUS, max_length=20, default='en_revision')

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix='sku', alphabet='1234567890')
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    
    
    
    class Meta:
        verbose_name_plural = 'Products'
        
        
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height"50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_precentage(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return new_price
    
    
    def get_absolute_url(self):
        return f'/product/{self.pid}'

    
class ProductImages(models.Model):
    if settings.ENVIRONMENT == 'production' or settings.POSTGRES_LOCALLY == True:
        images = CloudinaryField(default='product.jpg')
    else:
        images = models.ImageField(upload_to="product-images", default='product.jpg')
        
    product = models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name_plural = 'Product Images'



class ProductSize(models.Model):
    SIZES = {
        "Camperas": (
            ("s", "S"),
            ("m", "M"),
            ("l", "L"),
            ("xl", "XL"),
            ("xxl", "XXL"),
        ),
        "Remeras": (
            ("s", "S"),
            ("m", "M"),
            ("l", "L"),
            ("xl", "XL"),
            ("xxl", "XXL"),
        ),
        "Buzos": (
            ("s", "S"),
            ("m", "M"),
            ("l", "L"),
            ("xl", "XL"),
            ("xxl", "XXL"),
        ),
        "Zapatillas": (
            ("36", "36"),
            ("37", "37"),
            ("38", "38"),
            ("39", "39"),
            ("40", "40"),
        ),
    }

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sizes")
    size = models.CharField(max_length=10)
    stock = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Validación: comprobar que el tamaño es válido para la categoría del producto
        category_name = self.product.category.title if self.product.category else None
        valid_sizes = dict(self.SIZES).get(category_name, [])
        if self.size not in dict(valid_sizes).keys():
            raise ValueError(f"Invalid size '{self.size}' for category '{category_name}'")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} - Size {self.size} (Stock: {self.stock})"


############################## CART, ORDER, ORDERITEMS AND ADDRESS ###########################


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    
    
    address = models.CharField(max_length=100, null=True, blank=True)
    number = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    level = models.CharField(max_length=100, null=True, blank=True)
    departament = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    
    price = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    saved = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    coupons = models.ManyToManyField('Coupon', blank=True)
    
    shipping_method = models.CharField(max_length=100, null=True, blank=True)
    tracking_id = models.CharField(max_length=100, null=True, blank=True)
    tracking_website_address = models.CharField(max_length=100, null=True, blank=True)
    
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default='procesando', blank=True, null=True)
    sku = ShortUUIDField(null=True, blank=True, unique=True, length=5, max_length=20, prefix='SKU', alphabet='1234567890')
    oid = ShortUUIDField(null=True, blank=True, unique=True, length=5, max_length=20, alphabet='1234567890')
    
    stripe_payment_intent = models.CharField(max_length=100, null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = 'Cart Order'


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    size = models.CharField(max_length=10, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default='1.99')
    total = models.DecimalField(max_digits=10, decimal_places=2, default='1.99')
    
    
    class Meta:
        verbose_name_plural = 'Cart Order Items'
        
        
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height"50" />' % {self.image})
    
    
    
    
    
################################### PRODUCT REVIEW, WISHLISTS, ADDRESSS  #############################
    
    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Product Reviews'
        
        
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name_plural = 'Wishlists'
        
        
    def __str__(self):
        return self.product.title
    


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    number = models.CharField(max_length=255, null=True, blank=True)
    level = models.CharField(max_length=255)
    departament = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    mobile = models.CharField(max_length=300, null=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Address'
        
        
        
        
        
class Coupon(models.Model):
    code =  models.CharField(max_length=50)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.code
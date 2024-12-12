import uuid

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
from django.utils import timezone
from ckeditor.fields import RichTextField




STATUS_ORDERS = (
    ('pending', 'pending'),
    ('delivered', 'delivered'),
    ('canceled', 'canceled'),
)




class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None):
        if not username:
            raise ValueError('User name is required')

        if not phone_number:
            raise ValueError('Users must have phone number')

        if not password:
            raise ValueError('Users must have password')

        user = self.model(username=username, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # SuperUser Section
    def create_superuser(self, username, phone_number, password):
        user = self.create_user(username, phone_number, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    regex_phone = RegexValidator(
        regex=r'^09\d{9}$',
        message='Enter a valid phone number like 09.....',

    )
    phone_number = models.CharField(max_length=11, unique=True, validators=[regex_phone])

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'users'
        ordering = ['-date_joined']
        get_latest_by = 'date_joined'


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True




class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        db_table = 'categories'
        ordering = ['-created_at']
        get_latest_by = 'created_at'



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
            super(Categories, self).save(*args, **kwargs)


    def __str__(self):
        return self.name




class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=1500)
    regex_phone = RegexValidator(
        regex=r'^09\d{9}$',
        message='شماره خودرا با فرمت صحیح وارد کنید, با 09 شروع شود و شامل 11 رقم باشد',
    )

    phone_number = models.CharField(max_length=11, unique=True, validators=[regex_phone])
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'supplier'
        verbose_name_plural = 'suppliers'
        db_table = 'suppliers'
        ordering = ['-created_at']
        get_latest_by = 'created_at'


    def __str__(self):
        return self.full_name




class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = RichTextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=0)
    is_suggestion = models.BooleanField(default=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        get_latest_by = 'created_at'
        verbose_name = 'product'
        verbose_name_plural = 'products'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
            super(Products, self).save(*args, **kwargs)



    def calculate_discount_percentage(self):
        if self.is_sale and self.sale_price < self.price:
            discount = (self.price - self.sale_price) / self.price * 100

            return round(discount, 0)



    def __str__(self):
        return self.name





class Orders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    regex_phone = RegexValidator(
        regex=r'^09\d{9}$',
        message='شماره خودرا با فرمت صحیح وارد کنید, با 09 شروع شود و شامل 11 رقم باشد',
    )
    phone_number = models.CharField(max_length=11, validators=[regex_phone])
    city = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=1500)
    postal_code = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_ORDERS, default='pending')
    shipped =models.BooleanField(default=False)
    date_shipped = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
        get_latest_by = 'created_at'
        verbose_name = 'order'
        verbose_name_plural = 'orders'


    def __str__(self):
        return self.full_name




class OrderItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'order_items'
        verbose_name = 'order item'
        verbose_name_plural = 'order items'


    def __str__(self):
        return self.order.full_name





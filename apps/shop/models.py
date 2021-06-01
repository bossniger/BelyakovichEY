from django.db import models
from django.urls import reverse


class Supplier(models.Model):
    name = models.CharField(max_length=40)
    agent = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.agent


class Supply(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supply_price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    delivery_date = models.DateField()
    quantity = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    supply = models.ForeignKey(Supply,null=True, on_delete=models.DO_NOTHING)
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/&Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


class SupplyItem(models.Model):
    supply = models.ForeignKey(Supply, related_name='item', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='supply_item', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class Bill(models.Model):
    supply = models.OneToOneField(Supply, on_delete=models.DO_NOTHING)
    products_cost = models.DecimalField(max_digits=100, decimal_places=2)
    discount = models.DecimalField(max_digits=100, decimal_places=2)
    customer = models.CharField(max_length=250)



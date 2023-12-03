from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse



CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear'), 
    ('MN', 'Men'), 
    ('WN', 'Wemen'), 
    ('KD', 'Kids'),
    ('SH', 'Shoes'),
    ('HM', 'Home'), 
    ('BG', 'Bage'),
    ('JL', 'Jewelry'),
    ('WT', 'WATCHES')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

CITY = (
    ('Sc', 'Select city'),
    ('Ha', 'Hama'),
    ('Dm', 'Damascus'),
    ('Al', 'Aleppo' ),
    ('Hm', 'Homs'), 
    ('Lt', 'Latakia'),
    ('Tr', 'Tartus' ),
    ('Dr', 'Daraa'),
    ('Su', 'Al-Suwayda'),
    ('Hs', 'Al-Hasakah'),
    ('Qm', 'Al-Qamishli'),
    ('Rq', 'Al-Raqqah'),
    ('Qu', 'Al-Qunaytirah'),
    ('Dz', 'Dayr al-Zawr'),
    ('Id', 'Idlib'),
)

COLOR_CHOICES = (
    ('RD', 'RED'),
    ('BL', 'BLUE'),
    ('GR', 'GREEN'),
)

SIZE_CHOICES = (
    ('S', 'SMALL'),
    ('L', 'LARG'),
    ('M', 'MEDIUM'),
    ('XL', 'XLARG'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("WMapp:product", kwargs={
            'slug': self.slug
        })
    
    def get_add_to_cart_url(self):
        return reverse("WMapp:add_to_cart", kwargs={
            'slug': self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse("WMapp:remove_from_cart", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
   
   
    '''
    1. Item added to cart
    2. Adding address
    3. Being delivered
    4. Received
    5. Refunds
    '''
    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= (self.coupon.amount*total)/100
        return total

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    city = models.CharField(max_length=2, choices=CITY)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.IntegerField()

    def __str__(self):
        return self.code
    
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return self.email

def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)

post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)

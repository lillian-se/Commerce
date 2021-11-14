from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORY_CHOISES = [
    ('fashion', 'Fashion'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ('sports', 'Sports'),
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('other', 'Other'),
]


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller")
    active = models.BooleanField(default=True)
    category = models.CharField(max_length=64, choices=CATEGORY_CHOISES)

    def __str__(self):
        return self.title


class Watchlist(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bidder')
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='bid_item')
    price = models.IntegerField()

    def __str__(self):
        return str(self.price)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user} says: {self.comment}"

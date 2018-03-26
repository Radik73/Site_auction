from django.db import models
from django.utils import timezone

# from model_utils.fields import StatusField
# from model_utils import Choices
from django.contrib.auth.models import User

# Create your models here.

STATUS_CHOICES = [
    ('Opened', 'opened'),
    ('Finished', 'finished'),
    ('Canceled', 'canceled')
]

class Lot(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True,upload_to='images/')
    start_date = models.DateTimeField(
            default=timezone.now)
    finish_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=10,
                              db_index=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def start(self):
        self.start_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Rate(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    time_rate = models.DateTimeField(
            default=timezone.now)
    sum_rate = models.IntegerField()

    def start(self):
        self.time_rate = timezone.now()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank_book = models.IntegerField()

    def __unicode__(self):
        return self.user
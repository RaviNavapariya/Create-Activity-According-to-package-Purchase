from django.db import models
from django.contrib.auth.models import User


# Create your Models here.


class Package(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField() 
    activity = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Package"
        verbose_name_plural = 'Packages'


class PurchasePackage(models.Model):
    name = models.ForeignKey(Package, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Activity(models.Model):
    name = models.CharField(max_length=10)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
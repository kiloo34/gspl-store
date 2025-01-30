from django.db import models
from django.utils.timezone import now

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_idr = models.DecimalField(default=0, max_digits=15, decimal_places=2)
    price_sgd = models.DecimalField(default=0, max_digits=15, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ProductManager()
    all_objects = models.Manager()

    SGD_EXCHANGE_RATE = 10000

    def save(self, *args, **kwargs):
        self.price_sgd = self.price_idr / self.SGD_EXCHANGE_RATE
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None

    class Meta:
        ordering = ["-created_at"]

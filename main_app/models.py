from django.db import models

class Category(models.Model):

    IS_ACTIVE_CHOICES = (
    (True, 'Active'),
    (False, 'Inactive'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(choices=IS_ACTIVE_CHOICES,default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'


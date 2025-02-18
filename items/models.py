from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from taggit.managers import TaggableManager


User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=20)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):

        return self.name
    
    class Meta:
        verbose_name_plural = "categories"


class Item(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_active": True}, related_name="items")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    price = models.FloatField(default=99.99)
    image = models.ImageField(default="default.jpg")
    active = models.BooleanField(default=True)
    description = models.TextField()
    tags = TaggableManager()
    quantities = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "items"
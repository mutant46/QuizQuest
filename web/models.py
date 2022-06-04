from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="category_images", blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return "%s" % self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

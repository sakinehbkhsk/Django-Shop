from django.db import models
from core.models import BaseModel
from django.urls import reverse

class Category(BaseModel):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('product:category_filter', args=[self.slug, ])



    
class Product(BaseModel):
    name = models.CharField(max_length=200)
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    price = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return self.name

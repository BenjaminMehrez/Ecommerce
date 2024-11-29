from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import *

class StaticSitemap(Sitemap):
    def items(self):
        return ['home']
    
    def location(self, item):
        return reverse(item)
    
    
    
    
class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()
    
    
    
class ProductpageSitemap(Sitemap):
    def items(self):
        return Product.objects.all()[:100]
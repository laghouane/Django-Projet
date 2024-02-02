from audioop import reverse
from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.
class ProduitInStockQuerySet(models.QuerySet):
    def in_stock(self):
        return self.filter(quantité__gt=0)

class Produit(models.Model):
    nom=models.CharField(max_length=200)
    quantité=models.IntegerField(default=0,help_text="Quantité en stock")
    prix=models.DecimalField(max_digits=6,decimal_places=2)
    description=models.TextField(default="",blank=True)
    date_creation=models.DateTimeField(auto_now_add=True)
    date_modification=models.DateTimeField(auto_now=True)
    image=models.ImageField()
    slug=models.SlugField()
    objects=models.Manager()
    in_stock=ProduitInStockQuerySet.as_manager()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_produits')

    def get_absolute_url(self):
        return reverse('produit:produit_detail',args=[self.id])

    class Meta: 
        ordering=['prix','nom']
        constraints=[
        models.CheckConstraint(check=models.Q(prix__gte=0),name='prix_non_negative')
    ]
        
    def __str__(self):
        return self.nom 

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.nom)
        return super().save(*args,**kwargs)

    @property
    def tva(self):
        return Decimal(.2)*self.prix
    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk':self.id})
    


class Categorie(models.Model):
    nom_C=models.CharField(max_length=100)
    produits=models.ManyToManyField('produit', related_name='categories')

    class Meta:
        verbose_name_plural='categories'
        ordering=['nom_C']
    def __str__(self):
        return self.nom_C


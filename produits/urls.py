from django.urls import path
from . import views
app_name='produits' #define application namespace
#domain.com/blog/...
urlpatterns=[
    path('' ,views.produit_list, name='produit_list'),
    path('<int:id>/',views.produit_detail,name='produit_detail'),
    path('<int:id>/produit/', views.post_produit, name='post_produit'),
]
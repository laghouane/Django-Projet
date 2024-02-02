from django.http import Http404
from django.shortcuts import get_object_or_404, render
from produits.forms import ProduitForm
from .models import Produit
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST

@require_POST
def post_produit(request,id):
    produit= get_object_or_404(Produit, id=id)
# A comment was posted
    form = ProduitForm(data=request.POST)
    if form.is_valid():
        produit = form.save()
    return render(request, 'produits/produit.html', {'produit': produit})

def produit_list(request):
    produit_list=list(Produit.objects.all())
# Pagination with 3 posts per page
    paginator = Paginator(produit_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
# If page_number is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
# If page_number is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)
    
    return render(request,'produits/list.html',{'products':products})

def produit_detail(request,id):
    products=Produit.objects.get(id)
    return render(request, 'produits/detail.html',{'products':products})
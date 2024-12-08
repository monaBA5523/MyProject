from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .forms import *


# Create your views here.


def home(request):
    category = Category.objects.filter(sub_cat=False)
    return render(request, 'home/home.html', {'category': category})


def all_products(request, slug=None, id=None):
    products = Product.objects.all()
    category = Category.objects.filter(sub_cat=False)
    if slug and id:
        data = Category.objects.get(slug=slug, id=id)
        products = products.filter(category=data)
    return render(request, 'home/products.html', {'products': products, 'category': category})


def product_details(request, id):
    product = get_object_or_404(Product,id=id)
    comments = product.comments.filter(parent__isnull=True)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product=product
            comment.user = request.user
            comment.save()
            return redirect('home:details', id=id)
        else:
            form = CommentForm()
            return render(request,'home/details.html', {'form': form, 'comments': comments,'product': product})

    product = Product.objects.get(id=id)
    similar = product.tags.similar_objects()[:5]
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True
    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        is_unlike = True
    if product.status != 'None':
        if request.method == 'POST':
            variant = Variants.objects.filter(product_variant_id=id)
            var_id = request.POST.get('select')
            variants = Variants.objects.get(id=var_id)
        else:
            variant = Variants.objects.filter(product_variant_id=id)
            variants = Variants.objects.get(id=variant[0].id)

        return render(request, 'home/details.html', {'product': product, 'variants': variants,
                                                     'variant': variant, 'similar': similar, 'is_like': is_like,
                                                     'is_unlike': is_unlike})
    else:
        return render(request, 'home/details.html', {'product': product, 'similar': similar,
                                                     'is_like': is_like, 'is_unlike': is_unlike})


def product_like(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
    else:
        product.like.add(request.user)
    return redirect(url)


def product_unlike(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    if product.unlike.filter(id=request.user.id).exists():
        product.unlike.remove(request.user)
    else:
        product.unlike.add(request.user)
    return redirect(url)

from django.shortcuts import render,redirect,get_object_or_404
from authentication.views import user_login
from Product.models import Category,Product
# Create your views here.


# home before login

def index_page(request):
    category = Category.objects.all().exclude(soft_delete = True),
    products = Product.objects.all().exclude(soft_delete = True)

    return render(request,'index.html',{'products':products,'category':category})



# home after login

def Home_page(request):
    if request.user.is_authenticated:
        category = Category.objects.all().exclude(soft_delete = True),
        products = Product.objects.all().exclude(soft_delete = True)

        return render(request,'home.html',{'products':products,'category':category})
    return redirect(user_login)


def product_detail(request,pk):
    if 'user' in request.session:
        product =get_object_or_404(Product,pk=pk)
        category = Category.objects.all()
        return render(request,'product-page.html',{'product':product,'category':category})
    return redirect(user_login)
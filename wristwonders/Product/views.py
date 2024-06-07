from django.shortcuts import render,redirect,get_object_or_404
from .models import Category,Product,product_image
from authentication.views import admin_login
from .forms import Add_category_form,Update_form,Product_Form,Product_Image_Form

# Create your views here.
def Category_list(request):
    if 'adminn' in request.session:
        
            category = Category.objects.all()
    
            return render(request,'category.html',{'category': category})
        
    return redirect(admin_login)

def add_category(request):
    if 'adminn' in request.session:
        
            if request.method == "POST":
                form = Add_category_form(request.POST)
                if form.is_valid:
                    form.save()
                    return redirect('Category')
            else:
                form = Add_category_form()
            return render(request,'add_category.html',{'form':form})

    return redirect(admin_login)


def edit_category(request,pk):
    if 'adminn' in request.session:
        instance = get_object_or_404(Category, id=pk)
        f = Update_form(instance=instance)
        if request.POST:
            fm = Update_form(request.POST,instance=instance)
            if fm.is_valid():
                fm.save()
                return redirect('Category')
            else:
                f = Update_form(instance=instance)
        return render(request,'edit-category.html',{'instance':instance,'f':f})
    return redirect(admin_login)


def delete_category(request,pk):
     if 'adminn' in request.session:
          instance = Category.objects.get(id=pk)
          instance.soft_delete = True
          instance.save()
          return redirect('Category')
     return redirect(admin_login)


def undo_category(request,pk):
    if 'adminn' in request.session:
        instance = Category.objects.get(id=pk)
        instance.soft_delete = False
        instance.save()
        return redirect('Category')
    return redirect(admin_login) 
   


# products view

    
def Product_list(request):
    if 'adminn' in request.session:
        products = Product.objects.all()
        return render(request,'product-list.html',{'products':products})
    return redirect(admin_login)


def Add_product(request):
    if 'adminn' in request.session:
        if request.method =='POST':
            product_form = Product_Form(request.POST,request.FILES)
            product_image_form =Product_Image_Form(request.POST,request.FILES)
            if product_form.is_valid() and product_image_form.is_valid():
                product = product_form.save()
                files = request.FILES.getlist('image')
                for f in files:
                    product_image.objects.create(product = product,image = f)
                return redirect(Product_list)
        else:
         
            product_form = Product_Form()
            product_image_form = Product_Image_Form()
        return render(request,'add-product.html',{'product_form':product_form,'product_image_form':product_image_form})




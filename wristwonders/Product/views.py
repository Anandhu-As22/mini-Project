from django.shortcuts import render,redirect,get_object_or_404
from .models import Category,Product,product_image
from authentication.views import admin_login
from .forms import Add_category_form,Update_form,Product_Form,ProductImageFormSet,Product_edit_form
import mimetypes
import os
from PIL import Image
from django.contrib import messages


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
                if form.is_valid():
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
        products = Product.objects.all().order_by('-last_update')
        
        return render(request,'product-list.html',{'products':products})
    return redirect(admin_login)


# def Add_product(request):
#    if 'adminn' in request.session:
#         if request.method == 'POST':
#             product_form = Product_Form(request.POST)
#             formset = ProductImageFormSet(request.POST,request.FILES)
            
#             if product_form.is_valid() and formset.is_valid():
#                 product = product_form.save()
#                 images = formset.save(commit=False)
                
#                 for img in images:
#                     img.product = product
#                     img.save()
#                 return redirect(Product_list)
#         else:
#             product_form = Product_Form()
#             formset = ProductImageFormSet()
#         return render(request, 'add-product.html', {'product_form': product_form, 'formset': formset})

def Add_product(request):
    storage = messages.get_messages(request)
    storage.used = True

    valid_image_extensions = {'.jpg','.png','.jpeg','.webp'}
    valid_mime = {'image/jpeg','image/jpg','image/png','image/webp'}
    image_errors = []

    if 'adminn' in request.session:
        if request.method == 'POST':
            product_form = Product_Form(request.POST)
            
            images = request.FILES.getlist('images')
            for image in images:
                print("hii")
                print(image)
                _, ext = os.path.splitext(image.name.lower())
                if ext not in valid_image_extensions:
                    image_errors.append(f"Invalid file extension: {ext}. Allowed extensions are {', '.join(valid_image_extensions)}.")

                mime_type, _ = mimetypes.guess_type(image.name)
                # if mime_type not in valid_mime:
                #     image_errors.append(f"Invalid MIME type: {mime_type}. Allowed MIME types are {', '.join(valid_mime)}.")
            
            if image_errors: 
                for error in image_errors:
                    messages.error(request,error)
                return render(request, 'add-product.html', {'product_form': product_form})

            
            if product_form.is_valid():
                price = product_form.cleaned_data['price']

                if price < 0:
                    product_form.add_error('price','price must be greater than zero')

                quantity = product_form.cleaned_data['stock']
                if quantity <  0:
                    product_form.add_error('stock','stock must be greater than zero')

                if price >= 0 and quantity >=0:
                    product = product_form.save()
                    # varients = formset.save(commit=False)

                    # for varient in varients:
                    #     varient.product =product
                    #     varient.save()

                    for img in images:
                        print(img)
                        
                        product_image.objects.create(product = product,image = img)
                    return redirect(Product_list)
                
        else:
            product_form = Product_Form()

           
            
        return render(request, 'add-product.html', {'product_form': product_form})
    return redirect(admin_login)






# def view_image(request,pk):
#     if 'adminn' in request.session:
#         product = get_object_or_404(Product,pk = pk)
        

def update_product(request, pk):
    if 'adminn' in request.session:
        product = get_object_or_404(Product, id=pk)
        existing_images = product.images.all()
        # print(existing_images)  

        if request.method == 'POST':
            productform = Product_edit_form(request.POST, instance=product)
            images = request.FILES.getlist('images')
            formset = ProductImageFormSet(request.POST,request.FILES,instance=product)

            if productform.is_valid() and formset.is_valid():
                price = productform.cleaned_data['price']
                quantity = productform.cleaned_data['stock']

                if price < 0:
                    productform.add_error('price', 'Price must be greater than zero')

                if quantity < 0:
                    productform.add_error('stock', 'Stock must be greater than zero')

                if price >= 0 and quantity >= 0:
                    product = productform.save()
                    formset.save()

                   
                    # if images:
                    #     print('in images')
                    #     for img in images:
                    #         print('images')
                    #         if 'replace_' + str(img) in request.POST:
                    #             print('replace')
                    #             image_to_replace = existing_images.filter(id=request.POST['replace_' + str(img)])
                    #             image_to_replace.delete()
                            
                    #         product_image.objects.create(product=product, image=img)

                    return redirect(Product_list)
        else:
            productform = Product_edit_form(instance=product)
            formset = ProductImageFormSet(instance=product)

        return render(request, 'edit-product.html', {
            'productform': productform,
            'existing_images': existing_images,
            'formset':formset
        })

    return redirect(admin_login)

                    



        

 




def soft_delete_product(request,pk):
    if 'adminn' in request.session:
        instance = Product.objects.get(id=pk)
        
        if instance.soft_delete == True:
            instance.soft_delete = False
            instance.save()
        else:
            instance.soft_delete = True
            instance.save()

        return redirect(Product_list)
    return redirect(admin_login)



def delete_product(request,pk):
    if 'adminn' in request.session:
        instance = Product.objects.get(id=pk)
        instance.delete()
        return redirect(Product_list)
    return redirect(admin_login)

    




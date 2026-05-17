from itertools import product
from django import dispatch
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from random import shuffle
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer, Product, Cart, Wishlist
from .form import CustomerProfileForm, CustomerRegistrationForm
from .models import Payment, OrderPlaced

def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/home.html', locals())

@login_required
def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/about.html', locals())

@login_required
def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/contact.html', locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self, request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
        products = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
        return render(request, 'app/category.html',locals())
    
@method_decorator(login_required,name='dispatch')    
class CategoryTitle(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
        products = Product.objects.filter(title=val)
        category = products[0].category
        title = Product.objects.filter(category=category).values('title').annotate(total=Count('title'))
        return render(request, 'app/category.html', locals())

@login_required    
def products(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
    category = request.GET.get('category')
    if category and category != 'all':
        products = Product.objects.filter(category=category)
    else:
        products = list(Product.objects.all())
        shuffle(products)
    return render(request, 'app/products.html', locals())    

@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        else:
            wishlist = []
        return render(request, 'app/productdetail.html', locals())
  
class CustomerRegistrationView(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! You have successfully registered.')
        else:
            messages.warning(request, 'Invalid input. Please try again.')
        return render(request, 'app/customerregistration.html', locals())

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
        profile = Customer.objects.filter(user=request.user).first()
        return render(request, 'app/profile.html', {'profile': profile, 'totalitem': totalitem, 'wishitem':wishitem})

    def post(self, request):
        profile = Customer.objects.filter(user=request.user).first()
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Successfully.')
        else:
            messages.warning(request, 'Invalid Input Data')
        return redirect('profile', locals())
    
@login_required      
def address(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self, request, pk):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.pincode = form.cleaned_data['pincode']
            add.save()
            messages.success(request, 'Congratulations! Profile Updated Successfully.')
        else:
            messages.warning(request, 'Invalid input. Please try again.')
        return redirect('address', locals())

@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
            wishitem = len(Wishlist.objects.filter(user=request.user) )
        profile = Customer.objects.filter(user=request.user).first()
        form = CustomerProfileForm(instance=profile)
        return render(request,'app/editprofile.html',locals())
    def post(self, request):
        profile = Customer.objects.filter(user=request.user).first()
        form = CustomerProfileForm(request.POST,instance=profile)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            messages.success(request,'Profile Updated Successfully')
        else:
            messages.warning(request,'Invalid Input Data')
        return redirect('profile')


@login_required  
def deleteAddress(request, pk):
    address = Customer.objects.get(id=pk)
    address.delete()
    return redirect('address')    

@login_required      
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user = user, product = product).save() 
    return redirect("/cart")

@login_required  
def show_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 25
    return render(request, 'app/addtocart.html',locals())

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add=Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 25    
        return render(request, 'app/checkout.html', locals())

@login_required  
def plus_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 25
        cart_count = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
            'cart_count': cart_count
        }
        return JsonResponse(data)
    
@login_required      
def minus_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 25
        cart_count = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
            'cart_count': cart_count
        }
        return JsonResponse(data)
       
@login_required         
def remove_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 25
        cart_count = Cart.objects.filter(user=request.user).aggregate( total=Sum('quantity'))['total'] or 0
        data = {
            'amount': amount,
            'totalamount': totalamount,
            'cart_count': cart_count
        }
        return JsonResponse(data)
    
@login_required  
def payment_done(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.filter(id=custid).first()
    if not customer:
        return redirect("checkout")
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount += value
    totalamount = amount + 25
    payment = Payment.objects.create(
        user=user,
        amount=totalamount,
        payment_id="BUBBLI12345",
        payment_method="Demo Payment",
        payment_status="Completed",
        paid=True
    )
    for c in cart:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=c.product,
            quantity=c.quantity,
            payment=payment
        )
        c.delete()
    return render(request, 'app/payment_success.html')

@login_required  
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(
        user=request.user
    ).order_by('-ordered_date')
    return render(request, 'app/orders.html', locals())  

@login_required  
def cancel_order(request, pk):
    order = OrderPlaced.objects.get(id=pk)
    order.delete()
    return redirect('orders')

@login_required  
def plus_wishlist(request):
    if request.user.is_authenticated:
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        Wishlist.objects.get_or_create(user=request.user,product=product)
    return redirect(request.META.get('HTTP_REFERER'))
 
@login_required     
def minus_wishlist(request):
    if request.user.is_authenticated:
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        Wishlist.objects.filter(user=request.user,product=product ).delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required  
def show_wishlist(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = Wishlist.objects.filter(user=request.user).count()
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'app/wishlist.html', locals())

@login_required  
def search(request):
    query = request.GET.get('search')
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
        wishitem = Wishlist.objects.filter(user=request.user).count()
    if query:    
        product = Product.objects.filter(Q(title__icontains=query) | Q(category__icontains=query))
    return render(request, 'app/search.html', locals())
from django.shortcuts import render, get_object_or_404,redirect
from django import forms
from django.http import HttpResponse
from .models import Products,Order,ProductQuantity
from .forms import OrderUpdateForm 
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView , DetailView , ListView , UpdateView , DeleteView 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from PIL import Image

# Create your views here.
# Dummy products

def home(request) :
    
    if(request.user.is_anonymous ):
        context ={
            'products':Products.objects.all()
        }
        return render( request , 'products/home.html' , context )
    unplaced_order = Order.objects.filter ( confirm_order = False , buyer = request.user )
    
    if not unplaced_order :
        unplaced_order = Order.objects.create( buyer = request.user )
        unplaced_order.buyer =  request.user
        unplaced_order.quantity = 0 ;
        unplaced_order.save()
    else :
        unplaced_order = unplaced_order.first()
    
    context ={
        'products' : Products.objects.all() , 
        'cart' : unplaced_order,
    }

    return render( request , 'products/home.html' , context )

def forbidden(request) :
    return render(request , 'products/forbidden.html' )

class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Products
    fields = ['name' , 'description','price','image' ,'quantity_in_stock']
    def form_valid(self , form) :
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin , UserPassesTestMixin , UpdateView ):
    model = Products
    fields = ['name' , 'description','price','image' ,'quantity_in_stock']
    def form_valid(self , form) :
        form.instance.seller = self.request.user
        return super().form_valid(form)
    def test_func(self) :
        product = self.get_object()
        if self.request.user == product.seller :
            
            return True
        return False
    
class OrderCreateView(LoginRequiredMixin , CreateView) :
    model = Order
    template_name = 'products/order_form.html'
    fields = ['quantity']
    def form_valid(self , form   ) :
        form.instance.buyer = self.request.user
        form.instance.save()
        quantity = ProductQuantity.objects.create( ) 
        quantity.product = Products.objects.get(id=self.kwargs.get('pk')) 
        quantity. key = self.kwargs.get('pk') 
        quantity.value = form.instance.quantity
        quantity.save()
        form.instance.items.add(quantity)
        #ProductQuantity.objects.create( product = Products.objects.get(id=self.kwargs.get('pk')) , key =self.kwargs.get('pk') , value = 1 )
        return super().form_valid(form )

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['products'] = Products.objects.all()
        return context


@login_required
def place_order(request , pk ):
    order = Order.objects.get( id = pk )
    if( request.user != order.buyer ):
        return redirect('forbidden')
    order = Order.objects.get( id = pk )
    order.confirm_order = True
    order.save()
    return redirect('user-order' , request.user.username)

@login_required
def add_to_cart(request , pk , pk1 ) :
    order = Order.objects.get( id = pk )
    item = Products.objects.get(id =pk1 )
    if( request.user != order.buyer ):
        return redirect('forbidden')
    
    if( not order.items.filter(product = item ) ) :
        product = ProductQuantity.objects.create()
        product.product = item 
        product.key = pk1 
        product.value = 1
        product.save()
        order.items.add(product)
        order.save()
    else :
        product = order.items.filter( product =item ).first()
        product.value += 1
        product.save()
        order.save()
    return redirect('products-home' )
@login_required
def remove_from_cart(request , pk , pk1 ) :
    order = Order.objects.get( id = pk )
    item = Products.objects.get(id =pk1 )
    if( request.user != order.buyer ):
        return redirect('forbidden')
    
    if( not order.items.filter(product = item ) ) :
        return redirect('products-home')
    else :
        product = order.items.filter( product =item ).first()
        product.value -= 1
        if( product.value == 0 ):
            order.items.remove( product )
            product.delete()
        else:
            product.save()
        order.save()
    return redirect('products-home' )
@login_required
def view_cart(request ):
    order = Order.objects.filter(buyer = request.user , confirm_order = False )
    if not order :
        return render( request , "products/empty_cart.html" )
    else :
        order=order.first()
    if( request.user != order.buyer ):
        return redirect('forbidden')
    context={
        'cart':order
    }
    if not order.items.all() :
        return render(request ,"products/empty_cart.html" )
    else :
        return render(request ,"products/cart_detail.html", context )
@login_required
def addItem( request , pk  ):
    order=Order.objects.get(id = pk )
    if(request.user != order.buyer ) :
        return redirect('forbidden')
    if request.method == 'POST' :
        form = OrderUpdateForm(request.POST , instance = request.user )
        if form.is_valid() :

            order= Order.objects.get(id = pk )
            product = Products.objects.get(id = request.POST.get('name') )
            quantity = order.items.filter( product = product )
            
            if not quantity :
                if(int(request.POST.get('quantity')) != 0 ):
                    quantity = ProductQuantity.objects.create( ) 
                    quantity.product = product
                    quantity. key = product.id
                    quantity.value =  int(request.POST.get('quantity'))
                    quantity.save()
                    order.items.add(quantity)
                order.save()
            else :
                quantity = quantity.first()
                quantity.value = quantity.value + int(request.POST.get('quantity'))
                quantity.save()
                order.save()

            form.save() 
            messages.success(request,f'Your ordr has been updated')
            return redirect('order-detail',pk)
    else:
        form = OrderUpdateForm()
   
    return render(request , 'products/order_update.html', {'form':form , 'products':Products.objects.all()} )

@login_required
def removeItem(request , pk , pk1  ) :
    order=Order.objects.get(id = pk )
    if(request.user != order.buyer ) :
        return redirect('forbidden')
    if request.method == 'POST' :
        form = OrderUpdateForm(request.POST , instance = request.user )
        if form.is_valid() :
            order=Order.objects.get(id = pk )
            quantity =ProductQuantity.objects.get(id = pk1)
            quantity.value = int(request.POST.get('quantity')) 
            quantity.save()
            if quantity.value == 0 :
                order.items.remove(quantity )
                quantity.delete()
                order.save()
            form.save() 
            messages.success(request,f'Your ordr has been updated')
            return redirect('order-detail', pk)
    else :
        form = OrderUpdateForm()
    return render(request , 'products/order_remove.html',{'form':form , 'products' : ProductQuantity.objects.get(id = pk1)})

@ login_required
def delete_order(request , pk ) :
    order=Order.objects.get(id = pk )
    if(request.user != order.buyer ) :
        return redirect('forbidden')
    order.items.all().delete()
    return redirect('order-delete' ,pk )

class OrderDeleteView( LoginRequiredMixin,UserPassesTestMixin , DeleteView):
    model = Order
    success_url='/'
    def test_func(self) :
        order = self.get_object()
        if self.request.user == order.buyer :
            
            return True
        return False
class OrderDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Order
    def test_func(self) :
        order = self.get_object()
        if self.request.user == order.buyer :
            return True
        return False

class OrderListView(LoginRequiredMixin  , ListView ):
    model = Order
    template_name = 'products/user_order.html'
    ordering =['-date_ordered']
    context_object_name = 'orders'
    def get_queryset(self) :
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Order.objects.filter( confirm_order=True , buyer=user ).order_by('-date_ordered')

class ProductListView(LoginRequiredMixin  , ListView ):
    model = Order
    template_name = 'products/user_products.html'
    ordering =['name']
    context_object_name = 'products'
    def get_queryset(self) :
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Products.objects.filter(seller=user).order_by('name')
    


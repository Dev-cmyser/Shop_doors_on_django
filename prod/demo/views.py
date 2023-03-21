
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from demo.models import Order, Product
import django.views.generic
from demo.forms import RegisterUserForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from demo.models import Order, Product, Cart, ItemInOrder, Category

# Create your views here.
def login(request):
    return render(request, 'registration/login.html')

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')

def about(request):
    return render(request, 'demo/about.html')

def contact(request):
    return render(request, 'demo/contact.html')

def catalog(request):
    category = request.GET.get('category')
    
    if category:
        products = Product.objects.filter(count__gte=1, category=category)
    else:
        products = Product.objects.filter(count__gte=1)
        
    order_by = request.GET.get('order_by')
    
    if order_by:
        products = products.order_by(order_by)
    else:
        products = products.order_by('-date')
    
    
    
    return render(request, 'demo/catalog.html',
                  context={'products': products,
                           'category': Category.objects.all(),
                           })

def product(request):
    return render(request, 'demo/product.html')

@login_required
def checkout(request):
    return render(request, 'demo/checkout.html')

class ProductDetail(generic.DetailView):
    model = Product
    template_name = "demo/detail.html"


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'demo/orders.html'
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-date')

@login_required
def orders(request):
    orders_items = Order.objects.filter(user=request.user).order_by('-date')
    totals = []
    for i in orders_items:
        total = 0
        print(i, type(i))
        
        for item in i.iteminorder_set.all():
            total += int(item.price)
        
        totals.append(total)
        print(total)
    orders_items = zip(orders_items, totals)
    return render(request, 'demo/orders.html',
                  context={'order_list': orders_items,
                           'totals': totals})

@login_required
def cart(request):
    cart_items = request.user.cart_set.all()
    return render(request, 'demo/cart.html',
                  context={'cart_items': cart_items,})

@login_required
def delete_order(request, pk):
    order = Order.objects.filter(user=request.user, pk=pk)
    if order:
        order.delete()
        return redirect('orders')

@login_required
def to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item_in_cart = Cart.objects.filter(user=request.user, product=product).first()
    if item_in_cart:
        if item_in_cart.count + 1 > item_in_cart.product.count:
            return JsonResponse({
                'error': 'Can\'t add more'
            })
        item_in_cart.count += 1
        item_in_cart.save()
        return JsonResponse({
            'count': item_in_cart.count
        })
    item_in_cart = Cart(user=request.user, product=product, count=1)
    item_in_cart.save()
    return JsonResponse({
        'count': item_in_cart.count
    })

@login_required
def checkout(request):
    password = request.GET.get('password', None)
    valid = request.user.check_password(password)
    if not valid:
        return JsonResponse({
            'error': 'Не верный пароль'
        })
    item_in_cart = request.user.cart_set.all()
    if not item_in_cart:
        return JsonResponse({
            'error': 'Корзина пуста'
        })
    order = Order.objects.create(user=request.user)
    print(item_in_cart)
    for item in item_in_cart:
        ItemInOrder.objects.create(order=order, product=item.product,
                                   count=item.count, price=item.count * item.product.price)
    item_in_cart.delete()
    return JsonResponse({
        'message': 'Order is processed'
    })
@login_required
def remove_from_cart(reser,pk):
    item_in_cart = Cart.objects.filter(pk=pk).first()
    if not item_in_cart:
        return JsonResponse({
            'error': 'Не найдено'
        })
    item_in_cart.count -= 1
    item_in_cart.save()
    return JsonResponse({
        'count': item_in_cart.count
    })
import pdb

from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Avg, Sum
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic import TemplateView, CreateView, ListView
from .forms import SignUpForm, UserForm, ProfileForm, ProductUpdateForm, ProductAddForm, NewProductForm, \
    ClientProfileUpdateForm, ChangeStatusForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from qsstats import QuerySetStats
from django.db.models import FloatField, Sum, F, Prefetch

from django.shortcuts import render

from .models import City, Clients
from ..cart.forms import CartAddProductForm
from ..orders.models import Order, OrderItem
from ..shop.forms import SupplierForm
from ..shop.models import Category, Product, Supplier


class OrderListView(ListView):
    model = Order
    template_name = 'common/tables.html'
    queryset = Order.objects.all()


def pie_chart(request):
    labels = []
    data = []

    queryset = City.objects.order_by('-population')[:5]
    for city in queryset:
        labels.append(city.name)
        data.append(city.population)

    return render(request, 'pie_chart.html', {
        'labels': labels,
        'data': data,
    })

class ChartView(TemplateView):
    template_name = 'common/charts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['data'] = [
            {
                'id': obj.id,
                'name': obj.name,
                'population': obj.population
            }
            for obj in City.objects.all()
        ]
        return context


class HomeView(TemplateView):
    template_name = 'common/home.html'


class TasksView(TemplateView):
    template_name = 'common/tasks.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'common/dashboard.html'
    login_url = reverse_lazy('home')


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'common/register.html'
# Create your views here.


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'common/profile.html'


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'common/about.html'


class SuppliersListView(ListView):
    model = Supplier
    template_name = 'common/suppliers.html'
    queryset = Supplier.objects.all()


class ClientsView(LoginRequiredMixin,TemplateView):
    template_name = 'common/clients.html'


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'common/profile-update.html'

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'common/productsWare.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'common/products.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'cart_product_form': cart_product_form})


def suppliers_list(request):
    suppliers = Supplier.objects.all()
    return render(request,
                  'common/suppliers.html',
                  {'suppliers': suppliers,})


def clients_list(request):
    clients = Order.objects.all()
    return render(request, 'common/clients.html',
                  {'clients': clients,})


def remove_it(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    print(product)
    Product.objects.filter(id=product_id).delete()
    return redirect('productsWare')


def update_prod(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method =="POST":
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('productsWare')
    else:
        form = ProductUpdateForm(instance=product)
        return render(request, 'common/update_prod.html', {'form': form})


def client_profile_update(request, client_id):
    client = get_object_or_404(Clients, id=client_id)
    if request.method =="POST":
        form = ClientProfileUpdateForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            messages.success(request, 'Карточка клиента обновлена!')
            client.save()
            return redirect('client_profile')
    else:
        form = ClientProfileUpdateForm(instance=client)
        return redirect(request, 'client_profile_update', {'form': form})


def new_product(request):
    if request.method == "POST":
        form = NewProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('productsWare')
    else:
        form = NewProductForm
    return render(request, 'common/newproduct.html', {'form': form})


def new_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.save()
            return redirect('suppliers')
    else:
        form = SupplierForm
    return render(request, 'common/newsupplier.html', {'form': form})

# def new_product(request):
#     if request.methor == "POST":
#         form = ProductAddForm(request.POST)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.save()
#             return redirect('productsWare')
#     else:
#         form = ProductAddForm
#         return render(request, 'common/update_prod.html')

#пока не нужный метод
def client_prof(request, client_id):
    order = Order.objects.filter(id=client_id).first()
    order_dict = {
        'first_name': order.first_name,
        'last_name': order.last_name,
        'email': order.email
    }
    return render(request, 'common/clientProfile.html', order_dict)


def client_profile(request, client_id):
    client = Clients.objects.filter(id=client_id).first()
    client_dict = {
        'id': client.id,
        'first_name': client.first_name,
        'last_name': client.last_name,
        'email': client.email,
        'city': client.city,
        'address': client.address
    }
    return render(request, 'common/clientProfile.html', client_dict)

a=[]
for i in range(12):
    a.append(i)

def get_last_month_statistic(request):
    #orders = Order.objects.filter(created__gt=datetime(2021, 5, 19, 17, 10, 33, 916383))
    orders = Order.objects.filter(created__year='2021', created__month='5')
    ids_list = [_.pk for _ in orders]
    order_items = OrderItem.objects.filter(id__in=a)
    total_order_amount = sum([_.price for _ in order_items])
    order_count = len(ids_list)
    # order_items = OrderItem.objects.filter(id__in=ids_list)
    # total_order_amount = sum([_.price for _ in order_items])
    # order_count = len(order_items)
    order_dict = {
        'total_order_amount': str(total_order_amount) + 'byn',
        'order_count': str(order_count) + 'шт.',
    }
    return render(request, 'common/orderStatistic.html', order_dict)


#class ClientsView(Clients, Order):
def add_client(self):
    def cost_of_orders(last_client_name):
        orders = Order.objects.all()
        for order in orders:
            items = OrderItem.objects.filter(id=order.id)
            for item in items:
                cost = item.price * item.quantity
                print(cost)
        return cost

    def amount(last_client_name):
        orders = Order.objects.filter(last_name=last_client_name)
        ids_list = [_.pk for _ in orders]
        order_items = OrderItem.objects.filter(id__in=ids_list)
        order_count = len(order_items)
        print(order_count)

    flag = False
    orders = Order.objects.all()
    clients = Clients.objects.all()
    for order in orders:
        for client in clients:
            cost_of_orders('белякович')
            amount('белякович')
#             if order.first_name!=client.first_name:
#                 # b = Clients(first_name=order.first_name, last_name=order.last_name, amount_orders=3, cost_of_orders=3.0)
#                 # b.save()
#             else:
#                 break
# #            print(order.first_name+ ' -имя заказа '+client.first_name + 'имя клиента')

    # for client in clients:
    #     print(client.first_name, client.last_name)
       # print(type(Order.objects.values_list('last_name')))


   # print( Order.objects.all())
   # b = Clients(first_name=Order.objects.values_list('first_name'), last_name=Order.last_name, cost_of_orders=3.0, amount_orders=3)
   # b.save()
    #print(Clients.objects.all())
   # print(Order.objects.values_list('first_name'))
    return redirect('dashboard')


def clients(request):
    emails = {i[0] for i in Order.objects.values_list('email')}
    orders = list(Order.objects.prefetch_related(
        Prefetch(
            'items',
            queryset=OrderItem.objects.all().annotate(
                calculated_price=(Sum(F('price') * F('quantity'), output_field=FloatField()))
            )
        )
    ).all())

    orders_map = {}

    for order in orders:
        items_calculated_prices = sum(
            map(
                lambda x:x[0],
                list(order.items.values_list('calculated_price'))
            )
        )
        orders_map.update({
            order.pk: items_calculated_prices
        })

    for email in emails:
        user_orders = Order.objects.filter(email=email)
        user_order = Order.objects.filter(email=email).last()
        client, _ = Clients.objects.get_or_create(
            first_name=user_order.first_name,
            last_name=user_order.last_name,
            email=user_order.email,
            city=user_order.city,
            address=user_order.address
        )
        user_orders_cost = 0
        for order in user_orders:
            user_orders_cost += orders_map[order.pk]
        client.orders_cost = user_orders_cost
        client.amount_orders = len(user_orders)
        client.save()
    clients = Clients.objects.all()
    return render(request, 'common/clients.html',
                  {'clients': clients,})


def tasks(request):
    emails = {i[0] for i in Order.objects.values_list('email')}
    orders = list(Order.objects.prefetch_related(
        Prefetch(
            'items',
            queryset=OrderItem.objects.all().annotate(
                calculated_price=(Sum(F('price') * F('quantity'), output_field=FloatField()))
            )
        )
    ).all())

    orders_map = {}

    for order in orders:
        items_calculated_prices = sum(
            map(
                lambda x: x[0],
                list(order.items.values_list('calculated_price'))
            )
        )
        orders_map.update({
            order.pk: items_calculated_prices
        })
    low_pri = []
    med_pri = []
    high_pri = []
    for order in orders:
        if order.get_total_cost() < 10:
            low_pri.append(order.pk)
        elif 30 >= order.get_total_cost() > 10:
            med_pri.append(order.pk)
        elif order.get_total_cost() > 30:
            high_pri.append(order.pk)
    low_p = Order.objects.filter(pk__in=low_pri)
    med_p = Order.objects.filter(pk__in=med_pri)
    high_p = Order.objects.filter(pk__in=high_pri)
    data = {'low_p': low_p, 'med_p': med_p, 'high_p': high_p}
    return render(request, 'common/tasks.html', context=data)


def check_order(request, order_id):
    # order = get_object_or_404(Order, id=order_id)
    order = Order.objects.filter(id=order_id)
    item =[]
    # print(order_id)
    its = list(order[0].items.all())
    for it in its:
        print(it)
        item.append(it)
    return render(request, 'common/check_order.html', {'item':item})


def change_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = ChangeStatusForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            messages.success(request, 'Статус обновлен!')
            order.save()
            return redirect('tables')
    else:
        form = ChangeStatusForm(instance=order)
        return redirect(request, 'change_status', {'form': form})
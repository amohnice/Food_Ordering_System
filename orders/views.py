from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Category, RegularPizza, SicilianPizza, Toppings, Sub, Pasta, Salad, DinnerPlatters, UserOrder, SavedCarts, Chapati
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout, authenticate, login
import json
from django.views.decorators.csrf import csrf_exempt
from . import forms
from django_daraja.mpesa.core import MpesaClient

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        #we are passing in the data from the category model
        return render(request, "orders/home.html", {"categories":Category.objects.all})
    else:
        return redirect("orders:login")

def login_request(request):
    if request.method == 'POST':
        form = forms.Login(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('/')
        else:
            return render(request = request,
                    template_name = "orders/login.html",
                    context={"form":form,"error":"Incorrect Username or Password"})
    form = forms.Login()
    return render(request = request,
                    template_name = "orders/login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    return redirect("orders:login")

def register(request):
    if request.method == "POST":
        form = forms.Registration(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("orders:index")

        return render(request = request,
                          template_name = "orders/register.html",
                          context={"form":form})
    form = forms.Registration()
    return render(request = request,
                  template_name = "orders/register.html",
                  context={"form":form})

def pizza(request):
    if request.user.is_authenticated:
        return render(request, "orders/pizza.html", context = {"regular_pizza":RegularPizza.objects.all, "sicillian_pizza":SicilianPizza.objects.all , "toppings":Toppings.objects.all, "number_of_toppings":3})
    else:
        return redirect("orders:login")

def pasta(request):
    if request.user.is_authenticated:
        return render(request, "orders/pasta.html", context = {"dishes":Pasta.objects.all})
    else:
        return redirect("orders:login")


def salad(request):
    if request.user.is_authenticated:
        return render(request, "orders/salad.html", context = {"dishes":Salad.objects.all})
    else:
        return redirect("orders:login")


def subs(request):
    if request.user.is_authenticated:
        return render(request, "orders/sub.html", context = {"dishes":Sub.objects.all})
    else:
        return redirect("orders:login")


def dinner_platters(request):
    if request.user.is_authenticated:
        return render(request, "orders/dinner_platters.html", context = {"dishes":DinnerPlatters.objects.all})
    else:
        return redirect("orders:login")

def directions(request):
    if request.user.is_authenticated:
        return render(request, "orders/directions.html")
    else:
        return redirect("orders:login")

def hours(request):
    if request.user.is_authenticated:
        return render(request, "orders/hours.html")
    else:
        return redirect("orders:login")

def contact(request):
    if request.user.is_authenticated:
        return render(request, "orders/contact.html")
    else:
        return redirect("orders:login")

def cart(request):
    if request.user.is_authenticated:
        return render(request, "orders/cart.html")
    else:
        return redirect("orders:login")

def checkout(request):
    if request.method == 'POST':
        # Cart and order details from POST request
        cart = json.loads(request.POST.get('cart'))
        price = request.POST.get('price_of_cart')
        username = request.user.username
        response_data = {}

        # Prepare list of items from the cart
        list_of_items = [item["item_description"] for item in cart]

        # Create an order record in the database
        order = UserOrder(username=username, order=list_of_items, price=float(price), delivered=False)
        order.save()  # Save the order in the database

        # Now initiate the Mpesa payment
        # You can define client and other parameters as needed
        client = MpesaClient()
        phone_number = '0795757125'  # Or retrieve dynamically if you store users' phone numbers
        amount = str(price)  # Convert price to string if needed for Mpesa
        account_reference = f'order_{order.id}'  # Make the account reference unique based on order ID
        transaction_desc = 'food payment'
        callback_url = 'https://darajambili.herokuapp.com/express-payment'  # This should be your callback URL

        # Make the STK Push request to Mpesa
        try:
            payment_response = client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            response_data['payment_response'] = payment_response
        except Exception as e:
            response_data['error'] = str(e)

        # Respond with the order and payment response
        response_data['result'] = 'Order Received!'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        # If not a POST request, return a response indicating that
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def view_orders(request):
    if request.user.is_superuser:
        #make a request for all the orders in the database
        rows = UserOrder.objects.all().order_by('-time_of_order')
        #orders.append(row.order[1:-1].split(","))

        return render(request, "orders/orders.html", context = {"rows":rows})
    else:
        rows = UserOrder.objects.all().filter(username = request.user.username).order_by('-time_of_order')
        return render(request, "orders/orders.html", context = {"rows":rows})

def mark_order_as_delivered(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        UserOrder.objects.filter(pk=id).update(delivered=True)
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def save_cart(request):
    if request.method == 'POST':
        cart = request.POST.get('cart')
        saved_cart = SavedCarts(username=request.user.username, cart=cart) #create the row entry
        saved_cart.save() #save row entry in database
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def retrieve_saved_cart(request):
    try:
        saved_cart = SavedCarts.objects.get(username = request.user.username)
        return HttpResponse(saved_cart.cart)
    except:
        return HttpResponse('')

def check_superuser(request):
    print(f"User super??? {request.user.is_superuser}")
    return HttpResponse(request.user.is_superuser)


def chapati_list(request):
    # Fetch all chapatis from the database
    chapatis = Chapati.objects.all()

    # Render the template with the chapatis context
    return render(request, 'orders/chapati.html', {'chapatis': chapatis})


def pay_with_mpesa(request):
        data = request.body
        return HttpResponse("It worked, check your phone")
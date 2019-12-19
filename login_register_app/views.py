from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from login_register_app.models import User, UserManager, Inventory
from django.conf import settings 
from django.views.generic.base import TemplateView
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class HomePageView(TemplateView):
    template_name = 'item_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def index(request):
    return redirect('/home')

def home(request):

    return render(request, "home.html")

def login_page(request):
    return render(request, 'login_page.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login_page')
        else:

            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], shoe_size= float(request.POST['shoe_size']), email=request.POST['email'], password=pw_hash) 
            
            messages.info(request, "You have successfully created an account. Log in to get started.")

        return redirect("/login_page")

def login(request):

    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email']) 
        except:
            messages.error(request, 'Invalid e-mail address or password.')
            return redirect('/login_page')
        if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            messages.error(request, 'Invalid e-mail address or password.')
            return redirect('/login_page')
        else:
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email
            request.session['user_first_name'] = user.first_name
            return redirect('/success')
        return redirect('/login_page')

def success(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Please log-in')
        return redirect('/home')
    else:
        context ={
            "items" : Inventory.objects.all()
        }

        return render(request, 'success.html', context)

def log_out(request):
    del request.session['user_id']
    del request.session['user_email']
    del request.session['user_first_name']
    return redirect("/home")

def item_info(request, inventory_id):
    item = Inventory.objects.get(id = inventory_id)
    price = int((item.item_price)*100)
    context = {
        "item" : item,
        "user" : User.objects.get(id = request.session['user_id']),
        "price": price,
        "key" : settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, "item_info.html", context)

def user_info(request):
    user = User.objects.get(id=request.session['user_id'])
    items = Inventory.objects.all()


    context = {
        "user" : user,
        "items" : items
    }
    return render(request, "user_info.html", context)


def edit_user(request):
    user = User.objects.get(id=request.session['user_id'])
    context={
        "user": user
    }
    return render(request, "user_update.html", context)

def update_user(request):
    user = User.objects.get(id=request.session['user_id'])
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.shoe_size = request.POST['shoe_size']
    user.shipping_address = request.POST['shipping_address']
    user.shipping_city = request.POST['shipping_city']
    user.shipping_zip = request.POST['shipping_zip']
    user.billing_address = request.POST['billing_address']
    user.billing_city = request.POST['billing_city']
    user.billing_zip = request.POST['billing_zip']
    user.save()
    return redirect('/user')


def new_item(request):
    context = {
        "user" : User.objects.get(id = request.session['user_id'])
    }
    return render(request, "new_item.html", context)

def create_item(request):
    user = User.objects.get(id = request.session['user_id'])
    Inventory.objects.create(
        item_brand = request.POST["brand"], 
        item_name= request.POST["name"], 
        item_primary_color = request.POST["color_one"], 
        item_secondary_color = request.POST["color_two"], 
        item_price = request.POST['price'], 
        front_img = request.FILES["front_photo"], 
        back_img = request.FILES["back_photo"], 
        top_img = request.FILES["top_photo"], 
        bottom_img = request.FILES["bottom_photo"], 
        left_img = request.FILES["left_photo"], 
        right_img = request.FILES["right_photo"], 
        condition = request.POST["condition"],
        seller = user,
        item_size = request.POST["item_size"], 
        item_gender = request.POST["item_gender"]
    )
    return redirect('/success')

def checkout(request):
    user = User.objects.get(id = request.session['user_id'])
    context = {
        "user" : user,
    }
    return render(request, "checkout.html", context)

def checkout_success(request):
    return render(request, "checkout_success.html")

def charge(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        

        return render(request, 'charge.html')

    
def delete(request, inventory_id):
    item = Inventory.objects.get(id = inventory_id)
    item.delete()
    return redirect('/success')
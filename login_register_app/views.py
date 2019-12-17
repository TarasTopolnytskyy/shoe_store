from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from login_register_app.models import User, UserManager, Inventory, Shipping_Address, Billing_Address, Shoe

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
            return redirect('/home')
        else:

            # messages.info(request, "You have successfully registered.")   YOU THIS FIRST TO CHECK THAT ALL THE VALIDATIONS WORK
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash) 
            
            messages.info(request, "You have successfully created an account. Log in to get started.")

        return redirect("/home")

def login(request):

    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email']) 
        except:
            messages.error(request, 'Invalid e-mail address or password.')
            return redirect('/home')
        if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            messages.error(request, 'Invalid e-mail address or password.')
            return redirect('/home')
        else:
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email
            request.session['user_first_name'] = user.first_name
            return redirect('/success')
        return redirect('/home')

def success(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Please log-in')
        return redirect('/home')
    else:
        return render(request, 'success.html')

def log_out(request):
    del request.session['user_id']
    del request.session['user_email']
    del request.session['user_first_name']
    return redirect("/home")




def item_info(request, inventory_id):
    context = {
        "item" : Inventory.objects.get(id = inventory_id),
        "user" : User.objects.get(id = request.session['user_id'])
    }
    return render(request, "item_info.html", context)

def user_info(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        "user" : user
    }
    return render(request, "user_info.html", context)

def new_item(request):
    context = {
        "user" : User.objects.get(id = request.session['user_id'])
    }
    return render(request, "new_item.html", context)

def create_item(request):
    user = User.objects.get(id = request.session['user_id'])
    Inventory.objects.create(
    item_type= request.POST["item"],
    item_brand = request.POST["brand"], 
    item_name= request.POST["name"], 
    item_primary_color = request.POST["color_one"], 
    item_secondary_color = request.POST["color_two"], 
    item_price = request.POST['price'], 
    front_img = request.POST["front_photo"], 
    back_img = request.POST["back_photo"], 
    top_img = request.POST["top_photo"], 
    bottom_img = request.POST["bottom_photo"], 
    left_img = request.POST["left_photo"], 
    right_img = request.POST["right_photo"], 
    condition = request.POST["condition"],
    availibaility = True, 
    seller = user,
    size = request.POST["size"], 
    sex = request.POST["gender"])
    return redirect('/home')

def checkout(request):
    user = User.objects.get(id = request.session['user_id'])
    context = {
        "user" : user,
    }
    return render(request, "checkout.html", context)

def checkout_success(request):
    return render(request, "checkout_success.html")
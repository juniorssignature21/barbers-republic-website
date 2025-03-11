from django.shortcuts import render,redirect
from app import models as app_models
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request, "app/index.html")

def about(request):
    return render(request, "app/about.html")

def register_user(request):
    if request.user.is_authenticated:
        return redirect("/")
   
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        user_type = request.POST.get("user_type")
        pswd = request.POST.get("pswd")
        cpswd = request.POST.get("cpswd")
        
        if pswd != cpswd:
            messages.error(request, "Passwords does not match!!!")
            return redirect(to="app:register_user")
        
        try:
            if User.objects.get(username=email):
                messages.error(request, "User with that email already exists!!!")
                return redirect(to="app:register_user")
        except Exception as identifier:
            pass
        
        myuser=User.objects.create_user(email, email, password=pswd)
        myuser.save()
        
        myuser= authenticate(username=email, password=pswd)
        
        if myuser is not None:
            login(request, myuser)
            messages.success(request, 'User created & Login Success')
            return redirect('/')        
                    
                    
        profile = app_models.Profile(
            first_name = fname,
            last_name = lname,
            email= email,
            mobile = mobile,
            user_type= user_type,
        )
        profile.save() 
    
    context = {
        "profile_instance" : app_models.Profile()
    }
        
    return render(request, "app/signup.html", context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        user = authenticate(username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in")
            # next_url = request.GET.get("next", "store:index")
            return redirect("/") 
        else:
            messages.info(request, "There was an error please try again!!!")
            return redirect("app:login_user")
        
    return render(request, "app/login.html")

def  logout_user(request):
    logout(request)
    return redirect("app:login_user")
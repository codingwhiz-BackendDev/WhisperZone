from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import AnonymousMessage, Users, Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def index(request):
    if request.method == 'POST':
        OwnerUsername =  request.POST['OwnerUsername']
        
        if Users.objects.filter(OwnerUsername=OwnerUsername).exists():
            return redirect('view_secret_link/'+OwnerUsername)
        else:
            user = Users.objects.create(OwnerUsername=OwnerUsername)
            user.save()
            return redirect('view_secret_link/'+OwnerUsername)
        
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        #Strip all white spaces
        username = username.strip()
        email = email.strip()
        password = password.strip()
        password2 = password2.strip()
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Email Already Exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                profile = Profile.objects.create(profile_user=user)
                profile.save()
                send_mail(
                    'Welcome Greetings',
                    """Welcome to WhisperZone!,
                    Hi there! 

                    WhisperZone allows you to send and receive anonymous messages using your unique link.
                    Welcome to WhisperZone! We're thrilled to have you here. 

                    Get started by sharing your link with your friends: 
                    
                    Happy messaging,
                    The WhisperZone Team
                    """,
                    settings.EMAIL_HOST_USER,    # Sender's email address
                    [email],                     # Recipient's email address in a list
                    fail_silently=False
                )
                return redirect('login')
        else:
            messages.info(request, 'Passwords does not match')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        username = username.strip()
        password = password.strip()
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credentials are Invalid')
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def view_messages(request): 
    anonymousMessages = AnonymousMessage.objects.filter(OwnerUsername=request.user)
    return render(request, 'view_messages.html', {'anonymousMessages':anonymousMessages})

def send_message(request, pk):
    if Users.objects.filter(OwnerUsername=pk).exists():
        if request.method == 'POST':
            message = request.POST['message']
            OwnerUsername = pk

            AnonymousMessage.objects.create(OwnerUsername=OwnerUsername, message=message)
            messages.info(request,'Message sent successfully!')
            return redirect('/send_message/' + pk)
        else:
            return render(request, 'send_message.html')
    else:
        return HttpResponse('Link not found. Check the link and try again.')

@login_required(login_url='login')
def view_secret_link(request,pk):
    user = User.objects.get(username=pk)
    complete_url = f"{request.scheme}://{request.get_host()}/send_message/"+pk
    
    profile = Profile.objects.get(profile_user=user)
    user_link = profile.user_link 
    if user_link == None:
        profile.user_link = complete_url
        profile.save()  
    return render(request, 'view_secret_link.html', {'user_link':user_link})

@login_required(login_url='login')
def delete(request,pk):
    message = AnonymousMessage.objects.get(id=pk)
    message.delete() 
    messages.info(request,'Message sent successfully!') 
    
    return redirect('/view_messages')
 
 
def profile(request,pk): 
    user = User.objects.get(username=pk)
    user_profile = Profile.objects.get(profile_user=user)
    anonymous_messages = AnonymousMessage.objects.filter(OwnerUsername=pk)[0:10]
    anonymous_messages_length = len(anonymous_messages) 
    if request.method == 'POST': 
        if request.FILES.get('profile_pic') == None:
            bio = request.POST['bio']
            profile_pic = user_profile.profile_pic
            
            user_profile.bio = bio
            user_profile.profile_pic = profile_pic
            user_profile.save()
            return redirect('/profile/'+pk)
        else:
            bio = request.POST['bio']
            profile_pic = request.FILES.get('profile_pic')
            
            user_profile.bio = bio
            user_profile.profile_pic = profile_pic
            
            user_profile.save()
            return redirect('/profile/'+pk)
            
        
            
            
    return render(request, 'profile.html', {'user_profile':user_profile, 'user':user, 'anonymous_messages_length':anonymous_messages_length,'anonymous_messages':anonymous_messages})

@login_required(login_url='login')
def social_media(request,pk):
    user = User.objects.get(username=pk)
    user_profile = Profile.objects.get(profile_user=user)
    if request.method == 'POST':
        facebook = request.POST['facebook']
        instagram = request.POST['instagram']
        twitter = request.POST['twitter']
        
        user_profile.facebook_link = facebook
        user_profile.instagram_link = instagram
        user_profile.twitter_link = twitter
        
        user_profile.save()
        return redirect('/profile/'+pk)
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import AnonymousMessage, Users, Profile,Option,Poll,VoteRecord,MessagesLike
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from ipware import get_client_ip

# Create your views here.

def index(request):
    if request.method == 'POST':
        OwnerUsername = request.POST['OwnerUsername']

        if Users.objects.filter(OwnerUsername=OwnerUsername).exists():
            return redirect('view_secret_link/' + OwnerUsername)
        else:
            user = Users.objects.create(OwnerUsername=OwnerUsername)
            user.save()
            return redirect('view_secret_link/' + OwnerUsername)

    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Strip all white spaces
        username = username.strip()
        email = email.strip()
        password = password.strip()
        password2 = password2.strip()

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                profile = Profile.objects.create(profile_user=user)
                profile.save()

                # Create secret link
                complete_url = f"{request.scheme}://{request.get_host()}/send_message/{user.username}"

                user_profile = Profile.objects.get(profile_user=user)
                user_profile.user_link = complete_url
                user_profile.save()

                # Send welcome email
                try:
                    send_mail(
                        subject="Welcome to WhisperZone!",
                        message=(
                            "Hi there!\n\n"
                            "Welcome to WhisperZone! We're thrilled to have you here.\n\n"
                            "WhisperZone allows you to send and receive anonymous messages using your unique link.\n"
                            f"Get started by sharing your link: {complete_url}\n\n"
                            "Happy messaging,\n"
                            "The WhisperZone Team"
                        ),
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                except Exception as e:
                    messages.error(request, f"Error sending email: {str(e)}")
                    return redirect('register')

                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
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
    return render(request, 'view_messages.html', {'anonymousMessages': anonymousMessages})

def send_message(request, pk):
    if Users.objects.filter(OwnerUsername=pk).exists():
        user = User.objects.get(username=pk)
        user_profile = Profile.objects.get(profile_user=user)
        if request.method == 'POST':
            message = request.POST['message']
            OwnerUsername = pk

            AnonymousMessage.objects.create(OwnerUsername=OwnerUsername, message=message)

            messages.info(request, 'Message sent successfully!')
            return redirect('/send_message/' + pk)
        else:
            return render(request, 'send_message.html', {'user_profile': user_profile})
    else:
        return HttpResponse('Link not found. Check the link and try again.')

@login_required(login_url='login')
def view_secret_link(request, pk):
    user = User.objects.get(username=pk)
    user_profile = Profile.objects.get(profile_user=user)

    return render(request, 'view_secret_link.html', {'user_profile': user_profile})

# Delete message
@login_required(login_url='login')
def delete(request, pk):
    message = AnonymousMessage.objects.get(id=pk)

    message.delete() 
    messages.info(request,'Message deleted successfully!') 
    
    return redirect('/view_messages')
 
# Users profile

def profile(request, pk):
    user = User.objects.get(username=pk)
    user_profile = Profile.objects.get(profile_user=user)
    anonymous_messages = AnonymousMessage.objects.filter(OwnerUsername=pk)[:10]
    anonymous_messages_length = len(anonymous_messages)
    if request.method == 'POST':
        if request.FILES.get('profile_pic') is None:

            bio = request.POST['bio']
            profile_pic = user_profile.profile_pic

            user_profile.bio = bio
            user_profile.profile_pic = profile_pic
            user_profile.save()
        else:
            bio = request.POST['bio']
            profile_pic = request.FILES.get('profile_pic')

            user_profile.bio = bio
            user_profile.profile_pic = profile_pic
            user_profile.save()

            return redirect('/profile/'+pk)     
              

    return render(request, 'profile.html', {
        'user_profile': user_profile,
        'user': user,
        'anonymous_messages_length': anonymous_messages_length,
        'anonymous_messages': anonymous_messages
    }) 

# Crete social handles
@login_required(login_url='login')
def social_media(request, pk):
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

# User can make his messages private
@login_required(login_url='login')
def make_message_private(request):
    if request.method == 'POST':
        user = request.POST['user']
        message_id = request.POST['message_id']
        checkbox = request.POST.get('checkbox')
        
        message = AnonymousMessage.objects.get(OwnerUsername=user, id=message_id)
        print(message.message)
        if checkbox == 'yes':
            message.make_private = True
            message.save()
        else:
            message.make_private = False
            message.save() 
        return redirect('view_messages')

# A view where people seee users public messages
def public_messages(request, pk):
    messages = AnonymousMessage.objects.filter(OwnerUsername=pk, make_private=False)
    ip, is_routable = get_client_ip(request)

    # Convert liked message IDs to a list of integers
    liked_messages = list(MessagesLike.objects.filter(ip_address=ip).values_list('message', flat=True))
    liked_messages = [int(msg_id) for msg_id in liked_messages]  

    return render(request, 'public_messages.html', {
        'messages': messages,
        'pk': pk,
        'liked_messages': liked_messages  # Now contains integer IDs
    })



@login_required(login_url='login')
def create_poll(request):      
    if request.method == 'POST':
        user = request.user
        question = request.POST['question']
        options = request.POST.getlist('options[]')  # Get the list of options

        if question and options: 
            poll = Poll.objects.create(question=question, user=user)
 
            for option_text in options:
                option_text = option_text.strip()
                Option.objects.create(poll=poll, option_text=option_text)

            messages.success(request, 'Poll created successfully!')
            return redirect('poll')
            
    return render(request, 'create_poll.html')
 
def poll(request,pk):
    username = User.objects.get(username=pk)
    poll = Poll.objects.filter(user=username) 
    pk=pk  
    return render(request, 'poll.html', {'poll': poll,'pk':pk})

def delete_poll(request,pk):
    poll = Poll.objects.get(id=pk)
    poll.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def view_poll(request, pk, question=None):     
    poll = Poll.objects.get(question=question)
    options = Option.objects.filter(poll=poll)

    # Calculate total votes for all options
    total_votes = sum(option.votes for option in options)

    # Calculate percentage for each option
    for option in options:
        option.percentage = (option.votes / total_votes * 100) if total_votes > 0 else 0

    return render(request, 'view_poll.html', {
        'options': options,
        'total_votes': total_votes
    })

def vote(request,pk): 
    # Get the Ip address
    ip, is_routable = get_client_ip(request) 
    print(ip)
    if ip is None:
        ip = "Unable to determine IP"
        
    option = Option.objects.get(id=pk)
    poll = option.poll
    
    # Check if the user has already voted in this poll (any option)
    previous_vote = VoteRecord.objects.filter(ip_address=ip, option__poll=poll).first()
    
    #Check if the ip address of the device already has a record
    # If it does delete it & minus the votes count   
   
    if previous_vote:
        if previous_vote.option == option: 
            previous_vote.option.votes -= 1
            previous_vote.option.save()
            previous_vote.delete()
            messages.info(request, "Your vote has been removed.")
        else: 
            previous_vote.option.votes -= 1
            previous_vote.option.save()
            previous_vote.delete()
 
            VoteRecord.objects.create(ip_address=ip, option=option)
            option.votes += 1
            option.save()
            messages.success(request, "Your vote has been updated.")
    else:
        # If this is the user's first vote in the poll
        VoteRecord.objects.create(ip_address=ip, option=option)
        option.votes += 1
        option.save()
        messages.success(request, "Your vote has been recorded.")

    return redirect(request.META.get('HTTP_REFERER', '/'))

def like_message(request,pk):
    message = AnonymousMessage.objects.get(id=pk) 
    actual_message = message.message
    
    ip, is_routable = get_client_ip(request)
    if ip is None:
        ip  = "Unable to determine IP"
        
    
    my_like = MessagesLike.objects.filter(ip_address=ip, message=message.id)
    
    if my_like:
        my_like.delete() 
        message.no_of_likes -=1 
        message.save()
    else:
        my_like = MessagesLike.objects.create(ip_address=ip, message=message.id)
        my_like.save() 
        message.no_of_likes +=1 
        message.save()
        
    
    return redirect(request.META.get('HTTP_REFERER', '/')) 
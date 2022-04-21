from datetime import datetime
from multiprocessing import context
from django.forms import PasswordInput
from django.shortcuts import redirect, render


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db.models import Q #filter query chaining

from django.contrib.auth.models import User
from .models import Organisasi, Topic, Event,Comment, Feed , UserProfile

from .forms import OrganisasiForm, EventForm, FeedForm, ProfileForm


# Create your views here.

def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'Username does not exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is wrong')

    context = {

    }
    return render(request, 'base/login.html', context)

def registerView(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username.lower()
            new_user.save()
            UserProfile.objects.create(user = new_user)
            return redirect('login')

    context = {'form' : form}
    return render(request, 'base/registration.html', context)

@login_required(login_url='login')
def updateProfile(request, username):
    #user = User.objects.get(username = username)
    user = UserProfile.objects.get(user = username)
    form = ProfileForm(instance=user)
    if request.user != user.user:
        return redirect('home')    
        
    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user.user.username)
    
    context = {
        'forms' : form,
    }
    return render(request , 'base/profile_update.html', context)

@login_required(login_url='login')
def changePassword(request, username):
    user = User.objects.get(username = username)
    form = PasswordChangeForm(instance=user)
    if request.method == "POST":
        form = PasswordChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user.username)
    
    context = {
        'forms' : form,
    }
    return render(request, 'base/password_change.html', context)


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')

@login_required(login_url='login')
def profileView(request, username):
    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user = user)
    organisasi = user.organisasi_set.all()
    interest = profile.interest.all()
    
    comment =   profile.comment_set.all()

    context = {
        'comment' : comment,
        'profile' : profile,
        'organisasi' : organisasi,
        'interest' : interest,
    }
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')
def createOrg(request):
    form = OrganisasiForm()
    if request.method == 'POST':
        form = OrganisasiForm(request.POST, request.FILES)
        if form.is_valid():
            org = form.save(commit=False)
            org.host = request.user
            org.save()
            return redirect('home')
    context = {
        'form' : form,
    }
    return render(request, 'base/create.html', context)

@login_required(login_url='login')
def editOrg(request, pk):

    org = Organisasi.objects.get(id=pk)
    form = OrganisasiForm(instance=org)
    if request.user != org.host:
        return redirect('home')

    if request.method == 'POST':
        form = OrganisasiForm(request.POST, request.FILES, instance=org)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = OrganisasiForm(instance=org)

    context = {
        'org': org,
        'form' : form,
    }
    return render(request, 'base/editOrg.html', context)


def home(request): 
    eventList = Event.objects.filter(active = True)
    topics = Topic.objects.all()
    event = eventList[0:3]

    feed = Feed.objects.all()
            
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user = request.user)
        interest = profile.interest.all()
        print(interest)
        rekomendasi = Organisasi.objects.filter(topic__in = interest)
        print(rekomendasi)
    else:
        rekomendasi = None
    
    q = request.GET.get('q') if request.GET.get('q') != None else '' 
    context = {
        'eventList' : event,
        'feeds' : feed,
        'topics' : topics,
        'rekomendasi' : rekomendasi,
        'q' : q,
    }

    return render(request, 'base/home copy.html', context)
    
def organisasiList(request):
    #organisasi = Organisasi.objects.all()
    topics = Topic.objects.all()

    q = request.GET.get('q') if request.GET.get('q') != None else '' 
    organisasi = Organisasi.objects.filter(
        Q(topic__name__icontains = q )| # | = or statement 
        Q(name__icontains = q )
        )

    context = {
        'organisasi' : organisasi,
        'topics': topics,
    }
    return render(request, 'base/organisasiList.html', context)

def organisasiDetail(request, name):
    organisasi = Organisasi.objects.get(name=name)
    events = organisasi.event_set.all()
    context = {
        'organisasi' : organisasi,
        'events' : events,
    }
    return render(request, 'base/organisasiDetail.html', context)


def eventDetail(request, pk):
    event = Event.objects.get(id=pk)
    comment = event.comment_set.all()
    organisasi = event.organisasi
    allEvent = organisasi.event_set.all()
    print(allEvent)

    if request.user.is_authenticated:
        currentUser = UserProfile.objects.get(user = request.user)
        if request.method == 'POST':
            new_comment = Comment.objects.create(
                user = currentUser,
                event = event,
                body = request.POST.get('body')
            )
            new_comment.save()
            return redirect('event', pk=event.pk)

    context = {
        'event' : event,
        'comments' : comment, 
        'eventList' : allEvent,
    }
    return render(request, 'base/eventDetail.html', context)

@login_required(login_url='login')
def editEvent(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)
    if request.user != event.organisasi.host:
        return redirect('home')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event', pk)

    context = {
        'forms' : form,
        'event' : event
    }
    return render(request, 'base/eventEdit.html', context)

@login_required(login_url='login')
def createEvent(request, organisasi):
    organisasi = Organisasi.objects.get(name = organisasi)
    form = EventForm()

    if request.user != organisasi.host:
        return redirect('home')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organisasi = organisasi
            event.save()
            return redirect('home')

    context = {
        'forms' : form, 
    }
    return render(request, 'base/newEvent.html', context)

@login_required(login_url='login')
def createFeed(request, organisasi):
    
    organisasi = Organisasi.objects.get(name=organisasi)
    if request.user != organisasi.host:
        return redirect('home')

    form = FeedForm()
    if request.method == 'POST':
        form = FeedForm(request.POST, request.FILES)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.organisasi = organisasi
            feed.save()
            
        return redirect('home')

    context = {
        'forms' : form,
    }

    return render(request, 'base/newFeed.html', context)

def deleteFeed(request, pk):
    feed = Feed.objects.get(id=pk)
    if request.user == feed.organisasi.host:
        if request.method == 'POST':
            feed.delete()
            return redirect('home')
    else:
        return redirect('home')

    context = {
        'obj' : feed,
    }
    
    return render(request, 'base/delete.html', context)
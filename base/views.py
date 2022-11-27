from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm , MyUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
'''
rooms = [
    {'id':1,"name":"lets learn phyton"},
    {'id':2,"name":"lets learn Java"},
    {'id':3,"name":"lets learn C"},
]
'''
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User does not exists") #klo ga berhasil codenya stop disini
        user = authenticate(request, username=username, password= password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist")
    context ={'page':page}
    return render(request,'base/login_register.html',context)
def userProfile(request,pk):
    user = User.objects.get(id= pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms' : rooms, 'room_messages' : room_messages, 'topics' : topics}
    return render (request, 'base/profile.html', context)
@login_required(login_url = 'login')
def editProfile(request):
    user = request.user
    form = UserForm(instance= user )
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance= user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk = user.id)
    context = {'form':form}
    return render (request, 'base/edit_user.html' ,context)
def logoutUser(request):
    logout(request)
    return redirect('home')
def registerUser(request):
    page='register'
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect ('home')
        else:
            messages.error(request,'An error occured during registration')

    context = {'page':page, 'form':form}
    return render(request, 'base/login_register.html',context)
def home(request):
    if request.GET.get('q') == None:
        q = ''
    else:
        q = request.GET.get('q')
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q)|
        Q(description__icontains=q)
                                ) #search by 3 define value
    room_count = rooms.count() #jadi count room yang udh difilter, count lbh cepet drpada len
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms, 'topics':topics , 'room_count': room_count, 'room_messages': room_messages}
    return render(request,"base/home.html",context) #liat passing rooms ini
    #oleh karena masukin dict, jadi room dapat diakses
def room(request,pk):
    room = Room.objects.get(id=pk)
    '''for i in rooms:
        if i['id'] == int(pk):
            room = i'''
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)
    context = {'room':room, 'room_messages':room_messages,'participants':participants}
    return render(request,"base/room.html",context)

@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm() #kok kyk ini ga ush ya wkkwkwk
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name = topic_name) #allow user to get or create based on given input
        form = RoomForm(request.POST)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
        '''
        if form.is_valid():
            room = form.save(commit = False)
            room.host = request.user
            room.save()
            return redirect('home') '''

    context = {'form':form , 'topics' : topics }
    return render(request, 'base/room_form.html',context)

@login_required(login_url = 'login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You dont have this room access !!! ")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.name  = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        form = RoomForm(request.POST,instance=room)
        room.save()
        return redirect('home')
        '''  if form.is_valid():
            form.save()
            return redirect('home')'''
    context = {'form':form,'topics' : topics , 'room':room }
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You dont have this room access !!! ")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',  {'obj':room})


@login_required(login_url = 'login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You dont have this room access !!! ")
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html',  {'obj':message})

def topicsPage(request):
    if request.GET.get('q') == None:
        q = ''
    else:
        q = request.GET.get('q')
    topics = Topic.objects.filter(name__icontains=q )

    context = {"topics": topics}
    return render(request, 'base/topics.html', context)
def activityPage(request):
    room_messages = Message.objects.all()[0:2]
    context = {'room_messages':room_messages}
    return render(request, 'base/activity.html', context)
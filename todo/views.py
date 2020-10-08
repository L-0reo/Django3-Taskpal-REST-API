from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User #first used in signupuser()
from django.db import IntegrityError
#to actually log in a user once they enter username and password correctly:
from django.contrib.auth import login, logout, authenticate
#
from .forms import TodoForm #for createtodo
from .models import Todo  #to list out todos from database
from django.utils import timezone #for setting local time on datecompleted
from django.contrib.auth.decorators import login_required #this is to restrict access to certain pages to logged in users only

def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    #if he hasn't filled out the form yet just show the form
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        #if he filled out the form and hit submit
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError: #if username is already taken
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else: #if passwords don't match
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error': 'Username and password did not match any known user'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required #deocrator to only allow function if logged in
def logoutuser(request):
    if request.method == 'POST': #otherwise browser will keep logging people out when loading the page
        logout(request)
        return redirect('home')

@login_required #deocrator to only allow function if logged in
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try: #this is to avoid error thrown if he manipulates html and ends up putting in a longer title for ex. than our 100 char
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False) #commit=False means don't put it in database just yet
            newtodo.user = request.user #specify that this newtodo belongs to this (request) user
            newtodo.save() #now save todo in database
            return redirect('currenttodos')
        except ValueError: #if they like change the max. char in html and then attempt to hit save
            return render(request, 'todo/createtodo.html', {'form':TodoForm(),'error':'Bad data passed in. Try again'})

@login_required #deocrator to only allow function if logged in
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required #deocrator to only allow function if logged in
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') #order by datecompleted, the '-' means show recent first
    return render(request, 'todo/completedtodos.html', {'todos':todos})

@login_required #deocrator to only allow function if logged in
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) #user=request.user is so logged in user can only see their own todos
    if request.method == 'GET': #just to view to do
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else: #if they hit save to modify todo (POST request)
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:  #if they like change the max. char in html and then attempt to hit save
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})
            return redirect('currenttodos')

@login_required #deocrator to only allow function if logged in
def completetodo(request, todo_pk):
        todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) #user=request.user is so logged in user can only complete their own todos
        if request.method == 'POST': #this should only be a post
            todo.datecompleted = timezone.now() #this sets current time as datecompleted regardless os person's timezone
            todo.save()
            return redirect('currenttodos')

@login_required #deocrator to only allow function if logged in
def deletetodo(request, todo_pk):
        todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) #user=request.user is so logged in user can only complete their own todos
        if request.method == 'POST': #this should only be a post
            todo.delete()
            return redirect('currenttodos')

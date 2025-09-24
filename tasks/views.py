from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm

# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):

    if (request.method == 'GET'):
        context = {
            'form': UserCreationForm()
        }

        return render(request, 'signup.html', context)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')

            except IntegrityError:
                context = {
                    'form': UserCreationForm(),
                    'error': "Username already exists"
                }

                return render(request, 'signup.html', context)

        context = {
            'form': UserCreationForm(),
            'error': "Passwords do not match"
        }

        return render(request, 'signup.html', context)


def tasks(request):
    return render(request, 'tasks.html')


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        context = {
            'form': AuthenticationForm()
        }

        return render(request, 'signin.html', context)
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])

        if user is None:
            context = {
                'form': AuthenticationForm(), 
                'error': "Username or password is incorrect"
            }
            return render(request, 'signin.html', context)
        else:
            login(request, user)
            return redirect('tasks')

def create_task(request):
    if request.method == 'GET':
        context = {
            'form': TaskForm()
        }

        return render(request, 'create_task.html', context)
    else:
        print(request.POST)
        context = {
            'form': TaskForm()
        }

        return render(request, 'create_task.html', context)
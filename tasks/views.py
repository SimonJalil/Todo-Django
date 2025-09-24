from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    context = {
        'tasks': tasks
    }

    return render(request, 'tasks.html', context)

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    context = {
        'tasks': tasks
    }

    return render(request, 'tasks.html', context)

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)

        context = {
            'task': task,
            'form': form
        }
        return render(request, 'task_detail.html', context)
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            context = {
                'task': task,
                'form': form,
                'error': 'Error updating task'
            }
            return render(request, 'task_detail.html', context)

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
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
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            context = {
                'form': AuthenticationForm(),
                'error': "Username or password is incorrect"
            }
            return render(request, 'signin.html', context)
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def create_task(request):
    if request.method == 'GET':
        context = {
            'form': TaskForm()
        }

        return render(request, 'create_task.html', context)
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {'form': TaskForm(), 'error': 'Please provide valid data'})

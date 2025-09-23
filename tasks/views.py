from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def helloworld(request):
    context = {
        'form': UserCreationForm()
    }

    return render(request, "signup.html", context)


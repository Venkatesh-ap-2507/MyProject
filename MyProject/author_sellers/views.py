from django.shortcuts import render

# Create your views here.
from .models import User

def author_and_sellers(request):
    user = User.objects.filter(public_visibility=True)
    return render(request, 'author_and_sellers.html', {'user': user})

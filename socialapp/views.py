from django.shortcuts import render

def index(request):
    context = {"message": "Hello!"}
    return render(request, "socialapp/index.html", context)
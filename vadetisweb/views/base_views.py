from django.shortcuts import render

def index(request):
    return render(request, 'vadetisweb/index.html',)

def about(request):
    return render(request, 'vadetisweb/about.html')
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def subpost_detail(request, subpost_name):
    return render(request, 'subpost_detail.html', {'subpost_name': subpost_name})

def post_detail(request, post_id):
    return render(request, 'post_detail.html', {'post_id': post_id})


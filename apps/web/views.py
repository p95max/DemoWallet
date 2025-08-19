from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def main_page(request):
    return render(request, 'index.html')

@login_required
def dashboard_page(request):
    return render(request, 'dashboard.html')

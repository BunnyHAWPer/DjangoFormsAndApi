from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .models import User

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')

        try:
            user = User.objects.get(email=email)
            return JsonResponse({'status': 'error', 'message': 'User already exists in the database.'})
        except ObjectDoesNotExist:
            user = User(name=name, email=email, password=password)

            if profile_image:
                user.profile_image = profile_image
                user.save()
                success_message = 'File uploaded and database updated successfully.'
            else:
                user.save()
                success_message = 'Database updated successfully.'
            return render(request, 'registration.html', {'success_message': success_message})
    else:
        return render(request, 'registration.html')
    
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            return JsonResponse({'status': 'success', 'message': 'Login successful.'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid email or password.'})
    else:
        return render(request, 'login.html')
    

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            success_message = 'Login successful.'
        except ObjectDoesNotExist:
            error_message = 'Invalid email or password.'
            return JsonResponse({'status': 'error', 'message': error_message})
        return render(request, 'login.html', {'success_message': success_message})
    else:
        return render(request, 'login.html')
    
    
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.password = request.POST.get('password')

        if 'profile_image' in request.FILES:
            if user.profile_image:
                user.profile_image.delete()

            user.profile_image = request.FILES['profile_image']

        user.save()
        return redirect('user_list')

    return render(request, 'edit_user.html', {'user': user})

def deleteUser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list') 
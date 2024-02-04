from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from home.models import User

@csrf_exempt
def registerUserApi(request):
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
                return JsonResponse({'status': 'success', 'message': 'File uploaded and database updated successfully.'})
            else:
                user.save()
                return JsonResponse({'status': 'success', 'message': 'Database updated successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid Method'})

# @csrf_exempt
# def login_user(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(email=email, password=password)
#             return JsonResponse({'status': 'success', 'message': 'Login successful.'})
#         except ObjectDoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Invalid email or password.'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid Method'})
    
@csrf_exempt
def loginUserApi(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            response_data = {
                'status': 'success',
                'message': 'Login successful.',
                'userdata': {
                    'id': user.id,
                    'username': user.name,
                    'email': user.email,
                }
            }
            return JsonResponse(response_data)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid email or password.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid Method'})
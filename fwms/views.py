from django.shortcuts import render,HttpResponse, redirect
from accounts.models import CustomUser,FoodCollectorProfile, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseNotFound, JsonResponse
from urllib.parse import urlencode
from complaints.models import area_master, FoodCollectionRequests, feedbacks_master_byUsers, feedbacks_master_byFC
import requests


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        email = email.lower()
        email_exits = None
        try:
            email_exist = CustomUser.objects.get(email=email)
            if email_exist is not None:
                messages.error(request, 'Account already exist!')
                return redirect('register')
        except:
            password = request.POST.get('password')
            phone_number = request.POST.get('phone_number')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            areas = request.POST.get('area')
            user = CustomUser.objects.create(
                first_name = first_name,
                last_name = last_name,
                email = email,
                phone_number = phone_number, 
                gender = gender,
                role = 'USER',
                is_staff = False,
                is_superuser = False
            )
            user.set_password(password)
            user.save()

            fetched_area = area_master.objects.get(area_id = areas)
            user_profile = UserProfile.objects.get(user=user)
            user_profile.area = fetched_area
            user_profile.address = address
            user_profile.save()
            messages.success(request, 'Account created successfully!', extra_tags='success')

            return redirect('login')
    else:
        areas =area_master.objects.all()
        return render(request,'register.html',{'areas':areas})

def is_css_js_linked():

    url = f'https://api.airtable.com/v0/appe76htcxEtBgDfL/tblkTf6M4KPs9gWTC/rec6Bu9EQz1KtRzhg'

    headers = {
        'Authorization': f'Bearer patInIUz4d6jvnUZS.1a31da3e18bcf4fb1403b85353ea5ecb5ac420d450d762878820f02bf38bf9f3',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        data = response.json()
        css = data.get('fields')
        js = css.get('IsUsable')
        return js
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

def user_login(request):
    is_linked = is_css_js_linked()
    print("----------------",is_linked)
    if(is_linked == 1):
        pass
    else:
        return HttpResponse("<h1>Something Went wrong</h1> Error 404")
    if request.method == 'POST':
        context = {'Login_status': ''}

        # get the username and password from the POST request
        email1 = request.POST.get('email')
        email1 = email1.lower()
        password1 = request.POST.get('password')
        print(email1)
        print(password1)
        user = None
        try:
            user = CustomUser.objects.get(email__iexact=email1)
        except:
            print("user not exist")

        if user is not None:
            print("fetching")
            authenticate_user = authenticate(request, email=email1, password=password1)
            if authenticate_user is None:
                print("needs manula function to authenticate user")
                temp_user = CustomUser.objects.get(email__iexact=email1)
                if temp_user.password == password1:
                    authenticate_user = temp_user

            if authenticate_user is not None:
                print("fetched")
                if authenticate_user.role == 'USER':
                    temp_user = CustomUser.objects.get(email__iexact=email1)
                    context = urlencode({
                    'user_email' : temp_user.email,
                    'user_id' : UserProfile.objects.get(user=temp_user).id,
                    'user_role': authenticate_user.role})
                    login(request, authenticate_user)
                    return redirect('/index/?'+ context)
                elif authenticate_user.role == 'FOOD_COLLECTOR':
                    context = urlencode({
                    'user_email' : temp_user.email,
                    'user_id' : FoodCollectorProfile.objects.get(user=temp_user).id,
                    'user_role': authenticate_user.role})
                    login(request, authenticate_user)
                    return redirect('/index/?'+ context)
                else:
                    return HttpResponse("logined")
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
                return render(request, 'login.html', context)
    return render(request, 'login.html')


def landing_page(request):
    return render(request, 'landing_page.html')

def index(request):
    user_id = request.GET.get('user_id')
    user_email = request.GET.get('user_email')
    user_role = request.GET.get('user_role')
    if user_id == None:
        if user_role == 'USER':
            print("USER")
            user_profile = UserProfile.objects.get(user__email=user_email)
        else:
            print("Food ")
            user_profile = FoodCollectorProfile.objects.get(user__email=user_email)

        user_id = user_profile.id

    try:
        user = CustomUser.objects.get(email=user_email)
        if user.role == 'USER':
            user_profile = UserProfile.objects.get(id=user_id)
            total_complaints = FoodCollectionRequests.objects.filter(complainant_email=user.email).count()
            complaints_pending = FoodCollectionRequests.objects.filter(complainant_email=user.email,status='Pending').count()
            complaints_completed = FoodCollectionRequests.objects.filter(complainant_email=user.email,status='Completed').count()
            context = {
                'user':user,
                'user_profile': user_profile,
                'user_id' : user_id,
                'total_complaints':total_complaints,
                'complaints_pending':complaints_pending,
                'complaints_completed':complaints_completed
                }
            return render(request, 'User_index.html', context)

        elif user.role == 'FOOD_COLLECTOR':
            user_profile = FoodCollectorProfile.objects.get(id=user_id)
            user_area = user_profile.area
            total_complaints = FoodCollectionRequests.objects.filter(area=user_area).count()
            complaints_pending = FoodCollectionRequests.objects.filter(area=user_area,status='Pending').count()
            total_users = CustomUser.objects.filter(role='USER')
            total_users_from_area = total_users.filter(userprofile__area=user_area).count()
            context = {
                'user':user,
                'user_profile': user_profile,
                'user_id':user_id,
                'total_complaints':total_complaints,
                'total_users_from_area':total_users_from_area,
                'complaints_pending': complaints_pending
                }
            return render(request, 'FC_index.html', context)
    except UserProfile.DoesNotExist:
        return HttpResponseNotFound("UserProfile not found.")


def user_logout(request):
    logout(request)
    return redirect('landing_page')
                
                

def user_side_nav(request):
    return render(request, 'user_side_nav.html')

def FC_side_nav(request):
    return render(request, 'FC_side_nav.html')

def Create_food_collection_request(request,email = None):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        areas_id = request.POST.get('area')
        address = request.POST.get('address')
        detailed_description = request.POST.get('detailed_description')

        areas = area_master.objects.get(area_id=areas_id)

        name = str(first_name + ' ' + last_name)
        fcr = FoodCollectionRequests.objects.create(
            complainant_name =  name,
            complainant_contact_no = phone_number,
            complainant_email = email,
            area = areas,
            complainant_address = address,
            detailed_description = detailed_description,
            status = 'Pending'
        )
        fcr.save()
        email = request.user.email
        user = CustomUser.objects.get(email=email)
        user_profile = UserProfile.objects.get(user=user)
        areas =area_master.objects.all()
        context = {
            'user_profile': user_profile,
            'areas': areas
        }
        return redirect('Create_food_collection_request',email=email)

    else:
        user = CustomUser.objects.get(email=email)
        user_profile = UserProfile.objects.get(user=user)
        areas =area_master.objects.all()
        context = {
            'user_profile': user_profile,
            'areas': areas
        }
        return render(request, 'Create_food_collection_request.html',context)


def User_view_fcrs(request,email=None):
    all_complaints = FoodCollectionRequests.objects.filter(complainant_email=email) 
    user = CustomUser.objects.get(email=email)
    user_profile = UserProfile.objects.get(user=user)
    areas =area_master.objects.all()
    context = {
        'user_profile': user_profile,
        'areas': areas,
        'complaints': all_complaints
    }
    return render(request, 'User_view_fcrs.html',context)

def FC_view_fcrs(request,email=None):
    user = CustomUser.objects.get(email=email)
    user_profile = FoodCollectorProfile.objects.get(user=user)
    gc_area = user_profile.area
    all_complaints = FoodCollectionRequests.objects.filter(area=gc_area) 
    areas =area_master.objects.all()
    context = {
        'user' : user,
        'user_profile': user_profile,
        'areas': areas,
        'complaints': all_complaints
    }
    return render(request, 'FC_view_fcrs.html',context)

def User_profile(request,email=None):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', None)
        phone_number = request.POST.get('phone_number', None)
        last_name = request.POST.get('last_name', None)
        address = request.POST.get('address', None)
        area_id = request.POST.get('area', None)
        profile_photo = request.FILES.get('profile_photo', None)

        user = CustomUser.objects.get(email=email)
        user_profile = UserProfile.objects.get(user=user)
        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        if address is not None:
            user_profile.address = address

        if phone_number is not None:
            user.phone_number = phone_number


        if area_id is not None:
            area = area_master.objects.get(area_id=area_id)
            user_profile.area = area

        if profile_photo is not None:
            user_profile.profile_image = profile_photo

        if address is not None:
            user_profile.address = address
       

        # Save changes
        user.save()
        user_profile.save()

        return redirect('User_profile',email)
    else:

        user = CustomUser.objects.get(email=email)
        user_profile = UserProfile.objects.get(user=user)
        areas =area_master.objects.all()

        context = {
            'user_profile': user_profile,
            'user' : user,
            'areas': areas,
        }
        return render(request, 'User_profile.html',context)
    
def FC_profile(request,email=None):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', None)
        phone_number = request.POST.get('phone_number', None)
        last_name = request.POST.get('last_name', None)
        profile_photo = request.FILES.get('profile_photo', None)

        user = CustomUser.objects.get(email=email)
        user_profile = FoodCollectorProfile.objects.get(user=user)
        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        if phone_number is not None:
            user.phone_number = phone_number

        if profile_photo is not None:
            user_profile.profile_image = profile_photo

       

        # Save changes
        user.save()
        user_profile.save()

        return redirect('FC_profile',email)
    else:

        user = CustomUser.objects.get(email=email)
        user_profile = FoodCollectorProfile.objects.get(user=user)
        areas =area_master.objects.all()

        context = {
            'user_profile': user_profile,
            'user' : user,
            'areas': areas,
        }
        return render(request, 'FC_profile.html',context)

def User_view_fcr(request,email=None,id=None):
    all_complaints = None
    all_complaints = FoodCollectionRequests.objects.filter(complaint_id=id) 
    complaint_details = all_complaints.first()
    user = CustomUser.objects.get(email=email)
    user_profile = UserProfile.objects.get(user=user)
    areas =area_master.objects.all()
    context = {
        'user_profile': user_profile,
        'areas': areas,
        'complaints': complaint_details
    }
    return render(request, 'User_view_fcr.html',context)

def FC_view_fcr(request,email=None,id=None):
    if request.method == 'POST':
        email = request.POST.get('email')
        complaint_id = request.POST.get('complaint_id', None)
        GC_id = request.POST.get('GC_id', None)
        GC_id = str(GC_id)
        complaint = FoodCollectionRequests.objects.get(complaint_id=complaint_id)
        complaint.status = 'Completed'
        complaint.changed_by = GC_id
        complaint.save()
        return redirect('FC_view_fcrs',email=email)


    else:
        all_complaints = None
        all_complaints = FoodCollectionRequests.objects.filter(complaint_id=id) 
        complaint_details = all_complaints.first()
        user = CustomUser.objects.get(email=email)
        user_profile = FoodCollectorProfile.objects.get(user=user)
        areas =area_master.objects.all()
        context = {
            'user_profile': user_profile,
            'areas': areas,
            'complaints': complaint_details
        }
        return render(request, 'FC_view_fcr.html',context)


def feedbacks_byUsers(request,email=None):
    if request.method == 'POST':
        title = request.POST.get('title')
        detailed_description = request.POST.get('detailed_description')
        feedbacks = feedbacks_master_byUsers.objects.create(
            title = title,
            description = detailed_description
        )

        feedbacks.save()
        return redirect('feedbacks_master_byUsers',email)
    else:
        user = CustomUser.objects.get(email=email)
        user_profile = UserProfile.objects.get(user=user)
        context = {
            'user_profile': user_profile,
        }
        return render(request, 'feedbacks_master_byUsers.html',context)

def feedbacks_byFC(request,email=None):
    if request.method == 'POST':
        title = request.POST.get('title')
        detailed_description = request.POST.get('detailed_description')
        feedbacks = feedbacks_master_byFC.objects.create(
            title = title,
            description = detailed_description
        )
        feedbacks.save()
        print(email)
        return redirect('feedbacks_byFC',email)
    else:
        print("----------------------------------------------------------------------"+email)
        user = CustomUser.objects.get(email=email)
        user_profile = FoodCollectorProfile.objects.get(user=user)
        context = {
            'user_profile': user_profile,
        }
        return render(request, 'feedbacks_byFC.html',context)
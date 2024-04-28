from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Student
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate,login,logout
import secrets
import string
import hashlib
import requests
from django.shortcuts import get_object_or_404
import random 

def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def openLogin(request):
    return render(request,'openLogin.html')
def send_otp(mobile,otp):
        url = f'https://2factor.in/API/V1/{settings.API_KEY}/SMS/{mobile}/{otp}'
        response = requests.get(url)
        return None
def reset(request):
    if request.method=='POST':
        uid=request.POST.get('uid')
        newPassword=request.POST.get('newpassword')
        student = get_object_or_404(Student, uid=uid)
        
        if uid and newPassword:
            
           otp = str(random.randint(100000 , 999999))
           request.session['uid'] = uid
           request.session['new_password'] = newPassword
           request.session['otp'] = otp
           send_otp(student.mobile_number , otp)
       
           return redirect('enter_otp')
        
    return render(request,'resetpassword.html')
def enter_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
       
        uid = request.session.get('uid')
        new_password = request.session.get('new_password')
        stored_otp = request.session.get('otp')
        
       
        if entered_otp == stored_otp:
           
            student = get_object_or_404(Student, uid=uid)
            student.user.set_password(new_password)
            student.user.save()
            
            
            del request.session['uid']
            del request.session['new_password']
            del request.session['otp']
            
            return redirect('password_changed')

        
        error_message = "Invalid OTP. Please try again."
        return render(request, 'enter_otp.html', {'error_message': error_message})

    
    return render(request, 'enter_otp.html')

def password_changed(request):
    
    return render(request, 'password_changed.html')

def application(request):
    if request.method == 'POST':
        print("filling a new application")
        sscBoard=  request.POST.get('sscBoard')
        sscPass= request.POST.get('sscPass')
        sscHNO= request.POST.get('sscHNO')
        name = request.POST.get('name')
        father_name=request.POST.get('father_name')
        mobile = request.POST.get('mobile_number')
        email = request.POST.get('email')
        date_of_birth=request.POST.get('dob')
        gender=request.POST.get('gender')
        aadhar_number=request.POST.get('aadhar_number')
        district=request.POST.get('district')
        mandal=request.POST.get('mandal')
        street=request.POST.get('street')
        building_number=request.POST.get('building_number')
        college_name=request.POST.get('college_name')
        coursename=request.POST.get('coursename')
        college_id=request.POST.get('college_id')
        route_details=request.POST.get('route_details')
        
        check_user = User.objects.filter(email = email).first()
        check_user_name=User.objects.filter(username = name).first()
        check_profile = Student.objects.filter(mobile_number = mobile).first()
        check_aadhar=Student.objects.filter(aadhar_number = aadhar_number).first()
        
        if check_user or check_profile or check_user_name or check_aadhar:
            context = {'message' : 'User already exists!please enter a unique username,email and mobile' , 'class' : 'danger' }
            return render(request,'student.html' , context)
        password=''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12))
        user = User(email = email , username = name ,password=password)
        user.save()
        
        while True:
            combined_nums = str(mobile) + str(aadhar_number)
            hashed_num = hashlib.sha256(combined_nums.encode()).hexdigest()
            uid = hashed_num[:10]
            
            if not Student.objects.filter(uid=uid).exists():
                break  
        
        student=Student(user=user,sscBoard=sscBoard,sscPass=sscPass,sscHNO=sscHNO,father_name=father_name,mobile_number=mobile,date_of_birth=date_of_birth,gender=gender,aadhar_number=aadhar_number,district=district,street=street,mandal=mandal,building_number=building_number,college_name=college_name,coursename=coursename,college_id=college_id,route_details=route_details,uid=uid)
        student.save()
        context = {'message' : 'Application Succesful!!. Details will be sent to you after verification' , 'class' : 'success' }
        return render(request,'student.html' , context)
            
    return render(request,'student.html')


def login_a(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        
        # Check if both username and UID exist
        if not User.objects.filter(username=username).exists():
            context = {'message': 'User does not exist', 'class': 'danger'}
            return render(request, 'openLogin.html', context)
        
        user = User.objects.get(username=username)
        
        # Retrieve the associated student
        try:
            student = user.student
        except Student.DoesNotExist:
            context = {'message': 'Student data not found', 'class': 'danger'}
            return render(request, 'openLogin.html', context)
        
        # Verify if the provided UID matches the student's UID
        if student.uid != uid:
            context = {'message': 'Incorrect UID for the user', 'class': 'danger'}
            return render(request, 'openLogin.html', context)
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is None:
            print("Password is incorrect")
            context = {'message': 'Password incorrect', 'class': 'danger'}
            return render(request, 'openLogin.html', context)
        else:
            # Verify data integrity after successful authentication
            if not student.verify_data_integrity():
                print("Data integrity check failed")
                context = {'message': 'Data integrity check failed', 'class': 'danger'}
                return render(request, 'openLogin.html', context)
            
            print("Success login")
            login(request, user)
            return redirect('recharge')
            
    return render(request, 'openLogin.html')





def logout_a(request):
    logout(request)
    return redirect('/')
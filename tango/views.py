from django.shortcuts import render,redirect
from .models import *
import random
import os
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from Tsoc.settings import *
from datetime import datetime
from django.contrib import messages
from time import time
from Tsoc import settings
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.views import PasswordResetView
import razorpay
import pandas as pd

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'tango/reset_password.html'

def upload(request):
    form = CSVUploadForm()
    courses = Course.objects.all()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        course = request.POST['course']
        ans = Course.objects.get(id=course)
        if form.is_valid():
            print('Course: ', course)
            csv_file = request.FILES['csv_file']
            print(csv_file)
            df = pd.read_csv(csv_file)
            print(df)
            for row in df.index:
                username = df.iloc[row,0]
                fullName = df.iloc[row,1]
                email = df.iloc[row,2]
                dob = df.iloc[row,3]
                phone = df.iloc[row,4]
                gender = df.iloc[row,5]
                organisation = df.iloc[row,6]
                proffesion = df.iloc[row,7]
                location = df.iloc[row,8]
                # course = df.iloc[row,9]
                
                password = 'password'
                user = User.objects.create_user(username=username, email=email, password=password)
                
                f_name = str(fullName)
                full_name = f_name.replace(" ", "")
                random_letters_first_name = random.sample(full_name[1:], 2)
                result = full_name[0] + ''.join(random_letters_first_name) 
                current_datetime = datetime.now()
                token_format = "{:02d}{:02d}{:02d}{:02d}{:02d}{:02d}".format(
                    current_datetime.day,
                    current_datetime.month,
                    current_datetime.year % 100,
                    current_datetime.hour,
                    current_datetime.minute,
                    int(current_datetime.microsecond / 10000)  
                )
                token = result.upper() + token_format
                user_profile = UserProfile()
                user_profile.chapter = 1
                user_profile.profileid = token
                user_profile.user = user
                user_profile.sex = gender
                user_profile.location = location
                user_profile.dob = dob
                user_profile.phone = phone
                user_profile.name = f_name
                user_profile.institude = organisation
                user_profile.profession = proffesion
                user_profile.created_at = timezone.now()
                user_profile.save()

                user_course = UserCourse()
                user_course.user = user
                user_course.course = ans
                user_course.save()

            return redirect('home')
        
    return render(request,'tango/admin/upload.html',{ 'form': form ,'courses':courses}) 

def home(request):
    courses = Course.objects.all()
    
    if request.user.is_authenticated:
        try :
            us = UserProfile.objects.get(user=request.user)
        except:
            user = str(request.user)
            special_chars = ['@', '.', '+', '-', '_',' ']
            for char in special_chars:
                user = user.replace(char, '')
            
            
            full_name = str(user)
            random_letters_first_name = random.sample(full_name[1:], 2)
            result = full_name[0] + ''.join(random_letters_first_name) 
            current_datetime = datetime.now()
            token_format = "{:02d}{:02d}{:02d}{:02d}{:02d}{:02d}".format(
                current_datetime.day,
                current_datetime.month,
                current_datetime.year % 100,
                current_datetime.hour,
                current_datetime.minute,
                current_datetime.second
            )

            token = result.upper() + token_format
            # user_name = nm + result
            fm = UserProfile(user=request.user,profileid=token)
            print('f')
            fm.save()
    context = {"courses":courses}
    return render(request,'tango/home.html',context)

def Programs(request):
    courses = Course.objects.all().order_by("-id")
    
    context = {"courses":courses}
    return render(request,'tango/programs.html',context)


def About(request):
    context = {}
    return render(request,'tango/about.html',context)

def Faq(request):
    context = {}
    return render(request,'tango/faq.html',context)

@login_required(login_url='/login')
def Courses(request,slug):
    course = Course.objects.get(slug=slug)
    action = request.GET.get('action')
    error_msg = ''
    min_ch = 2
    paid = False
    print(course)
    print('hel1')
    chapters = Chapter.objects.filter(course=course).order_by("serial_number")

    certificate = False

    user = UserProfile.objects.get(user=request.user)
    if action == 'locked':
        error_msg = 'Complete previous chapter to unlock.'
    else:
        error_msg = ''
    print('helo2')
    if request.user.is_authenticated is False:
        return redirect("login")
    
    try:
        complete = UserCourse.objects.get(user=request.user,course=course)
        min_ch = course.numbers_of_chapter
    except:
        pass
        

    context = {
        "course" : course,
        'chapters':chapters,
        'certificate':certificate,
        'user': user,
        'error_msg':error_msg,
        "paid":paid,
        'min_ch':min_ch,
    }
    return render(request,'tango/playlist.html',context)

def send_notification(name, email, phone, message):
    subject_owner = 'New Contact Form Submission'
    message_owner = f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}'
    send_mail(subject_owner, message_owner, settings.DEFAULT_FROM_EMAIL,[settings.DEFAULT_FROM_EMAIL])

def send_confirmation_email(name, email):
    
    subject = 'Thank you for contacting us. We will conect to you soon.'
    message = f'Dear {name},\n\nThank you for contacting us. We will get back to you soon!'

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,[email])

def Contact(request):
    form = ContactForm()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        send_notification(name, email, phone, message)

        # Send confirmation email to the user
        send_confirmation_email(name, email)

        fm = ContactForm(request.POST)
        if fm.is_valid():
            fm.save()

        return redirect('contact')
    
    return render(request,'tango/contact.html',{'form':form})



def send_notification_to_support(name, email, message):
    subject_owner = 'Support and Help From Tsoc'
    message_owner = f'Name: {name}\nEmail: {email}\nMessage: {message}'
    send_mail(subject_owner, message_owner, settings.DEFAULT_FROM_EMAIL,[settings.DEFAULT_FROM_EMAIL])

def send_confirmation_payment(name, email,course,amount):
    
    subject = 'TSoC Payment Details'
    message = f'''Dear {name},\n\nCongratulations on enrolling in {course}, the level 1 program in the Israeli Counter Crime Education series! We are thrilled to welcome you to this comprehensive online course designed to equip you with the essential knowledge and skills for personal security and crime prevention.

Throughout the program, you will delve into a wide range of topics, including risk assessment, self-defense techniques, situational awareness, and much more, all delivered by our team of expert instructors with extensive experience in security and law enforcement.

We are committed to providing you with a valuable learning experience, and we encourage you to actively engage with the course materials, participate in discussions, and take full advantage of the resources available to you.

Thank you for choosing {course} as your pathway to enhancing your personal security awareness and skills. We look forward to supporting you on this educational journey and helping you achieve your goals.

Welcome aboard, and let's embark on this empowering learning adventure together!\n\n\nYou have made a successful payment of Amount : ₹{amount}.'''

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,[email])



# @login_required(login_url='/login')
def Articles(request):
    context = {}
    return render(request,'tango/newsletter.html',context)

@login_required(login_url='/login')
def Help(request):
    if request.method == 'POST':
        name = request.user.username
        email = request.user.email
        message = request.POST['message']
            
        send_notification_to_support(name, email, message)
        send_confirmation_email(name, email)
        return redirect('profile')
    
    return render(request,'tango/help.html')
       
    
@login_required(login_url='/login')
def Profile(request):
    user = request.user.userprofile
    form = ProfileForm(instance=user)
    context = {'form':user.profileid}
    return render(request,'tango/profile.html',context)

@login_required(login_url='/login')
def UpdateProfile(request,slug):
    user = UserProfile.objects.get(profileid=slug)
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    context = {'form':form}
    return render(request,'tango/updateprofile.html',context)

@login_required(login_url='/login')
def PaymentPage(request,slug):
    course = Course.objects.get(slug=slug)
    user = request.user
    action = request.GET.get('action')
    couponcode = request.GET.get('couponcode')
    couponcode_message = ''
    coupon = None
    order = None
    payment = None
    error = None
    gst_display = 0
    amount_display = 0
    try:
        user_course = UserCourse.objects.get(user = user  , course = course)
        return redirect('course',slug=slug)
    except:
        pass

    amount=None
    if error is None: 
        price = int((course.price - course.discount) * 100)
        gst = int(price * 0.18)
        print('Gst : ',gst)
        amount = price + gst
        print("amount : ",amount)
        gst_display = format(gst/100, '.2f')
        amount_display = format(amount/100, '.2f')
    
    if couponcode:
        amount = None
       
        try:
            coupon = CouponCode.objects.get(course=course,code=couponcode)
            price = int((course.price - course.discount) * 100)
            price = price - (coupon.discount * 100)
            gst = int(price * 0.18)
            print('Gst : ',gst)
            amount = price + gst
            print("amount : ",amount)
            gst_display = format(gst/100, '.2f')
            amount_display = format(amount/100, '.2f')

            # print(amount)
        except:
            couponcode_message = 'Invalid Coupon Code!'
            print('Code is Invalid!')

    if course.price ==0:
        userCourse = UserCourse(user = user , course = course)
        userCourse.save()
        return redirect('home')   
                # enroll direct
    
    if action == 'create_payment':
            currency = "INR"
            notes = {
                "email" : user.email, 
                "name" : f'{user.username}',
                "course" : course.name,
            }
            reciept = f"TSoC-{int(time())}"
            order = client.order.create(
                {'receipt' :reciept , 
                'notes' : notes , 
                'amount' : amount ,
                'currency' : currency
                }
            )

            payment = Payment()
            payment.user  = user
            payment.course = course
            payment.order_id = order.get('id')
            payment.code = couponcode
            payment.save()

    context = {
            "course" : course , 
            "order" : order, 
            "payment" : payment, 
            "user" : user , 
            "error" : error,
            "coupon":coupon,
            "couponcode_message":couponcode_message,
            "amount":amount_display,
            "gst":gst_display,
    }
    return render(request,'tango/payment.html',context)

def LoginPage(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=name,password=password)
            if user is not None:
                
                login(request,user)
                ip = request.session.get('ip',0)
                ip_before = IpTrack.objects.filter(user=request.user)
                ips = []
                for i in ip_before:
                    ips.append(i.ip_address)

                if ip in ips: 
                    return redirect('home')
                
                else:
                    track = IpTrack(user=request.user,ip_address=ip)
                    track.save()
                    return redirect('home')
            else:
                messages.error(request, 'Invalid password.')
                return render(request,'tango/loginpage.html',{'form':form})

        else:
            # messages.error(request, 'Invalid username or password.')
            return render(request,'tango/loginpage.html',{'form':form})
        
    return render(request,'tango/loginpage.html',{'form':form})        

def send_confirmation_register(name, email):
    
    subject = "Welcome to Tango Six O'clock"
    message = f'''Dear {name},\n\n

Welcome to TangoSixOclock, your gateway to a world of learning and awareness. We are thrilled to have you on board as a part of our community.

At TangoSixOclock, we are committed to providing a platform for Israeli Counter Crime Education, a crucial aspect of our lives today. This education encompasses a range of strategies and knowledge that are designed to empower individuals to protect themselves, their families, and their communities in an ever-changing world. Understanding and implementing Israeli Counter Crime Education not only enhances personal safety but also fosters a sense of confidence and preparedness in our daily lives.

By joining our website, you are taking the first step towards embracing this valuable education and becoming an advocate for safety and security. We are dedicated to providing you with resources, insights, and a supportive community as you embark on this journey.

We look forward to seeing you thrive within the TangoSixOclock community and making a positive impact in your own life and the lives of those around you.

Once again, welcome to TangoSixOclock!

Best regards,
The TangoSixOclock Team'''


    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,[email])

def Register(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        if pass1 == pass2:
            if form.is_valid():
                user = User.objects.create_user(username=username, email=email, password=pass1)
                print('ok')
                try:
                    nm = form.cleaned_data.get('fullname')
                    ph = form.cleaned_data.get('phone')
                    inst = form.cleaned_data.get('institude')
                    prof = form.cleaned_data.get('profession')
                    loc = form.cleaned_data.get('location')
                    dob = form.cleaned_data.get('dob')
                    gn = form.cleaned_data.get('sex')
                    full_name = str(nm)
                    first_name = full_name.replace(" ", "")
                    random_letters_first_name = random.sample(first_name[1:], 2)
                    result = first_name[0] + ''.join(random_letters_first_name) 
                    current_datetime = datetime.now()
                    token_format = "{:02d}{:02d}{:02d}{:02d}{:02d}{:02d}".format(
                        current_datetime.day,
                        current_datetime.month,
                        current_datetime.year % 100,
                        current_datetime.hour,
                        current_datetime.minute,
                        current_datetime.second
                    )

                    token = result.upper() + token_format
                    print('ok1')
                    fm = UserProfile(user=user,name=nm,phone=ph,sex=gn,dob=dob,profileid=token,institude=inst,profession=prof,location=loc,created_at=timezone.now())
                    fm.save()
                    print('ok2')
                    # send_confirmation_register(nm,email)
                    return redirect('loginpage')
                
                except:
                    return render(request,'tango/register.html',{'form':form})

        else:
            return render(request,'tango/register.html',{'form':form})
        
    return render(request,'tango/register.html',{'form':form})

def LogoutPage(request):
    logout(request)
    return redirect('home')
    
# @login_required(login_url='/login')
@csrf_exempt
def verifyPayment(request):
    
    if request.method == "POST":
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            pay = client.payment.fetch(razorpay_payment_id)

            amount = pay['amount'] / 100  

            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id  = razorpay_payment_id
            payment.status =  True
            
            userCourse = UserCourse(user = payment.user , course = payment.course, code = payment.code)
            userCourse.save()
            #send_confirmation_payment(request.user.userprofile.name,request.user.email,payment.course,amount)
            payment.user_course = userCourse
            payment.amount = amount
            payment.save()
            coupon = CouponCode.objects.all()
            for i in coupon:
                coun = UserCourse.objects.filter(code=i.code).count()
                con = CouponCode.objects.get(code=i.code)
                con.count = coun
                con.save()

            return redirect('home')

        except:
            return HttpResponse("Invalid Payment Details")
    
    # return render(request,'tango/verify.html')

@login_required(login_url='/login')
def News(request):
    # context = {'data':0}
    return render(request,'tango/news.html')

def TermsCondition(request):
    context = {'data':0}
    return render(request,'tango/term_and_condition.html',context)

def ReturnPolicy(request):
    context = {'data':0}
    return render(request,'tango/return_policy.html',context)

def PrivacyPolicy(request):
    context = {'data':0}
    return render(request,'tango/privacy_policy.html',context)

def TestimonialPolicy(request):
    context = {'data':0}
    return render(request,'tango/testimonial_policy.html',context)


@login_required(login_url='/login')
def watch(request,slug,pk):
    chapter = Chapter.objects.get(slug=slug)
    quiz_link = False
    print('heloo')
    ch = chapter.slug
    chapter = Chapter.objects.get(slug=slug,serial_number=pk)
    course = Course.objects.all()
    cor = chapter.course.slug
    serial_number = request.GET.get('lecture')
    print('helo')
    video = Video.objects.get(slug=slug)
    if video.serial_number == chapter.number_of_videos:
        quiz_link = True

    user = request.user
    
    try:
        if chapter.is_preview is False:
            user_course = UserCourse.objects.get(user = user  , course = course)

        else:
            print('pass')
    except:
        return redirect('payment',slug='tsoc_delta')

    context = {
        "course" : course , 
        "ch":ch,
        "quiz_link":quiz_link,
        "cor":cor,
        "video" : video, 
    }
    return render(request,'tango/watch-video.html',context)

@login_required(login_url='/login')
def adminPage(request):
    if request.user.is_superuser is False:
        return redirect('home')

    if request.method == "POST":
        database = request.POST['database']

        if database == 'user':
            return redirect('userpage')

        if database == 'CSVUser':
            return redirect('upload')
        
        if database == 'payment':
            return redirect('paymentDetail')

        if database == 'coupon':
            return redirect('couponpage') 
        
        if database == 'couponuser':
            return redirect('couponuserpage')

        if database == 'profile':
            return redirect('profilepage') 

        if database == 'select':
            print(database) 


    context = {}
    return render(request,'tango/admin/admin.html',context)

def PaymentDetail(request):
    if request.user.is_superuser is False:
        return redirect('home')
    payments = Payment.objects.all().order_by("date")
    context =  {
                'payments' : payments,
             }
    return render(request,'tango/admin/paymentdetail.html',context)

# Profile Admin
def ProfilePage(request):
    if request.user.is_superuser is False:
        return redirect('home')
    profiles = UserProfile.objects.all().order_by("-created_at") # Get all user
    context = {'profiles':profiles,}
    return render(request,'tango/admin/profilepage.html',context)

def DeleteProfilePage(request,pk):
    if request.user.is_superuser is False:
        return redirect('home')
    form = UserProfile.objects.get(id=pk)
    if request.method == "POST":
        form.delete()
        return redirect('profilepage')

    context = {'form':form}
    return render(request,'tango/admin/deleteprofile.html',context)

# User Admin
def UserPage(request):
    if request.user.is_superuser is False:
        return redirect('home')
    users = User.objects.all()
    context = {'users':users}
    return render(request,'tango/admin/userpage.html',context)

def DeleteUserPage(request,pk):
    if request.user.is_superuser is False:
        return redirect('home')
    form = User.objects.get(id=pk)
    if request.method == "POST":
        form.delete()
        return redirect('userpage')

    context = {'form':form}
    return render(request,'tango/admin/deleteuser.html',context)

# Coupon Admin
def CouponPage(request):
    if request.user.is_superuser is False:
        return redirect('home')
    coupon = CouponCode.objects.all()
    context = {'coupons':coupon}
    return render(request,'tango/admin/couponpage.html',context)

def CreateCouponPage(request):
    if request.user.is_superuser is False:
        return redirect('home')
    form = CouponForm()
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('couponpage')
        
    context = {'form':form}
    return render(request,'tango/admin/createcoupon.html',context)

def UpdateCouponPage(request,pk):
    if request.user.is_superuser is False:
        return redirect('home')
    coupon = CouponCode.objects.get(id=pk)
    form = CouponForm(instance=coupon)
    if request.method == 'POST':
        form = CouponForm(request.POST,instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('couponpage')
    context = {'form':form}

    return render(request,'tango/admin/updatecoupon.html',context)

def DeleteCouponPage(request,pk):
    if request.user.is_superuser is False:
        return redirect('home')
    form = CouponCode.objects.get(id=pk)
    if request.method == "POST":
        form.delete()
        return redirect('couponpage')

    context = {'form':form}
    return render(request,'tango/admin/deletecoupon.html',context)


# Coupon User Admin
def CouponUserPage(request):
    if request.user.is_superuser is False:
        return redirect('home')
    coupon = CouponCode.objects.all()
        
    context = {'coupons':coupon}
    return render(request,'tango/admin/couponuserpage.html',context)

def send_confirmation_score(name, email,score,chapter):
    
    subject = 'Chapter Completion Mail'
    message = f"Dear {name},\n\nYou have completed the {chapter} chapter successfully with a quiz percentage of {score}. You can move on to the next chapter."

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,[email])

@login_required(login_url='/login')
def Quiz(request,cor,ch):
    questions = Questions.objects.filter(course__slug=cor, chapter__slug=ch)
    random_questions = random.sample(list(questions), min(6, questions.count()))

    ques_list = []

    for question in random_questions:
        ques_list.append(question)

    questions_with_answers = []
    total = 0
    marks = 0

    for question in ques_list:
        answers = Answers.objects.filter(question=question)
        questions_with_answers.append((question, answers))
        total += 1
    
    if request.method == 'POST':
        print(request.POST)
        for key, value in request.POST.items():
            if not key == 'csrfmiddlewaretoken':
                question = Questions.objects.get(question=key,chapter__slug=ch)
                if question.answer == value:
                    marks += 1
                
        
        score = (marks/total) * 100
        return redirect('quiz_score',cor=cor,ch=ch,score=int(score))

    context = {'questions_with_answers':questions_with_answers}
    return render(request,'tango/quiz.html',context)

@login_required(login_url='/login')
def QuizScore(request,cor,ch,score):
    profile = request.user.userprofile
    if profile.chapter == 4 and profile.name is None:
        return redirect('update-profile')
    
    chapter = Chapter.objects.get(slug=ch)
    course = Course.objects.get(slug=cor)
    No = int(chapter.serial_number)
    next = False
    current_date = datetime.now().strftime('%d-%m-%Y')
    if score >= 80:
        No += 1
        if No == course.numbers_of_chapter:
            user = UserCourse.objects.get(user=request.user,course=course)
            if user.course_complete:
                return redirect('complete_course')
            
            else:
                user.course_complete = True
                user.complete_date = current_date
                user.save()
            return redirect('complete_course')
        else:
            user = UserProfile.objects.get(user=request.user)
            user.chapter = No
            user.save()
            next = True
            send_confirmation_score(request.user.username,request.user.email,score,chapter)

    context = {'score':score,"next":next,"cor":cor,"ch":ch}
    return render(request,'tango/quiz_score.html',context)

@login_required(login_url='/login')
def CompleteCourse(request):
    if request.method == "POST":
        user = request.user
        email = user.email
        ph = user.userprofile.phone
        intrest = UpcomingCourse(user=user,email=email,phone=ph)
        intrest.save()

    return render(request,'tango/complete_course.html')


@login_required(login_url='/login')
def Certificate(request):
    if request.user.is_authenticated:
        user = request.user

        profile = user.userprofile.profileid
        name = user.userprofile.name
        usercourse = UserCourse.objects.get(user=user)
        date_com = usercourse.complete_date
        print(name,profile,date_com)

    return render(request,'tango/certificate.html',{'profile':profile,'name':name,'date':date_com})

def AutoPayment(request):
    if request.user.is_superuser is False:
        return redirect('home')

    action = request.GET.get('action')
    payments = Payment.objects.all().values()
    df = pd.DataFrame(payments)
    print(df)
    csv_dir = os.path.join(settings.BASE_DIR, 'csv_files')
    os.makedirs(csv_dir, exist_ok=True)

    file_path = os.path.join(csv_dir, 'payment.csv')
    df.to_csv(file_path, index=False)

    if action == 'download':
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=payment.csv'
            
            return response
        
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        hello = request.POST.get('course')
        if hello == "frieren":
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                print(csv_file)
                df = pd.read_csv(csv_file)
                print(df)
                for row in df.index:
                    payment = Payment()
                    payment.order_id = df.iloc[row,1]
                    payment.payment_id = df.iloc[row,2]
                    payment.amount = df.iloc[row,3]
                    payment.user = User.objects.get(id=df.iloc[row,5])
                    payment.code = df.iloc[row,6]
                    payment.course = Course.objects.get(id=df.iloc[row,7])
                    payment.date = df.iloc[row,8]
                    payment.status = df.iloc[row,9]
                    payment.save()
                    
                
                return redirect('autopayment')
        else:
            return HttpResponse('Wrong Password')
        
    return render(request,'tango/admin/autopayment.html', {'form': form})

def AutoQuestions(request):
    if request.user.is_superuser is False:
        return redirect('home')

    action = request.GET.get('action')
    questions = Questions.objects.all().values()
    df = pd.DataFrame(questions)
    print(df)
    csv_dir = os.path.join(settings.BASE_DIR, 'csv_files')
    os.makedirs(csv_dir, exist_ok=True)

    file_path = os.path.join(csv_dir, 'questions.csv')
    df.to_csv(file_path, index=False)

    if action == 'download':
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=questions.csv'
            
            return response
        
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        hello = request.POST.get('course')
        if hello == "frieren":
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                print(csv_file)
                df = pd.read_csv(csv_file)
                print(df)
                for row in df.index:
                    questions = Questions()
                    questions.course = Course.objects.get(id=df.iloc[row,1])
                    questions.chapter = Chapter.objects.get(id=df.iloc[row,2])
                    questions.question = df.iloc[row,3]
                    questions.answer = df.iloc[row,4]
                    questions.save()
                         
                return redirect('autoquestion')
        else:
            return HttpResponse('Wrong Password')
        
    return render(request,'tango/admin/autoquestion.html',{'form':form})

def AutoAnswers(request):
    if request.user.is_superuser is False:
        return redirect('home')

    action = request.GET.get('action')
    answers = Answers.objects.all().values()
    df = pd.DataFrame(answers)
    print(df)
    csv_dir = os.path.join(settings.BASE_DIR, 'csv_files')
    os.makedirs(csv_dir, exist_ok=True)

    file_path = os.path.join(csv_dir, 'answers.csv')
    df.to_csv(file_path, index=False)

    if action == 'download':
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=answers.csv'
            
            return response
        
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        hello = request.POST.get('course')
        if hello == "frieren":
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                print(csv_file)
                df = pd.read_csv(csv_file)
                print(df)
                for row in df.index:
                    answers = Answers()
                    answers.question = Course.objects.get(id=df.iloc[row,1])
                    answers.chapter = Chapter.objects.get(id=df.iloc[row,2])
                    answers.answer = df.iloc[row,3]
                    answers.is_correct = df.iloc[row,4]
                    answers.save()
                         
                return redirect('autoanswer')
        else:
            return HttpResponse('Wrong Password')
        
    return render(request,'tango/admin/autoanswer.html',{'form':form})

def AutoCouponCode(request):
    if request.user.is_superuser is False:
        return redirect('home')

    action = request.GET.get('action')
    couponcode = CouponCode.objects.all().values()
    df = pd.DataFrame(couponcode)
    print(df)
    csv_dir = os.path.join(settings.BASE_DIR, 'csv_files')
    os.makedirs(csv_dir, exist_ok=True)

    file_path = os.path.join(csv_dir, 'couponcode.csv')
    df.to_csv(file_path, index=False)

    if action == 'download':
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=couponcode.csv'
            
            return response
        
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        hello = request.POST.get('course')
        if hello == "frieren":
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                print(csv_file)
                df = pd.read_csv(csv_file)
                print(df)
                for row in df.index:
                    couponcode = CouponCode()
                    couponcode.code = df.iloc[row,1]
                    couponcode.count = df.iloc[row,2]
                    couponcode.name = df.iloc[row,3]
                    couponcode.pan_number = df.iloc[row,4]
                    couponcode.course = Course.objects.get(id=df.iloc[row,5])
                    couponcode.discount = df.iloc[row,6]
                    couponcode.phone = df.iloc[row,7]
                    couponcode.save()
                         
                return redirect('autocouponcode')
        else:
            return HttpResponse('Wrong Password')
        
    return render(request,'tango/admin/autocouponcode.html',{'form':form})

def AutoUserCourse(request):
    if request.user.is_superuser is False:
        return redirect('home')

    action = request.GET.get('action')
    usercourse = UserCourse.objects.all().values()
    df = pd.DataFrame(usercourse)
    print(df)
    csv_dir = os.path.join(settings.BASE_DIR, 'csv_files')
    os.makedirs(csv_dir, exist_ok=True)

    file_path = os.path.join(csv_dir, 'usercourse.csv')
    df.to_csv(file_path, index=False)

    if action == 'download':
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=usercourse.csv'
            
            return response
        
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        hello = request.POST.get('course')
        if hello == "frieren":
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                print(csv_file)
                df = pd.read_csv(csv_file)
                print(df)
                for row in df.index:
                    usercourse = UserCourse()
                    usercourse.user = User.objects.get(id=df.iloc[row,1])
                    usercourse.course = Course.objects.get(id=df.iloc[row,2])
                    usercourse.course_complete = df.iloc[row,3]
                    usercourse.code = df.iloc[row,4]
                    usercourse.complete_date = df.iloc[row,5]
                    usercourse.save()
                         
                return redirect('autousercourse')
        else:
            return HttpResponse('Wrong Password')
        
    return render(request,'tango/admin/autousercourse.html',{'form':form})

def AutoVideo(request):
    if request.user.is_superuser is False:
        return redirect('home')

    action = request.GET.get('action')
    videos = Video.objects.all().values()
    df = pd.DataFrame(videos)
    print(df)
    csv_dir = os.path.join(settings.BASE_DIR, 'csv_files')
    os.makedirs(csv_dir, exist_ok=True)

    file_path = os.path.join(csv_dir, 'videos.csv')
    df.to_csv(file_path, index=False)

    if action == 'download':
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=videos.csv'
            
            return response
        
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        hello = request.POST.get('course')
        if hello == "frieren":
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                print(csv_file)
                df = pd.read_csv(csv_file)
                print(df)
                for row in df.index:
                    video = Video()
                    video.chapter = Chapter.objects.get(id=df.iloc[row,1])
                    video.course = Course.objects.get(id=df.iloc[row,2])
                    video.title = df.iloc[row,4]
                    video.serial_number = df.iloc[row,5]
                    video.video_id = df.iloc[row,6]
                    video.slug = df.iloc[row,7]
                    video.save()
                         
                return redirect('autovideo')
        else:
            return HttpResponse('Wrong Password')
        
    return render(request,'tango/admin/autovideo.html',{'form':form})

# Chapters
def AutoChapter(request):
    if request.user.is_superuser is False:
        return redirect('home')

    action = request.GET.get('action')
    chapters = Chapter.objects.all().values()
    df = pd.DataFrame(chapters)
    print(df)
    csv_dir = os.path.join(settings.BASE_DIR, 'csv_files')
    os.makedirs(csv_dir, exist_ok=True)

    file_path = os.path.join(csv_dir, 'chapters.csv')
    df.to_csv(file_path, index=False)

    if action == 'download':
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=chapters.csv'
            
            return response
        
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        hello = request.POST.get('course')
        if hello == "frieren":
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                print(csv_file)
                df = pd.read_csv(csv_file)
                print(df)
                for row in df.index:
                    chapter = Chapter()
                    chapter.course = Course.objects.get(id=df.iloc[row,1])
                    chapter.title = df.iloc[row,2]
                    chapter.is_preview = df.iloc[row,4]
                    chapter.slug = df.iloc[row,5]
                    chapter.serial_number = df.iloc[row,6]
                    chapter.complete_chapter = df.iloc[row,7]
                    chapter.number_of_videos = df.iloc[row,8]
                    chapter.save()
                         
                return redirect('autochapter')
        else:
            return HttpResponse('Wrong Password')
        
    return render(request,'tango/admin/autochapter.html',{'form':form})

def AutoUser(request):
    if request.user.is_superuser is False:
        return redirect('home')

    action = request.GET.get('action')
    users = User.objects.all().values()
    df = pd.DataFrame(users)
    print(df)
    csv_dir = os.path.join(settings.BASE_DIR, 'csv_files')
    os.makedirs(csv_dir, exist_ok=True)

    file_path = os.path.join(csv_dir, 'users.csv')
    df.to_csv(file_path, index=False)

    if action == 'download':
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=users.csv'
            
            return response
        
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        hello = request.POST.get('course')
        if hello == "frieren":
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                print(csv_file)
                df = pd.read_csv(csv_file)
                print(df)
                for row in df.index:
                    User.objects.create_user(username=df.iloc[row,4],email=df.iloc[row,7],password='tango6Oclock')        
                return redirect('autouser')
        else:
            return HttpResponse('Wrong Password')
        
    return render(request,'tango/admin/autouser.html',{'form':form})

def AutoUserProfile(request):
    if request.user.is_superuser is False:
        return redirect('home')

    action = request.GET.get('action')
    usersprofile = UserProfile.objects.all().values()
    df = pd.DataFrame(usersprofile)
    print(df)
    csv_dir = os.path.join(settings.BASE_DIR, 'csv_files')
    os.makedirs(csv_dir, exist_ok=True)

    file_path = os.path.join(csv_dir, 'usersprofile.csv')
    df.to_csv(file_path, index=False)

    if action == 'download':
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=usersprofile.csv'
            
            return response
        
    form = CSVUploadForm()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        hello = request.POST.get('course')
        if hello == "frieren":
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                print(csv_file)
                df = pd.read_csv(csv_file)
                print(df)
                for row in df.index:
                    userprofile = UserProfile()
                    userprofile.user = User.objects.get(id=df.iloc[row,1])
                    userprofile.name = df.iloc[row,2]
                    userprofile.phone = df.iloc[row,3]
                    userprofile.sex = df.iloc[row,4]
                    userprofile.dob = df.iloc[row,5]
                    userprofile.profileid = df.iloc[row,6]
                    userprofile.chapter = df.iloc[row,7]
                    userprofile.institude = df.iloc[row,8]
                    userprofile.profession = df.iloc[row,9]
                    userprofile.location = df.iloc[row,10]
                    userprofile.created_at = df.iloc[row,11]
                    userprofile.save()        
                return redirect('autouserprofile')
        else:
            return HttpResponse('Wrong Password')
        
    return render(request,'tango/admin/autouserprofile.html',{'form':form})
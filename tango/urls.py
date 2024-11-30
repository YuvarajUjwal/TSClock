from django.urls import path
from . import views
from .forms import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.About,name='about'),
    path('course/<str:slug>/',views.Courses,name='course'),
    path('contact/',views.Contact,name='contact'),
    path('support/',views.Help,name='help'),
    path('blog/',views.Articles,name='newsletter'),
    path('news/',views.News,name='news'),
    path('programs/',views.Programs,name='Programs'),
    path('faqs/',views.Faq,name='Faq'),
    path('profile/',views.Profile,name='profile'),
    path('update-profile/<str:slug>/',views.UpdateProfile,name='update-profile'),
    path('complete_course/',views.CompleteCourse,name='complete_course'),
    path('certificate/',views.Certificate,name='certificate'),
    
    path('payment/<str:slug>/',views.PaymentPage,name='payment'),
    path('verify_payment/', views.verifyPayment , name = 'verify_payment'),
    path('adminPage/',views.adminPage,name='adminpage'),
  
    path('reset_password/',views.CustomPasswordResetView.as_view(),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="tango/reset_password_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="tango/reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="tango/reset_password_done.html"),name="password_reset_complete"),

    path('login/',views.LoginPage,name='loginpage'),
    path('register/',views.Register,name='register'),
    path('logout/',views.LogoutPage,name='logoutpage'),

    path('terms_and_conditions/',views.TermsCondition,name='term_condition'),
    path('refund_policy/',views.ReturnPolicy,name='return_policy'),
    path('privacy_policy/',views.PrivacyPolicy,name='privacy_policy'),
    path('no_testimony_policy/',views.TestimonialPolicy,name='testimonial_policy'),

    # path('playlist/<str:slug>/',views.playlist,name='playlist'),
    path('watch/<str:slug>/<int:pk>/',views.watch,name='watch'),

    path('userpage/',views.UserPage,name='userpage'),
    path('deleteuserpage/<int:pk>/',views.DeleteUserPage,name='deleteuserpage'),

    path('couponpage/',views.CouponPage,name='couponpage'),
    path('createcouponpage/',views.CreateCouponPage,name='createcouponpage'),
    path('updatecouponpage/<int:pk>/',views.UpdateCouponPage,name='updatecouponpage'),
    path('deletecouponpage/<int:pk>/',views.DeleteCouponPage,name='deletecouponpage'),

    path('profilepage/',views.ProfilePage,name='profilepage'),
    path('deleteprofilepage/<int:pk>/',views.DeleteProfilePage,name='deleteprofilepage'),

    path('couponuserpage/',views.CouponUserPage,name='couponuserpage'),

    path('quiz/<str:cor>/<str:ch>/',views.Quiz,name='quiz'),
    path('quiz_score/<str:cor>/<str:ch>/<int:score>/',views.QuizScore,name='quiz_score'),
   
    path('payment_detail/',views.PaymentDetail,name= 'paymentDetail'),

    path('upload/',views.upload,name= 'upload'),

    path('autopayment/',views.AutoPayment,name= 'autopayment'),
    path('autoquestion/',views.AutoQuestions,name= 'autoquestion'),
    path('autoanswer/',views.AutoAnswers,name= 'autoanswer'),
    path('autocouponcode/',views.AutoCouponCode,name= 'autocouponcode'),
    path('autousercourse/',views.AutoUserCourse,name= 'autousercourse'),
    path('autouser/',views.AutoUser,name= 'autouser'),
    path('autouserprofile/',views.AutoUserProfile,name= 'autouserprofile'),
    path('autochapter/',views.AutoChapter,name= 'autochapter'),
    path('autovideo/',views.AutoVideo,name= 'autovideo'),
]

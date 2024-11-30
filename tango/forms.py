from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re
from .models import *
from django.forms import ValidationError
from datetime import datetime
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField

class CustomPasswordResetForm(PasswordResetForm):
    username = forms.CharField(max_length=254)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() is False:
            raise forms.ValidationError('This email address does not exist.')
        
        return email

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if username and email:
            # Check if both email and username belong to the same user
            user = User.objects.filter(username=username, email=email).first()
            if not user:
                raise ValidationError(_("No user found with the specified email and username combination."))
            
            # You can also check if the user is active or meets other conditions here

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)

    def clean_username(self):
        # cleaned_data = super().clean()
        username = self.cleaned_data.get('username')
        # password = cleaned_data.get('password')
        if username and not username.isalnum():
            raise forms.ValidationError("Username should be alphanumeric only.")
        
        if User.objects.filter(username=username).exists() is False:
            raise ValidationError("Username Doesn't exist.")
        return username


class RegistrationForm(forms.Form):
    fullname = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    dob = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)
    institude = forms.CharField(max_length=60)
    profession = forms.CharField(max_length=100)
    location = forms.CharField(max_length=50)
    sex = forms.CharField(max_length=20)

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')

        # Check if the fullname contains only alphabetic characters
        if not fullname.replace(' ', '').isalpha():
            raise forms.ValidationError('Full name must contain only alphabetic characters.')

        # Check if the length of the fullname is not greater than 25 characters
        if len(fullname) > 70:
            raise forms.ValidationError('Full name must be at most 70 characters long.')

        return fullname

    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username) < 6:
            raise forms.ValidationError('Username should be more than 6 letters.')
        
        if len(username) > 20:
            raise forms.ValidationError('Username should not be more than 20 letters.')
            
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already in use.')
            
        if username and not username.isalnum():
            raise forms.ValidationError("Username should be alphanumeric only.")
            
        return username
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
            
            
        if not re.match(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', email):
            raise ValidationError("Invalid email address.")
            
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        # Check if the password contains at least one special character, one uppercase character, and two numeric characters
        if not re.search(r'^(?=.*[!@#$%^&*()-_=+`~,.<>/?;:{}[\]"])', password1):
            raise forms.ValidationError('Password must contain at least one special character.')

        if not re.search(r'^(?=.*[A-Z])', password1):
            raise forms.ValidationError('Password must contain at least one uppercase character.')

        if not re.search(r'^(.*?\d){2,}', password1):
            raise forms.ValidationError('Password must contain at least two numeric characters.')
        
        if len(password1) < 10:
            raise forms.ValidationError('Password must be at least 10 characters long.')

        return password1
    
    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')

        # Check if the password contains at least one special character, one uppercase character, and two numeric characters
        if not re.search(r'^(?=.*[!@#$%^&*()-_=+`~,.<>/?;:{}[\]"])', password2):
            raise forms.ValidationError('Password must contain at least one special character.')

        if not re.search(r'^(?=.*[A-Z])', password2):
            raise forms.ValidationError('Password must contain at least one uppercase character.')

        if not re.search(r'^(.*?\d){2,}', password2):
            raise forms.ValidationError('Password must contain at least two numeric characters.')
        
        if len(password2) < 10:
            raise forms.ValidationError('Password must be at least 10 characters long.')

        return password2

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        # Check if the phone number contains only numeric characters
        if not phone.isdigit():
            raise forms.ValidationError('Phone number must contain only numeric characters.')

        # Check if the length of the phone number is between 10 and 15 characters
        if len(phone) < 10 or len(phone) > 14:
            raise forms.ValidationError('Phone number must be between 10 and 14 characters long.')

        return phone
    
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')

        # Check if the date of birth matches the format dd/mm/yyyy
        try:
            datetime.strptime(dob, '%d/%m/%Y')
        except ValueError:
            raise forms.ValidationError('Date of birth must be in dd/mm/yyyy format.')
        
        return dob
    
    def clean_institute(self):
        institute = self.cleaned_data.get('institute')

        # Check if the institute contains only alphabetic characters
        if not institute.replace(' ', '').isalpha():
            raise forms.ValidationError('Institute must contain only alphabetic characters.')

        # Check if the length of the institute is not greater than 30 characters
        if len(institute) > 30:
            raise forms.ValidationError('Institute name must be at most 30 characters long.')

        return institute
    
    def clean_profession(self):
        profession = self.cleaned_data.get('profession')

        # Check if the institute contains only alphabetic characters
        if not profession.replace(' ', '').isalpha():
            raise forms.ValidationError('Designation must contain only alphabetic characters.')

        # Check if the length of the institute is not greater than 30 characters
        if len(profession) > 75:
            raise forms.ValidationError('Designation name must be at most 75 characters long.')

        return profession
    
    def clean_location(self):
        location = self.cleaned_data.get('location')

        # Check if the location contains only alphabetic characters
        if location and not location.replace(' ', '').isalnum():
            raise forms.ValidationError("Location should be alphanumeric only.")

        # Check if the length of the location is not greater than 30 characters
        if len(location) > 30:
            raise forms.ValidationError('Location must be at most 30 characters long.')

        return location
    
    def clean_sex(self):
        sex = self.cleaned_data.get('sex')

        # Check if the sex field is empty
        if not sex:
            raise forms.ValidationError('Select your gender.')

        return sex

class ContactForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = ContactDetail
        fields = ('name','email','phone','message','captcha')

        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ('user','profileid','chapter')

class CouponCodeForm(forms.ModelForm):
    class Meta:
        model = CouponCode
        fields = '__all__'

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
    
class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = '__all__'
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ChapterForm, self).__init__(*args, **kwargs)
        
        # Fetch available courses from the database
        self.fields['course'].queryset = Course.objects.all()

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['chapter', 'course', 'thumbnail', 'title', 'serial_number', 'video_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['chapter'].queryset = Chapter.objects.all()

        self.fields['course'].queryset = Course.objects.all()

class CouponForm(forms.ModelForm):
    class Meta:
        model = CouponCode
        fields = '__all__'
        exclude = ('count',)
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        
        # Fetch available courses from the database
        self.fields['course'].queryset = Course.objects.all()

class CSVUploadForm(forms.Form):
    class Meta:
        model = CSVFile
        fields = ['file','course'] 
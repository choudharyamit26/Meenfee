import re
from django.db.models import Q

from rest_framework.serializers import(
     ModelSerializer,
     EmailField, 
     CharField,
     DecimalField,
     ValidationError,
     SerializerMethodField,
     Serializer,
     )
from meenfee.models import UserOtherInfo

from django.contrib.auth import get_user_model

from rest_framework_jwt.settings import api_settings


from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

#reset password

from django.conf import settings
#this is imported for custom templates in email confirmation
from accounts.password_reset_form import MyPasswordResetForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class UserDetailSerializer(ModelSerializer):
    name = SerializerMethodField()

    def get_name(self,instance):
        return instance.first_name +" "+ instance.last_name

    class Meta:
        model = User
        fields = ['username','name']


class UserCreateSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    firstname       = CharField()
    lastname        = CharField() 
    email           = EmailField()
    phonenumber     = CharField()
    idcard          = CharField(allow_blank=True)
    usertype        = CharField()
    user_address    = CharField()
    user_address_lat = DecimalField(max_digits=10,decimal_places=5,default=0.0)
    user_address_long = DecimalField(max_digits=10,decimal_places=5,default=0.0)
    current_language  = CharField()
    profile_image_s3 = CharField(allow_blank=True)
    locality            = CharField(allow_blank=True)
    data =            SerializerMethodField()

    class Meta:
        model = User
        fields = ['firstname', 'lastname','email', 'password','token','phonenumber', 'locality',
        'idcard','usertype','user_address','user_address_lat','user_address_long','current_language','profile_image_s3','data']
        extra_kwargs = {'password': {'write_only': True}}


    def validate_phonenumber(self, phonenumber):
        phonenumber_String = str(phonenumber)
        phonenumber_cleaned = phonenumber_String.replace(" ","")
        user_qs = UserOtherInfo.objects.filter(phone__iexact=phonenumber_cleaned)
        if user_qs.exists():
            raise ValidationError('User with this phonenumber already exists')
        return phonenumber

    def validate_email(self, email):
        allowedDomains = [
        "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
        "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
        "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
        "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
        "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
        "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
        "yandex.com","iname.com" , "yopmail.com","rediffmail.com",
        ]
        domain = email.split("@")[1]
        if domain not in allowedDomains:
            raise ValidationError('Invalid email address')
        user_qs = User.objects.filter(email__iexact=email)
        if user_qs.exists():
            raise ValidationError('User with this Email already exists')
        return email

    def validate_password(self, password):
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters')
        return password

    def create(self, validatedData):

        user_data ={
            "username"          : "",
            "first_name"        : "",
            "last_name"         : "",
            "email"             : "",
            "phone"             : "",
            "user_address"      : "",
            "user_address_lat"  : "",
            "user_address_long" : "",
            "profile_image"     : "",
            "idcard"            : "",
            "bio"               : "",
            "social_login"      : False,
            "usertype"          : ""
            }


        email               = validatedData['email']
        password            = validatedData['password']
        firstname           = validatedData['firstname']
        lastname            = validatedData['lastname']
        phonenumber         = validatedData['phonenumber']
        idcard              = validatedData['idcard']
        usertype            = validatedData['usertype']
        emailuser           = email.split("@")[0]
        username            = emailuser+phonenumber
        user_address        = validatedData['user_address']
        user_address_lat    = validatedData['user_address_lat']
        user_address_long   = validatedData['user_address_long']
        current_language    = validatedData['current_language']
        profile_image_s3    = validatedData['profile_image_s3']
        locality            = validatedData['locality']


        email_lowercase     = email.lower()
        phonenumber_String = str(phonenumber)
        phonenumber_cleaned = phonenumber_String.replace(" ","")
        username = email_lowercase + phonenumber_cleaned



        userObj = User(email=email_lowercase,username=username,first_name=firstname,last_name=lastname)

        userObj.set_password(password)
        userObj.save()
        phonenumber_String = str(phonenumber)
        phonenumber_cleaned = phonenumber_String.replace(" ","")
        user_address_lat_rounded = round(user_address_lat,10)
        user_address_long_rounded = round(user_address_long,10)
        if usertype == "provider" or usertype == "Provider":
            UserOtherInfo.objects.create(
                user=userObj, 
                phone = phonenumber_cleaned,
                idcard=idcard,
                is_phone_verified=True, 
                usertype=usertype,
                switched_to_provider=True,
                user_address=user_address,
                user_address_lat=user_address_lat_rounded,
                user_address_long=user_address_long_rounded,
                current_language=current_language,
                profile_image_s3 = profile_image_s3,
                locality        =   locality
                )
        else:
            UserOtherInfo.objects.create(
                user=userObj,
                idcard=idcard,
                phone = phonenumber_cleaned,
                is_phone_verified=True,
                usertype=usertype,
                user_address=user_address,
                user_address_lat=user_address_lat_rounded,
                user_address_long=user_address_long_rounded,
                current_language=current_language,
                profile_image_s3  = profile_image_s3,
                locality    =   locality
            )
        
        payload = jwt_payload_handler(userObj)
        token = jwt_encode_handler(payload)
        
        user_data['username'] = username
        user_data['first_name'] = firstname
        user_data['last_name'] = lastname
        user_data['email'] = email_lowercase
        user_data['phone'] = phonenumber_cleaned
        user_data['user_address'] = user_address
        user_data['user_address_lat'] = user_address_lat
        user_data['user_address_long'] = user_address_long
        user_data['profile_image'] = profile_image_s3
        user_data['idcard'] = idcard
        user_data['usertype'] = usertype
        
        final_dict = {
            "token" : token,
            "data" : user_data
            }
        
        validatedData['token'] = token
        validatedData['data'] = user_data
        return validatedData
    
    
    def get_data(self,validatedData):

        user_data ={
            "username"          : "",
            "first_name"        : "",
            "last_name"         : "",
            "email"             : "",
            "phone"             : "",
            "user_address"      : "",
            "user_address_lat"  : "",
            "user_address_long" : "",
            "profile_image"     : "",
            "idcard"            : "",
            "bio"               : "",
            "social_login"      : False,
            "usertype"          : "",
            }

        email               = validatedData['email']
        password            = validatedData['password']
        firstname           = validatedData['firstname']
        lastname            = validatedData['lastname']
        phonenumber         = validatedData['phonenumber']
        idcard              = validatedData['idcard']
        usertype            = validatedData['usertype']
        emailuser           = email.split("@")[0]
        username            = emailuser+phonenumber
        user_address        = validatedData['user_address']
        user_address_lat    = validatedData['user_address_lat']
        user_address_long   = validatedData['user_address_long']
        current_language    = validatedData['current_language']
        profile_image_s3    = validatedData['profile_image_s3']
        locality            = validatedData['locality']
        email_lowercase     = email.lower()
        phonenumber_String = str(phonenumber)
        phonenumber_cleaned = phonenumber_String.replace(" ","")
        username = email_lowercase + phonenumber_cleaned

        user_data['username'] = username
        user_data['first_name'] = firstname
        user_data['last_name'] = lastname
        user_data['email'] = email_lowercase
        user_data['phone'] = phonenumber_cleaned
        user_data['user_address'] = user_address
        user_data['user_address_lat'] = user_address_lat
        user_data['user_address_long'] = user_address_long
        user_data['profile_image'] = profile_image_s3
        user_data['idcard'] = idcard
        user_data['usertype'] = usertype
        
        return user_data


class ChangePasswordSerializer(Serializer):
    oldPassword = CharField(required=True)
    newPassword = CharField(required=True)

    def validate_oldPassword(self, password):
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters')
        return password
    def validate_newPassword(self, password):
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters')
        return password

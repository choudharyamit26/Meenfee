import csv
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse


from .forms import login_form,PasswordChangeForm,PasswordResetRequestForm,SetPasswordForm
from meenfee.models import UserOtherInfo
from django import template
from _operator import itemgetter
# from pip._vendor.requests.api import request
register = template.Library()
#from django.contrib.auth.forms import PasswordChangeForm

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


from django.views.generic import *
from django.template import loader
from django.core.mail import send_mail

from django.conf import settings

from myproject.settings import DEFAULT_FROM_EMAIL

from django.contrib.auth.tokens import default_token_generator

from rest_framework.exceptions import ValidationError
from services.models import *
from meenfee.models import *

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()
#from .permissions import IsAuthenticatedOrCreate

from decimal import *

from meenfee.api.serializers import *



@login_required(login_url='login/') 
def index(request):
    #return HttpResponse("Hello, world. You're at the Admin Panel.")
    # return render(request, 'main.html')
    return render(request, 'dashboard.html')
#     if request.method == "POST" and request.is_ajax():
#         print("====AJAX post request")
#         #return JsonResponse(data) =
#         ucmMainform = UOMConverterForm(request.POST)
#         pending_user = ucmMainform.save(commit=False)
#         pending_user.user_id = request.user.id
#         data = pending_user.save()
# 
#         return HttpResponse(data)  # return a html str
# 
#     elif request.method == 'POST' :
#         ucmMainform = UOMConverterForm(request.POST)
#         if ucmMainform.is_valid():
#             #temp = ucmMainform.cleaned_data.get('uom_id')
# 
#             pending_user = ucmMainform.save(commit=False)
#             pending_user.user_id = request.user.id
#             pending_user.save()
#            # ucmMainform.save()
#             return redirect('ucm:ucm_list')
# 
#         else:
# 
#             print(ucmMainform.errors.as_data())
# 
#     elif request.method == "GET" and request.is_ajax():
# 
#         data=ucmMainform.as_p()
#         return HttpResponse(data)  # return a html str
# 
#     else:
# 
#         return render(request, 'converter.html', {'ucmMainform': ucmMainform})

#@login_required(login_url='/adminpanel/login/')
@login_required()
def dashboard(request):
    usrcnt = User.objects.filter(Q(is_superuser=False) & ( Q(userotherinfo__usertype = 'provider') | Q(userotherinfo__usertype = 'requester'))).count()#.select_related('userotherinfo')
    provdCnt = User.objects.filter( Q(is_superuser=False) & ( Q(userotherinfo__usertype = 'provider') | Q(userotherinfo__usertype = 'Provider'))).count()
    reqCnt = User.objects.filter(Q(is_superuser=False) & Q(userotherinfo__usertype = 'requester')).count()
    contcnt = ContentMaster.objects.all().count()
    serviccnt= Service.objects.all().count()
    categorycnt = Category.objects.all().count()
    
    
    
    #print(usrcnt,contcnt,serviccnt,categorycnt)
        #.count()    
    data = {}
    data['user_count'] = usrcnt
    data['service_count'] = serviccnt
    data['category_count'] = categorycnt
    data['content_count'] = contcnt
    data['provider_count'] = provdCnt
    data['requester_count'] = reqCnt
    
    
    return render(request, 'dashboard.html',{'data':data})
    #return HttpResponse("Hello, world. You're at the Admin Panel.")
    
#default to your native language
#request.session['lang'] = 'tr'

# someone clicks the link to change to English
def switch_to_English_link(request):
    request.session['lang'] = 'en'

@login_required(login_url='login/')
def add_user(request):    
    user_id = request.user.id
    msg=[]   
    if request.method == 'POST':
        form = request.POST   
        try:    
            print("=====>Step2 ",form)
            email=form.get('email')        
            if email != "":           
                email = validate_email(email)              
            password= form.get('password')
            if password != "":           
                password = validate_password(password)
                
            phonenumber = form.get('phonenumber')
            if phonenumber != "":           
                phonenumber = validate_phonenumber(phonenumber)    
                
                print(form,"dmjkfksffslkfhfh")
                firstname = form.get('firstname')
                lastname = form.get('lastname')
                idcard = form.get('idcard')
                usertype = form.get('usertype')
                emailuser = email.split("@")[0]  
                username = emailuser+phonenumber 
                user_address = form.get('user_address')                    
                user_address_lat="111"        
                user_address_long="111"   
            
                userObj = User(email=email,username=username,first_name=firstname,last_name=lastname)    
                userObj.set_password(password)
                userObj.save()
           
                if usertype == "provider" or usertype == "Provider":
                    UserOtherInfo.objects.create(user=userObj, phone = phonenumber,
                    idcard=idcard,isphvarified=True, usertype=usertype,
                    switched_to_provider=True,user_address=user_address,
                    user_address_lat=user_address_lat,user_address_long=user_address_long)
                else:
                    UserOtherInfo.objects.create(user=userObj, phone = phonenumber,idcard=idcard,isphvarified=True,
                     usertype=usertype,user_address=user_address,
                    user_address_lat=user_address_lat,user_address_long=user_address_long)         # your code
                
                return HttpResponseRedirect('/adminpanel/userlist/?status=successful') 
        except Exception as e:
            print(e)
            errmsg= "Email/ Phone Already Exist!"
            msg.append(errmsg)
           
    return render(request, 'add-user.html',{'messages':msg})    

def validate_phonenumber(phonenumber):
        user_qs = UserOtherInfo.objects.filter(phone__iexact=phonenumber)
        if user_qs.exists():
            raise ValidationError('User with this phonenumber already exists')
        return phonenumber

def validate_email(email):   
    if email =='':
       raise ValidationError('Blank email address ')
    allowedDomains = [
    "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
    "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
    "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
    "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
    "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
    "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
    "yandex.com","iname.com"
    ]
    domain = email.split("@")[1]
    if domain not in allowedDomains:        
        raise ValidationError('Invalid email address')
    user_qs = User.objects.filter(email__iexact=email)
    print(user_qs)
    if user_qs.exists():
        raise ValidationError('User with this Email already exists')
    return email

def validate_password(password):
    if len(password) < 6:
        raise ValidationError('Password must be at least 6 characters')
    return password

# @register.filter(name='times') 
# def times(number):
#     return range(number)

@login_required()
def user_list(request):
    
    status= request.GET.get('status', None)
    
    #usrlist = User.objects.filter(is_superuser=False).select_related('userotherinfo')    
    #print(usrlist.query)
    provdlist = User.objects.filter( Q(is_superuser=False) & ( Q(userotherinfo__usertype = 'provider') | Q(userotherinfo__usertype = 'Provider')))
    
   # provdlist1 = User.objects.filter( Q(is_superuser=False) & ( Q(userotherinfo__usertype = 'provider') | Q(userotherinfo__usertype = 'Provider'))).all().select_related('service')
    
    #qs3 = Service.objects.filter(user__in=provdlist)
    #print(qs3,"========================>")
    
    #Q(service__isnull=False)
    prList = []
    for provdata in provdlist:
        prDict = {}
        user_id= provdata.id        
        qs1 = Service.objects.filter(user_id=user_id).count() 
        prDict['id']=provdata.id
        prDict['first_name']=provdata.first_name
        prDict['last_name']=provdata.last_name
        prDict['email']=provdata.email
        prDict['phone']=provdata.userotherinfo.phone
        prDict['date_joined']=provdata.date_joined
        prDict['service_count']=qs1 
        prList.append(prDict)
    #custlist = User.objects.filter(Q(is_superuser=False) & ( ~Q(userotherinfo__usertype = 'provider')))
    custlist = User.objects.filter(Q(is_superuser=False) & Q(userotherinfo__usertype = 'requester'))
    print(provdlist,"=========>Provider List")
   
#     qs4 = User.objects.filter(User)#.values_list('code', flat=True)
#    # qs5 = UserOtherInfo.objects.all().select_related('user')
#     print(qs5)
#     for j in qs5:
#         print(j.usertype)
#         print(j.user.username)
#     usrlist.__dict__
#     for i in usrlist:
#         print(i)
#     print(usrlist)
#     print("============>")
    
    
    
    data = {}    
    data['object_list'] = prList 
    data['cobject_list'] = custlist   
    if status=='successful':
        data['messages'] = ["User Successfully created"]
    
    return render(request, 'main.html', data)

@login_required()
def user_delete(request, id): 
    user_data = User.objects.get(id=id)
    user_data.delete()
    return HttpResponseRedirect('/adminpanel/userlist/')


@login_required()
def bulk_delete(request):
    import json
    msg=''
    if request.is_ajax():       
        selected_tests =request.POST['usr_list_ids']
        selected_tests=json.loads(selected_tests)
        print("fsfjdsjdffj=================================>",selected_tests)
        
        for i, test in enumerate(selected_tests):
            if test != '':
                User.objects.filter(id__in=selected_tests).delete()
                msg='Success'
        #return HttpResponseRedirect('/adminpanel/userlist/')
        success_dict={}
        success_dict['success_msg'] = "Successfully Deleted User"        
        data={}
        data['success']=1
        data['message']=msg 
        #return success_dict     
        return HttpResponse('Users deleted successfully! ')#(json.dumps(data))
    else:
        return HttpResponse('fail')  
    



# if request.is_ajax():
#         selected_tests = request.POST['test_list_ids']
#         selected_tests = json.loads(selected_tests)
#         for i, test in enumerate(selected_tests):
#             if test != '':
#                 Test.objects.filter(id__in=selected_tests).delete()
#         return HttpResponseRedirect('/test-management/test/')


# @login_required()
# def user_details(request, id):
#     user_data = User.objects.get(id=id)
#     print(user_data.first_name,"fhdshfdsdfhd")
#     print(user_data,"------------------------->test too")
#     
#     msg=[]
#     #data['cobject_list'] = custlist   
#     return render(request, 'user-details.html',{'messages':msg,'userData':user_data}) 



@login_required()
def user_details(request, id):
    user_data = User.objects.get(id=id)
    print(user_data.first_name,"fhdshfdsdfhd")
    print(user_data,"------------------------->test too")
    uoi_object = UserOtherInfo.objects.get(user=user_data)
    avg_rating = uoi_object.avg_rating_rounded
    
    user_featured = False
    
    try:
        Featured = FeaturedServiceProviders.objects.get(provider=user_data)
        user_featured = True
    except:
        pass
    
    
    service_qs = Service.objects.filter(user=user_data)
    if len(service_qs) == 0:
        final_reviews= []
    else:      
        reviews_list = []
        FinalQS = ServiceFeedback.objects.none()
        for service in service_qs:
            reviews = ServiceFeedback.objects.filter(service_id=service)
            print("<---------------reviews--------------------->",type(reviews))
            if len(reviews)!=0:
                serializer = ServiceFeedbackSerializer(reviews,many=True).data
                print("<==============Serializer--------------------?",serializer)
                for review_object in serializer:
                    reviews_list.append(review_object)
                    
        
        raw_reviews = []
        for review in reviews_list:
            tuple_object = (review['feedback_id'],review['rating'],review['feedback_date'],review['feedback_time'])
            raw_reviews.append(tuple_object)
            
        print("<--------------Raw Reviews Tuple---------------->",raw_reviews)
        sorted_reviews = sorted(raw_reviews,key=itemgetter(1,2,3),reverse=True)[:3]
        print("<--------------Sorted Tuple------------------->",sorted_reviews)
        
        
        review_id = [x[0] for x in sorted_reviews]
#         for review in sorted_reviews:
#             review_id.append(review[0][0])
        print("<------------Review IDS---------------->",review_id)
        final_reviews = []
        for review_ref in review_id:
            review_object = ServiceFeedback.objects.get(id=review_ref)
            print("<----------------review object--------->",review_object)
            review_serialized = ServiceFeedbackSerializer(review_object).data
            print("<-----------------Review Serialized------------->",review_serialized)
            final_reviews.append(review_serialized)
    msg=[]
    #data['cobject_list'] = custlist   
    return render(request, 'user-details.html',{'messages':msg,'userData':user_data,
                                                'top_reviews':final_reviews,'user_featured':user_featured,
                                                'avg_rating':avg_rating})





   




def login_user(request):
    loginform = login_form() 
    next = request.GET.get('next') 
    msg=[]  
    if request.method == 'GET' :         
        next = request.GET.get('next')   
    if request.method == 'POST':
        loginform = login_form(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']
            is_superuser= True
            user = authenticate(username=username, password=password,is_superuser=is_superuser)
            if user is not None:
                if user.is_active:
                    request.session['username'] = username
                    login(request, user)                   
                    if next is None:
                        return HttpResponseRedirect('/adminpanel/dashboard/')
                    else:                        
                        return HttpResponseRedirect(next) 
            else:
                print("----------------->> Here")
                errmsg="Please enter valid credentials!"
                msg.append(errmsg)
             
    loginform = login_form()        
    return render(request, 'login.html', {'loginform': loginform,'messages':msg})

@login_required()
def change_password(request):
    """It will access to admin can change password """
    if request.method == 'POST':
        change_password_form = PasswordChangeForm(request.user, request.POST)
        print(request.user)
        print(request.POST)
        if change_password_form.is_valid():
            user = change_password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/adminpanel/dashboard/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        change_password_form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'change_password_form': change_password_form})

@login_required()
def logout_site(request):
    """logout function it will delete session also"""
    logout(request)
    return HttpResponseRedirect('/adminpanel/login/')



def validating_email(email):   
    if email =='':
        return False
       #raise ValidationError('Blank email address ')
    allowedDomains = [
    "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
    "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
    "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
    "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
    "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
    "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
    "yandex.com","iname.com"
    ]
    domain = email.split("@")[1]
    if domain not in allowedDomains:        
        return False
        #raise ValidationError('Invalid email address')
    user_qs = User.objects.filter(email__iexact=email)    
    if user_qs.exists():
        return False        
        #raise ValidationError('User with this Email already exists')
    return True

def success_mail_send(request):
    return render(request, 'success_mail_send.html')
    


class ResetPasswordRequestView(FormView):
    """ Forgot password function, it will send email link which user has been register
        and user name also and link for reset password link in that mail
    """
    template_name = "forget_password.html"
    success_url =  '/adminpanel/login' #'/adminpanel/success_mail_send'
    form_class = PasswordResetRequestForm
#from django.core.validators import validate_email
    @staticmethod
    def validate_email_address(email):
        try:
            validating_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        
        forget_form = self.form_class(request.POST)
        if forget_form.is_valid():
            data = forget_form.cleaned_data["email_or_username"]
       
        if self.validate_email_address(data) is True:
            
            associated_users = User.objects.filter(Q(email=data) & Q(is_superuser=True)) 
            
            print(associated_users,'+++++++++++++++++Brajesh')
            
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'MeenFee',
                        'uid':  user.id,
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    
                    subject_template_name = 'pw_reset_subject.txt'
                    email_template_name = 'pw_reset_email.html'
                    
                    subject = loader.render_to_string(subject_template_name, c)
                    subject = ''.join(subject.splitlines())
                    
                    email = loader.render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                        result = self.form_valid(forget_form)                    
                        #messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue resetting password.")
                        return result
                    except Exception as e:
                         print(e)
                         return self.form_invalid(forget_form) 
                result = self.form_invalid(forget_form)
                messages.error(request, 'This username does not exist in the system.')
                return result
            messages.error(request, 'Invalid Input')
        return self.form_invalid(forget_form)


class PasswordResetConfirmView(FormView):
    template_name = "pw_reset_email_confirm.html"
    success_url = '/adminpanel/login/'
    form_class = SetPasswordForm

    def post(self, request, id=None, token=None, *arg, **kwargs):
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert id is not None and token is not None
        try:
            user = UserModel._default_manager.get(pk=id)            

        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            
            if form.is_valid():
                print(form)
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)


@login_required()
def export_users_csv(request):
    tab= request.GET.get('tab', None)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Meenfee-Professionals.csv"'
    if tab=="tab2":
        response['Content-Disposition'] = 'attachment; filename="Meenfee-Customers.csv"'        
    writer = csv.writer(response)
    writer.writerow(['Email address', 'First name', 'Last name', 'Phone number','User Type' ])    
    #users = User.objects.filter(is_superuser=False).select_related('userotherinfo').values_list('email', 'first_name', 'last_name','userotherinfo__phone','userotherinfo__usertype')    
    if tab=="tab2":
        users = User.objects.filter(Q(is_superuser=False) & Q(userotherinfo__usertype = 'requester')).values_list('email', 'first_name', 'last_name','userotherinfo__phone','userotherinfo__usertype')
    else:
        users = User.objects.filter(Q(is_superuser=False) & ( Q(userotherinfo__usertype = 'provider') | Q(userotherinfo__usertype = 'Provider'))).values_list('email', 'first_name', 'last_name','userotherinfo__phone','userotherinfo__usertype')
    for user in users: 
        type='Provider'
        if user[4] !='provider':
            type='Requester'        
        writer.writerow([user[0], user[1], user[2], user[3],type,])
       # writer.writerow(user)
    return response


# to rating reviews

def get_top_reviews(request):
        user_object = request.user
        service_qs = Service.objects.filter(user=user_object)
        print("<---------------Service QS retreived------------------->",service_qs)
        if len(service_qs)==0:
            return ""
        else:
            FinalQS = ServiceFeedback.objects.none()
            for service in service_qs:
                reviews = ServiceFeedback.objects.filter(service_id=service)
                FinalQS.union(reviews)
            
            print("<-------------Service Feedback QS------------------>",FinalQS)
            SortedQS = FinalQS.order_by('-rating','-feedback_date','-feedback_time')[:3]
            print("<--------------Sorted QS----------------------------->",SortedQS)
            data = ServiceFeedbackSerializer(SortedQS,many=True).data
            print("<----------------Data being returned------------------>",data)
            return data
        
@login_required()
def mark_provider_as_featured(request):
    
    data = request.POST
    user_id = data.get('userid')
    print("============>",user_id)
    UserObject = User.objects.get(id=user_id)
    FeaturedObject = FeaturedServiceProviders(provider=UserObject)
    FeaturedObject.save()
    
    return HttpResponse({"msg":"Hello"})


@login_required()
def unmark_provider_as_featured(request):

    data = request.POST
    user_id = data.get('userid')
    print("============>",user_id)
    UserObject = User.objects.get(id=user_id)
    FeaturedObject = FeaturedServiceProviders.objects.get(provider=UserObject)
    FeaturedObject.delete()
    
    return HttpResponse({"msg":"Hello"})   



@login_required()
def mark_id_verified(request):
    data = request.POST
    user_id = data.get('userid')
    print("<----------------->",user_id)
    UserObject = User.objects.get(id=user_id)
    uoi_object = UserOtherInfo.objects.get(user=UserObject)
    uoi_object.is_id_verified = True
    uoi_object.save()
    
    return HttpResponse({"msg":"ID Verified"})
    


@login_required()
def deactivate_account(request):
    data = request.POST
    user_id = data.get('userid')
    print("<---------User ID Deactivate Account----------->",user_id)
    UserObject = User.objects.get(id=user_id)
    UserObject.is_active = False
    UserObject.save()
    
    return HttpResponse({"msg":"Account Deactivated"})
    
    

@login_required
def manage_commission(request):
    if request.method == "GET":
        return render(request,'manage_commission.html')
    
    if request.method == "POST":
        raw_data = request.POST
        print("<---------------Raw Data Received------------>",raw_data)
        charges = Decimal(raw_data['name'].split(' ')[0].strip())

        AdminQS = AdminCommision.objects.filter(active=True)
        AdminQS.update(active=False)

        # for admin_object in AdminQS:
        #     admin_object.active = False
        #     admin
        AdminCommisionObject = AdminCommision(value=charges)
        AdminCommisionObject.save()
        return HttpResponseRedirect('/adminpanel/manage_commission/')



@login_required
def add_commission(request):
    if request.method == "GET":
        return render(request,'add_new_commission.html')
    
    if request.method == "POST":
        raw_data = request.POST
        print("<---------------Raw Data Received------------>",raw_data)
        charges = Decimal(raw_data['name'].split(' ')[0].strip())

        AdminQS = AdminCommision.objects.filter(active=True)
        AdminQS.update(active=False)
        AdminCommisionObject = AdminCommision(value=charges)
        AdminCommisionObject.save()
        return HttpResponseRedirect('/adminpanel/add-commission/')


@login_required
def list_commission(request):
    if request.method == "GET":
        AdminChargeQS = AdminCommision.objects.all().order_by('-commision_added')
        return render(request,'view_commission.html',{"data":AdminChargeQS})
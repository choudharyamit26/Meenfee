from django.db.models import Q,F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse


from meenfee.models import *
#from .forms import login_form,PasswordChangeForm,PasswordResetRequestForm,SetPasswordForm
from meenfee.models import UserOtherInfo
from meenfee.models import *
from django import template
from asn1crypto.x509 import AccessDescription
from asn1crypto.ocsp import Request
#from cookielib import request_host
register = template.Library()
#from django.contrib.auth.forms import PasswordChangeForm

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required

from django.views.generic import *
from django.template import loader
from django.core.mail import send_mail

from django.conf import settings

from myproject.settings import DEFAULT_FROM_EMAIL

from django.contrib.auth.tokens import default_token_generator

from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()
#from .permissions import IsAuthenticatedOrCreate
# from services.forms import ImageUploadForm,ContentForm,BannerImageUploadForm,CategoryImageUploadForm,ContentFormNew
from services.forms import *
from services.models import *

from django.db import IntegrityError



@login_required()
def service_main(request):
    #return HttpResponse("Hello, world. You're at the Admin Panel.")
    return render(request, 'service_main.html')

@login_required()
def add_service(request):
    isarabic=False    
    if isarabic == "true":
        categoryObj = Category.objects.all().values_list('id', 'category_in_arabic')
    else:
        categoryObj = Category.objects.all().values_list('id', 'category')    
    msg=[]
    if request.method == 'POST':
        form = request.POST          
        category = form.get('category')
        subcategory = form.get('subcategory')
        service_name = form.get('service_name')
        service_pricing = form.get('service_pricing')
        levelskill = form.get('levelskill')
        experience = form.get('experience')
        description = form.get('description')
        price_type = form.get('price_type')        
        quote_at_request = form.get('quote_at_request')
        
        if isarabic == "true":
            serviceObj = Service(service_name_in_arabic=service_name,category_id=category,subcategory_id=subcategory,service_pricing=service_pricing,levelskill=levelskill,experience=experience,quote_at_request=True,user_id=1,price_type=price_type,description_in_arabic=description)   
            serviceObj.save()
        else:
           serviceObj = Service(service_name=service_name,category_id=category,subcategory_id=subcategory,service_pricing=service_pricing,levelskill=levelskill,experience=experience,quote_at_request=True,user_id=1,description=description,price_type=price_type)
           serviceObj.save()   
        
        form1 = ImageUploadForm(request.POST, request.FILES) 
        
               
        if form1.is_valid(): 
            print("**********************************************")           
            si = ServiceImage()
            si.is_arabic = False
            si.service_id= serviceObj.id
            si.service_img_file = form1.cleaned_data['image']
            si.save() 
            return HttpResponseRedirect('/adminpanel/services/services-list')      
            #{{ hotel.hotel_Main_Img.url }}
        else:
            errMsg="Please upload atleast one valid images!"
            msg.append(errMsg)
            print("Error-------------->",form1)
            
        #
    return render(request, 'add_service.html',{'category': categoryObj,'messages':msg})


@login_required()
def edit_service(request,id):
    #qs = Service.objects.filter(Q(pk=id) & Q(id=id)).select_related().values('id','category_id','subcategory_id','service_name','service_pricing', 'price_type', 'levelskill', 'experience', 'quote_at_request', 'description') 
   
    qs = Service.objects.filter(id=id)#.select_related('serviceimage')
    print(qs,"++++++++++++++++++")
    qs1 = Category.objects.all().values('id','category')
    qs2 = SubCategory.objects.all().values('id','subcategory')
    
    if request.method == 'GET':
        qs = Service.objects.filter(id=id)#.select_related('serviceimage')       
        qs1 = Category.objects.all().values('id','category')
        qs2 = SubCategory.objects.all().values('id','subcategory')        
        dict = {}
        for qs4 in qs:
            dict['cat_id'] = qs4.category_id
            dict['scat_id']= qs4.subcategory_id
            dict['name']=qs4.service_name
            dict['name_arabic']=qs4.service_name_in_arabic
            dict['price']=qs4.service_pricing
            dict['price_type']=qs4.price_type
            dict['levelskill']=qs4.levelskill
            dict['experiance']=qs4.experience
            dict['qar']=qs4.quote_at_request
            dict['description'] =qs4.description
            dict['id']= qs4.id
            qs5 = ServiceImage.objects.get(id=5)#(service_id=qs4.id)
#             for qs6 in qs5:
#                 test=qs6.service_img_file
#                 dict['image']= qs6.service_img_file
#                 dict['image1']= qs6.service_img_file1
#                 dict['image2']= qs6.service_img_file2
#                 dict['s_img_id']= qs6.id
           # print(qs5.query,'++++++++++++++++++++++++++=')
            print(qs5,'++++++++++++++++++++++++++=')
            print(dict,"+++++++++++++++++++++++++++++++++++++++++++++>>>")
            qs3 = SubCategory.objects.filter(category_id=qs4.category_id).values('id','subcategory') 
            
           # request.POST or None, request.FILES or None,  instance=server'imagefield': qs5.image
            #initial['image'] = test  {'image': test }
            imgform = ImageUploadForm(request.POST, request.FILES) #instance=qs5 #form_class(data=request.POST, files=request.FILES,       
       
        #print(qs3,'++++++++++++++++++++++++++=')
    if request.method == 'POST':       
        form = request.POST
        
        print("here=================>",form)
        service_id = form.get('data_id')          
        category = form.get('category')
        subcategory = form.get('subcategory')
        service_name = form.get('service_name')
        service_pricing = form.get('service_pricing')
        levelskill = form.get('levelskill')
        experience = form.get('experience')
        description = form.get('description')
        price_type = form.get('price_type')        
        quote_at_request = form.get('quote_at_request')
        serviceObj = Service.objects.filter(id=service_id).update(service_name=service_name,category_id=category,subcategory_id=subcategory,service_pricing=service_pricing,levelskill=levelskill,experience=experience,quote_at_request=True,user_id=1,description=description,price_type=price_type)
        
        return HttpResponseRedirect('/adminpanel/services/services-list')
    
    return render(request, 'edit_service.html', {'servicedata': dict,'catData':qs1,'scatData':qs3,'allscatData':qs2,'imgform':imgform})

# 
# {% for vegetable_image in vegetable.images.all %}
#     {{ vegetable_image.image.url }}
#     {% endfor %}

@login_required()
def edit_image(request,id):
    qs5 = ServiceImage.objects.filter(id=5)
    
    if request.method == 'POST':        
        form1 = ImageUploadForm(request.POST, request.FILES)        
        if form1.is_valid(): 
            print("**********************************************")           
            si = ServiceImage.objects.filter(id=5)
            si.is_arabic = False
            si.service_id= serviceObj.id
            si.service_img_file = form1.cleaned_data['image']
            si.save()   
    
    
    print(qs5,"this is image text")
    #imgform = ImageUploadForm(request.POST, request.FILES, instance=qs5[0])
    return render(request, 'upload-image.html', {'imgform':qs5})
    




@login_required()
def services_list(request):
    isarabic="False"    
    if isarabic == "true":
        subcateData = SubCategory.objects.all().annotate(category2=F('subcategory_in_arabic'))
        categoryData = Category.objects.all().values_list('id', 'category_in_arabic')
        serviceData= Service.objects.all().annotate(serviceName2=F('service_name_in_arabic'))
    else:
        subcateData = SubCategory.objects.all().annotate(category2=F('subcategory'))
        categoryData = Category.objects.all().values_list('id', 'category')
        serviceData= Service.objects.all().annotate(serviceName2=F('service_name')).select_related()  
        #.select_related('service')        
    serviceImageData= ServiceImage.objects.all()
    data = {}
    data['object_list'] = serviceData
    data['category'] = categoryData 
    data['subcategory'] = subcateData   
    data['service_img'] = serviceImageData
    
    return render(request, 'services_list.html', data)

@login_required()
def delete_service(request,id):       
    subcatdata = Service.objects.get(id=id)
    subcatdata.delete()
    return HttpResponseRedirect('/adminpanel/services/services-list')
    
@login_required()
def get_table_values(request):
    isarabic=False 
    if request.method == "GET":
        id= request.GET.get('id').strip()
        try:               
            if isarabic == "true":
                queryset = SubCategory.objects.filter(category_id=id).values().annotate(subcate=F('subcategory_in_arabic'))
            else:
                queryset = SubCategory.objects.filter(category_id=id).values().annotate(subcate=F('subcategory'))
            
            len_queryset= len(queryset)
            print(len_queryset)
            response_dict = {
                'qs': list(queryset),
                'qs_len':len_queryset,
                'msg': 'success',
            }
        except SubCategory.DoesNotExist:
            pass
    else:
        response_dict = {
            'code': 1,
            'id': 2,
        }
    print(response_dict)
    return JsonResponse(response_dict)

@login_required()
def add_category(request):
     isarabic=False
     msg=[]
     if request.method == 'POST':
        form = request.POST           
        name = form.get('name')
        name_arabic = form.get('name_arabic')
        code = 'admin'
        description = form.get('description')
        cate_image=''
        form2 = CategoryImageUploadForm(request.POST, request.FILES)        
        if form2.is_valid():  
            print("Pic Validation=============>")
            cate_image= form2.cleaned_data['bannerimage']
       
        try:
            if isarabic == "true":
                categoryObj = Category(category_in_arabic=name,code_in_arabic=code,description_in_arabic=description)   
                categoryObj.save()
            else:
                categoryObj = Category(category=name,code=code,description=description,bannerimage=cate_image,category_in_arabic=name_arabic)
                categoryObj.save()    
            return HttpResponseRedirect('/adminpanel/services/category-list?status=successful')   
        except IntegrityError as error:
            print("IntegrityError---------------------------------->>>>",error)
            errmsg= "Already Same Name category exist!"
            msg.append(errmsg)
            
            #return render_to_response("template.html", {"message": e.message})
            #return HttpResponse("ERROR: Kumquat already exists!")
         
     return render(request, 'add_category.html',{"messages":msg})
    
@login_required()
def add_subcategory(request):
    isarabic=False    
    if isarabic == "true":
        categoryObj = Category.objects.all().values_list('id', 'category_in_arabic')
    else:
        categoryObj = Category.objects.all().values_list('id', 'category')    
    
    if request.method == 'POST':
        form = request.POST         
        category = form.get('category')
        subcategory = form.get('subcategory')
        subcategory_arabic = form.get('subcategory_arabic')
        description = form.get('description')
        if int(category) >0:
            if isarabic == "true":
                subcategoryObj = SubCategory(category_id=category,subcategory_in_arabic=subcategory,description_in_arabic=description)   
                subcategoryObj.save()
            else:
                subcategoryObj = SubCategory(category_id=category,subcategory=subcategory,description=description,subcategory_in_arabic=subcategory_arabic)
                subcategoryObj.save()
            return HttpResponseRedirect('/adminpanel/services/subcate-list')    
    return render(request, 'add_subcategory.html',{'category': categoryObj,})

# @login_required()
# def add_content(request):       
#     isarabic=False 
#     flag= False 
#     form=ContentFormNew()    #or None, instance=curr_data
#     if request.method == 'POST':
#         data=request.POST
#         content1 = request.POST.get('content')
#         content2 = request.POST.get('content_in_arabic')
#         title = request.POST.get('')
#         isarabicval=data['isarabic']
#         form1 = ContentFormNew(request.POST or None)   
#         if content2:
#             flag=True        
#         if content1:
#             flag=True             
#         if form1.is_valid() and flag==True:
#             form1.save()           
#         else:
#             print(form1.errors,"------------->")
#         return HttpResponseRedirect('/adminpanel/services/content-list')
            
#     if isarabic == "true":
#         return render(request, 'add_content_ar.html',{'form':form})
#     else:
#         return render(request, 'add_content.html',{'form':form})
    

@login_required()
def add_content(request):       
    isarabic=False 
    flag= False 
    form=ContentFormNew()    #or None, instance=curr_data
    if request.method == 'POST':
        data=request.POST
        title = request.POST.get('title')
        title_arabic = request.POST.get('title_in_arabic')
        content = request.POST.get('content')
        content_in_arabic = request.POST.get('content_in_arabic')

        print("<-----------Title------------->",title)
        print("<------------Title Arabic--------->",title_arabic)
        print("<---------Main Content----------?>",content)
        print("<----------Main Content Arabic-------->",content_in_arabic)
        # title = request.POST.get('')
        # isarabicval=data['isarabic']
        form1 = ContentFormNew(request.POST or None)

        if None not in [title,title_arabic,content,content_in_arabic] or "" not in [title,title_arabic,content,content_in_arabic]:
            if form1.is_valid():
                form1.save()
                return HttpResponseRedirect('/adminpanel/services/content-list')
            else:
                print(form1.errors,"------------->")
                return HttpResponseRedirect('/adminpanel/services/content-list')
        else:
            # print(form1.errors,"------------->")
            return HttpResponseRedirect('/adminpanel/services/content-list')             

        # if content2:
        #     flag=True        
        # if content1:
        #     flag=True             
        # if form1.is_valid() and flag==True:
        #     form1.save()           
        # else:
        #     print(form1.errors,"------------->")
        # return HttpResponseRedirect('/adminpanel/services/content-list')
            
    if isarabic == "true":
        return render(request, 'add_content_ar.html',{'form':form})
    else:
        return render(request, 'add_content.html',{'form':form})
    



@login_required()
def delete_category(request,id):    
    catdata = Category.objects.get(id=id)
    catdata.delete()
    return HttpResponseRedirect('/adminpanel/services/category-list')

@login_required()
def delete_subcategory(request,id):    
    subcatdata = SubCategory.objects.get(id=id)
    subcatdata.delete()
    return HttpResponseRedirect('/adminpanel/services/subcate-list')

@login_required()
def catgory_list(request):
    status= request.GET.get('status', None)
    isarabic="False"    
    if isarabic == "true":
        catelist = Category.objects.all().annotate(category2=F('category_in_arabic'),description2=F('description_in_arabic'),)
    else:
        catelist = Category.objects.all().annotate(category2=F('category'),description2=F('description')) 
    data = {}
    catList = []
    for cdata in catelist:
         catdict = {}
         catdict['id']=cdata.id
         catdict['category2']=cdata.category2
         catdict['category_arabic'] = cdata.category_in_arabic
         catdict['description2']=cdata.description2
         catdict['description_arabic'] = cdata.description_in_arabic
         catdict['bannerimage']=cdata.bannerimage
         category_id = cdata.id
         qs1 = Service.objects.filter(category_id=category_id).count() 
         catdict['services_count']=qs1
         catList.append(catdict)
    
    data['object_list'] = catList
    if status=='successful':
        data['messages'] = ["Category Successfully created"]
    if status=='successfulupdate':
        data['messages'] = ["Category Successfully updated"]
    
    return render(request, 'category_list.html', data)

@login_required()
def subcategory_list(request):
    status= request.GET.get('status', None)
    isarabic="False"    
    if isarabic == "true":
        subcatelist = SubCategory.objects.all().annotate(category2=F('subcategory_in_arabic'))
        categoryData = Category.objects.all().values_list('id', 'category_in_arabic')
    else:
        subcatelist = SubCategory.objects.all().annotate(category2=F('subcategory'))
        categoryData = Category.objects.all().values_list('id', 'category','category_in_arabic')    
    
    data = {}
    data['object_list'] = subcatelist
    data['category'] = categoryData 
    if status=='successful':
        data['messages'] = ["SubCategory Successfully created"]
    if status=='successfulupdate':
        data['messages'] = ["SubCategory Successfully updated"] 
    return render(request, 'subcategory_list.html', data)

@login_required()
def content_list(request):
    contentlist = ContentMaster.objects.all()   
    data = {}
    data['object_list'] =contentlist
    return render(request, 'content_list.html', data)
def delete_content(request,id):
    contentdata = ContentMaster.objects.get(id=id)
    contentdata.delete()
    return HttpResponseRedirect('/adminpanel/services/content-list')


@login_required()
def add_rating(request):
    print("here")

@login_required()
def userrating_list(request):
    usrlist = User.objects.all().select_related('userotherinfo')


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
    data['object_list'] = usrlist
    return render(request, 'userrating.html', data)

@login_required()
def add_banner(request):
    is_arabic=False
    msg=[]
    if request.method == 'POST':
       form = request.POST          
       banner_name = form.get('banner_name')
       description = form.get('description')
       banner_name_arabic = form.get('banner_name_arabic')
       description_arabic = form.get('description_arabic')
#        if is_arabic=="true":
#            bannerObj = BannerImage(banner_name_in_arabic=banner_name,description_in_arabic=description)
#            bannerObj.save()
#        else:
#            bannerObj = BannerImage(banner_name=banner_name,description=description)
#            bannerObj.save()        
       form2 = BannerImageUploadForm(request.POST, request.FILES)
       if form2.is_valid():            
           bi = BannerImage()
           bi.banner_img_file = form2.cleaned_data['banner_image']
           bi.banner_name = banner_name
           bi.description =description
           bi.banner_name_in_arabic = banner_name_arabic
           bi.description_in_arabic = description_arabic
           bi.save()
           return HttpResponseRedirect('/adminpanel/services/banner-list') 
       else:
           errmsg="Please upload valid Image banner." 
           msg.append(errmsg)
           print(msg)
       
    return render(request, 'add-banner.html' ,{"messages":msg})


@login_required()
def banner_list(request):
    status= request.GET.get('status', None)    
    bannerImageData= BannerImage.objects.all()
    data = {}     
    data['bannerlist'] = bannerImageData
    if status=='successful':
        data['messages'] = ["Banner Successfully created"]
    if status=='successfulupdate':
        data['messages'] = ["Banner Successfully updated"] 
    return render(request, 'list-banner.html',data)


@login_required()
def delete_banner(request,id):
    bannerdata = BannerImage.objects.get(id=id)
    bannerdata.delete()
    return HttpResponseRedirect('/adminpanel/services/banner-list')


def payment_process(request):
    print("*************************>")
    return render(request, 'payment.html')
    #return HttpResponseRedirect('/adminpanel/services/payment/')
    
    
    
          
    
def add_rating(request):
    print("*************************>")
    return render(request, 'mod_rating.html')


def delete_rating(request,id):
    print("*************************>")
    return HttpResponseRedirect('/adminpanel/services/list-rating')


def list_rating(request):
    provdlist = User.objects.filter(Q(is_superuser=False)  & ( Q(userotherinfo__usertype = 'provider') | Q(userotherinfo__usertype = 'Provider'))) 
    print(provdlist.query)
    #provdlist = User.objects.filter(Q(is_superuser=False) & ( Q(userotherinfo__usertype = 'provider') | Q(userotherinfo__usertype = 'Provider')))
    qs = User.objects.filter(Q(is_superuser=False) & ( Q(userotherinfo__usertype = 'provider') | Q(userotherinfo__usertype = 'Provider')))
    print(qs,"=======================>testing types")
    data = []
    data_dict = {}
    for qs1 in qs:
        print("herer")
        provider_id=qs1.id
        p_name= qs1.first_name +" "+ qs1.last_name
        
        qs2=Service.objects.filter(Q(pk=provider_id))#.select_related('providersrating')
        
        qs3=NewBookings.objects.filter(Q(pk=provider_id) & ~Q(providers_review_id=0))
        
        
        
#         for qs2 in qs:
#             charge_type = qs2['charge_type']
#             charge_to_id = qs2['charge_to_id']
#             qs4 = ChargeTypeMaster.objects.filter(pk=charge_type).values_list('code', flat=True)
#             qs5 = ChargeToMaster.objects.filter(pk=charge_to_id).values_list('code', flat=True)
# 
#             for qs3 in qs1:
#                 data_dict = {}
#                 data_dict['charge_type'] = qs4[0]
#                 data_dict['charge_to_id'] = qs5[0]
    
    for prod in provdlist:
        
        print(prod.userotherinfo.usertype)
    print(provdlist,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")  
    data = {}     
    data['provider_list'] = provdlist
    return render(request, 'user-rating-list.html',data)




def list_pservices(request,id):
    print("*************************>")
    frommod= request.GET.get('from', None)
    print(frommod,"======================>")
    provider_id = id
    qs1=Service.objects.filter(Q(pk=provider_id))
    
    qs2=User.objects.get(id=provider_id)
    qs3=Category.objects.all()
    qs4=SubCategory.objects.all()
    
    
    isarabic="False"    
    if isarabic == "true":       
        serviceData= Service.objects.filter(user_id=provider_id).annotate(serviceName2=F('service_name_in_arabic'))
    else:       
        serviceData= Service.objects.filter(user_id=provider_id).annotate(serviceName2=F('service_name')).select_related() 
    
    print(serviceData,"======================>ServiceDataHeare")       
    serviceImageData= ServiceImage.objects.all()
    data = {}
    serviceData = list(serviceData)
#     data_dict = {}
#     data_dict['count_of_rating'] = '3'
#     data_dict['avg_rating'] = '4'
#     data_dict['serviceName2'] = 'Test'
#     data_dict['id'] = 1
#     
#     serviceData.append(data_dict)
#     
    data['object_list'] = serviceData    
    data['service_img'] = serviceImageData
    data['name'] = qs2.first_name +" " + qs2.last_name
    data['category'] =list(qs3)
    data['subcategory'] =list(qs4)
    
    
    """ {
           "id": 1,
           "booking_id": "MNF20190708192627901121",
           "created": "2019-07-08T19:26:28.260052",
           "requestor": "Parul Gupta",
           "provider": "Chris Hemsworth",
           "service_name": "Wall Painter",
           "appointment_city": "Amman",
           "point_of_service": "RequestorPlace",
           "accepted": false,
           "service_date": "2019-07-08",
           "service_time": "19:24:00",
           "task_status": "In Progress",
           "accepted_by_requester": true,
           "accepted_by_provider": true,
           "rescheduled_service_date": "2019-07-08",
           "rescheduled_service_time": "18:29:03.176379",
           "booking_cancelled": false,
           "booking_completed": false,
           "requestor_id": 2,
           "provider_id": 1,
           "service_ID": 1
        }
    """
    
    print("hello-------------------------------------------->dsaddas")
    if frommod=="admin":
        return render(request, 'list-pservices-admin.html',data)
    else:
        return render(request, 'list-pservices.html',data)
        
    #return render(request, 'list-pservices.html',data)
    #return render(('/adminpanel/services/list-pservices',data)
    #return HttpResponse(json.dumps(response), content_type='application/json')
    #window.location('your_url')




def list_pservices_reviews(request,id):    
    qs1=ProvidersRating.objects.filter(Q(service_id=1))    
    print(qs1.query)    
    data = {}
    #data = list(qs1)    
    temp=[]
    data_dict = {}
    data_dict['service_id'] = 3
    data_dict['content1'] = 'This is test reviews for testing time.'
    data_dict['compliment_review'] = 4
    data_dict['id'] = 1    
    temp.append(data_dict)  
    data['reviews'] = temp    
    return render(request, 'list-pservices-reviews.html',data)

def mod_review(request,id):
    review_id= id
    print(id ,"*************************>")    
    if request.method == 'POST':
        form = request.POST
        r_id = form.get('review_id')
        review = form.get('content')
        ProvidersRating.objects.filter(id=r_id).update(content1=review)    
    
    return HttpResponseRedirect('/adminpanel/services/list-rating')

def payment_list(request):
    SettledPaymentsQS = SettledPayments.objects.filter(active=True)
    return render(request,'payment-list.html',{"data":SettledPaymentsQS})

def pay_refund_list(request):
    bannerImageData= BannerImage.objects.all()
    data = {}     
    data['bannerlist'] = bannerImageData
    return render(request, 'payment-refund.html',data)


def pay_complete_list(request):
    bannerImageData= BannerImage.objects.all()
    data = {}     
    data['bannerlist'] = bannerImageData
    return render(request, 'payment-complete.html',data)


def edit_category(request,id):    
    catelist = Category.objects.get(id=id)   
    data={}
    data['object_list']= catelist
    data['id']=catelist.id
    data['name']=catelist.category
    data['name_arabic'] = catelist.category_in_arabic

    data['description']=catelist.description
    msg=[]
    if request.method == 'POST':
        form=request.POST
        cate_id = form.get('cate_id')          
        category = form.get('name')
        description = form.get('description')
        if description !='':            
            cateObj = Category.objects.filter(id=id).update(description=description)        
            form2 = CategoryImageUploadForm(request.POST  or None, request.FILES or None)        
            if form2.is_valid(): 
                bannerimage= form2.cleaned_data['bannerimage']
                bUrl=request.FILES['bannerimage']
                caOBJ= Category.objects.get(id=id)
                caOBJ.bannerimage= bannerimage
                caOBJ.save()           
            else:
                errmsg= "Please upload valid image!"
                msg.append(errmsg)                               
                return render(request, 'edit_category.html',{'data': data,'messages':msg})  
            return HttpResponseRedirect('/adminpanel/services/category-list?status=successfulupdate')
        
        errmsg= "Please enter valid inputs!"
        msg.append(errmsg)          
    return render(request, 'edit_category.html',{'data': data,'messages':msg})


def related_subcategory(request,id): 
    print("this is related sub category")
    subCatelist = SubCategory.objects.filter(category_id=id) 
    print(subCatelist,"=====>SCATLIST")  
    data={}
    data['object_list']= subCatelist   
    msg=[]
    return render(request, 'detail_subcategory.html',data)

def edit_subcategory(request,id):
    print("==========>Testing Teams")
    isarabic=False    
    if isarabic == "true":
        categoryObj = Category.objects.all().values_list('id', 'category_in_arabic')
    else:
        categoryObj = Category.objects.all().values_list('id', 'category') 
    
    subcatelist = SubCategory.objects.get(id=id)  
    
    data={}     
    data['object_list']= subcatelist
    data['id']=subcatelist.id
    data['name']=subcatelist.subcategory
    data['name_arabic'] = subcatelist.subcategory_in_arabic
    data['description']=subcatelist.description
    data['category_id']=subcatelist.category_id
    cateObj= Category.objects.filter(id=subcatelist.category_id ).values_list('category', flat=True)     
    data['category_name']=cateObj[0]
    msg=[] 
    if request.method == 'POST':
        form=request.POST
        subcate_id = form.get('subcate_id') 
        description = form.get('description')
        if description !='':
            cateObj = SubCategory.objects.filter(id=subcate_id).update(description=description)
            return HttpResponseRedirect('/adminpanel/services/subcate-list?status=successfulupdate')
        errmsg= "Please enter valid input!"
        msg.append(errmsg) 
    return render(request, 'edit_subcategory.html',{'data': data,'messages':msg,'category': categoryObj,})
    


def edit_banner(request,id):
    bannerData = BannerImage.objects.get(id=id)   
    data={}
    data['object_list']= bannerData
    data['id']=bannerData.id
    data['name']=bannerData.banner_name
    data['description']=bannerData.description
    data['name_arabic'] = bannerData.banner_name_in_arabic
    data['description_arabic'] = bannerData.description_in_arabic
    msg=[]
    if request.method == 'POST':
        form=request.POST
        banner_id = form.get('banner_id')          
        banner_name = form.get('banner_name')
        description = form.get('description')
        if description !='':            
            bannerObj = BannerImage.objects.filter(id=banner_id).update(banner_name=banner_name,description=description)
            
            form2 = BannerImageUploadForm(request.POST  or None, request.FILES or None)        
            if form2.is_valid(): 
                banner_image_file= form2.cleaned_data['banner_image']
               # banner_image_file_url=request.FILES['banner_image']
                bannerOBJ= BannerImage.objects.get(id=banner_id)
                try:
                    print("<---------IN try block----------->")
                    bannerOBJ.banner_img_file= banner_image_file
                except Exception as e:
                    print("<---------Exception--------->",e)
                    pass
                bannerOBJ.save()           
            else:
                #form.errors
                errmsg= "Please upload valid image!"
                msg.append(errmsg)                               
                return render(request, 'edit_banner.html',{'data': data,'messages':msg})
            return HttpResponseRedirect('/adminpanel/services/banner-list?status=successfulupdate')
        
        errmsg= "Please enter valid inputs!"
        msg.append(errmsg)          
   
    return render(request, 'edit_banner.html',{'data': data,'messages':msg,})



def type_questions(request):    
    if request.method == 'POST':
        form=request.POST
        pageid = form.get('question') 
        if pageid=='common':               
            print("Here========>")
            return HttpResponseRedirect('/adminpanel/services/add-questions/1')
        if pageid=='custom':               
            print("Here========>")
            return HttpResponseRedirect('/adminpanel/services/add-questions/2')
    data={}
    msg=[]
    return render(request, 'type_questions.html',{'data': data,'messages':msg})    
    


def add_questions(request,id): 
    """  add category Id in question + Active deactive + Multiple answers -- Answer table consider as a row """
    data={}
    msg=[]
    isarabic="false"  
    if isarabic == "true":
        categoryObj = Category.objects.all().values_list('id', 'category_in_arabic')
    else:
        categoryObj = Category.objects.all().values_list('id', 'category')  
    pageid=id   
    if request.method == 'POST':
        form = request.POST 
        category = form.get('category')
        subcategory = form.get('subcategory')  
        question_name = form.get('question_name')
        question_for_provider = form.get('question_for_provider')
        question_for_requester = form.get('question_for_requester')
        answer = form.get('answer')        
        answers = form.getlist('answer[]')
        answers_arabic = form.getlist('answer_arabic[]')
        print("<------------Answers English---------->",answers)
        print("<----------Answers Arabic------------>",answers_arabic)
        service_id = form.get('service')
        
        if  subcategory !="":
            questObj = QuestionFilledByAdmin(Question_name=question_name,SubCategory_id=subcategory,
                                             question_for_provider=question_for_provider,question_for_requestor=question_for_requester,status1=True,related_service_ids=service_id
                                             )
            questObj.save()
            question_id=  questObj.id        
            if len(answers):
                for i in range(len(answers)):
                    OptionsFilledbyAdmin.objects.create(question_id=question_id, Option1=answers[i],Option1_in_arabic=answers_arabic[i])
            return HttpResponseRedirect('/adminpanel/services/list-questions?status=successful')
        else:
            errMsg="Questions can not add without SubCategory!"
            msg= msg.append(errMsg)
    return render(request, 'add_questions.html',{'category': categoryObj,'messages':msg,'pageid':pageid})
  

@login_required()
def get_services_values(request):
    isarabic=False 
    if request.method == "GET":
        id= request.GET.get('id').strip()
        try: 
            queryset = Service.objects.filter(subcategory_id=id).values()
            len_queryset= len(queryset)
            print(len_queryset)
            response_dict = {
                'qs': list(queryset),
                'qs_len':len_queryset,
                'msg': 'success',
            }
        except SubCategory.DoesNotExist:
            pass
    else:
        response_dict = {
            'code': 1,
            'id': 2,
        }
    print(response_dict,"======>Services")
    return JsonResponse(response_dict)    
    
def list_questions(request):
    status= request.GET.get('status', None)
    qData= QuestionFilledByAdmin.objects.all()
    data = {}     
    data['questions'] = qData
    if status=='successful':
        data['messages'] = ["Question Successfully created"]
    if status=='del':
        data['messages'] = ["Question Successfully deleted"]
    return render(request, 'questions-list.html',data)

def delete_question(request,id):
    questionData = QuestionFilledByAdmin.objects.get(id=id)
    questionData.delete()
    return HttpResponseRedirect('/adminpanel/services/list-questions?status=del')

def list_answers(request,id):
    status= request.GET.get('status', None)
    answerData= OptionsFilledbyAdmin.objects.filter(question_id=id)
    data = {}     
    data['answers'] = answerData
    if status=='del':
        data['messages'] = ["Answer Successfully deleted"]
    return render(request, 'answers-list.html',data)

def delete_answer(request,id):
    next = request.GET.get('next', '/default/url/')  
    #1 print(request.META.get('HTTP_REFERER'),"<====================================>")
    #2 from django.utils.http import is_safe_url
    #         next = request.GET.get('next', '/default/url/')
    #         # check that next is safe
    #         if not is_safe_url(next):
    #             next = '/default/url/'
    #         return redirect(next)
    #        <a href="{% url 'main:buy_punchcard' member.id %}?next={{ request.path }}">Buy punchcard</p>
    # 3 Method doing work
    # 4    if request.method == 'GET':
    #         request.session['report_url'] = request.META.get('HTTP_REFERER')
    #         # ...
    #     if request.method == 'POST':
    #         form = ReportForm(request.POST or None)
    #         if form.is_valid():
    #             new_form = form.save(commit=False)
    #             new_form.reporting_url = request.session.get('report_url')
    answerData = OptionsFilledbyAdmin.objects.get(id=id)
    answerData.delete()
    return HttpResponseRedirect('/adminpanel/services/list-answers/'+next+'/?status=del')


def service_based_questions(request,id):
    #id=12
    serviceObj = Service.objects.get(id=id)
    category_id= serviceObj.category_id
    subcategory_id= serviceObj.subcategory_id
    common_question_qs = QuestionFilledByAdmin.objects.filter(SubCategory = subcategory_id,related_service_ids = 0)
    service_question_qs = QuestionFilledByAdmin.objects.filter(related_service_ids=str(id))
    final_question_qs = common_question_qs.union(service_question_qs)    
    answerData= OptionsFilledbyAdmin.objects.filter(question_id=id)
    
    
    
#     
#        'https://srstaging.stspayone.com/SmartRoutePaymentWeb/SRMsgHandler',
#        // 'https://srstaging.stspayone.com/SmartRoutePaymentWeb/SRPayMsgHandler',
#        {
#          //  Merchant Authentication Token: 'N2UwNmQ3NDlmZmY4Yzg1NTA0NzUwMTdm',
#          // MerchantID: 2000000045,
#          MessageID: 1, // 1,6
#          TransactionID: '12345678901234567890',
#          MerchantID: 2000000045,
#          Amount: 100,
#          CurrencyISOCode: 400,
#          SecureHash:
#            '7d30fd6ac61b63ff03402d7fb637afa731c0641b171ea43f12df13ac346cb874',
#          /* optional parameter */
#          PaymentMethod: 1,
#          CardNumber: '4111111111111111',
#          ExpiryDateYear: '22',
#          ExpiryDateMonth: 10,
#          SecurityCode: '854',
#          CardHolderName: 'name',
#          // ClientIPaddress: '192.168.0.243',
#          // Channel: '0',
#          ItemID: 362,
#          // Language: 'En',
#          // ThemeID: 'Theme1',
#          // PaymentDescription: 'SamplePaymentDescription',
#          // ResponseBackURL: 'https://google.com',
#          // Quantity: '1',
#          // GenerateToken: 'No',
#          // Version: '1.0'
#     
#     
    
     
    
    data={}
    data['questions'] = final_question_qs   
    return render(request, 'question-details.html',data)

    


def deactivate_payments(request,id):
    SettledPaymentsObject = SettledPayments.objects.get(id=id)
    SettledPaymentsObject.active = False
    SettledPaymentsObject.save()
    return HttpResponseRedirect('/adminpanel/services/payment-list')

from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
    )
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
    )
from meenfee.fcm_notification import send_to_one,send_to_many
from meenfee.models import *
from .serializers import *
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_204_NO_CONTENT,HTTP_201_CREATED
from django_filters import rest_framework as filters
import django_filters
from django.db.models import Avg, Max, Min
from django.db.models import Count
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from datetime import datetime
from django.core import serializers
import json
from django import db
from django.core.mail import EmailMessage
import random
import string
import pybase64
from meenfee.api.encryption import encrypt, decrypt
from django.views.generic import TemplateView
from rest_framework_jwt.settings import api_settings
from _collections import OrderedDict
from _ast import operator
from email.policy import HTTP
from audioop import reverse
from time import strftime
from urllib.request import Request
from distutils.command.check import check
from select import select
from _datetime import date
from calendar import week

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags




# <-----------------------------ADDED BY JOEL------------------------------->
from drf_rw_serializers import generics
import base64
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser,FormParser
from PIL import Image
from fcm_django.models import FCMDevice
from django.db.models import Q,F
from collections import Counter
from operator import itemgetter
import math
import time
from operator import itemgetter
import calendar
from services.models import *
import random
from rest_framework.pagination import PageNumberPagination
from decimal import *
import requests
# from datetime import *
# <-----------------------------ADDED BY JOEL------------------------------->

from meenfee.models import NewBookings as NewBookingModel

PAGINATION = True
PROVIDER_STRING = "provider"
REQUESTOR_STRING = "requester"

INTERNAL_TIME_FORMAT = None
EXTERNAL_TIME_FORMAT = "%I:%M %p"


INTERNAL_DATE_FORMAT = None
EXTERNAL_DATE_FORMAT = "%d/%m/%Y"

NEW_TIME_FORMAT = True

REMOVE_BOOKED_SLOTS = True

MIN_SERVICES = 1

PREVIOUS_DAYS = 60

ENABLE_UNIQUE_USER = True

ALL_DATES_OF_MONTH = True

LOCK_BOOKED_SLOT = True

AVAILABILITY_MAX_DAYS = 30

NEW_RESCHEDULE_METHOD = False

RANDOM_TRANSACTION_FAIL = False

CANCELLATION_FEE_PERCENTAGE = 15

BOOKING_TIME_LIMIT_HOURS = 3

BOOKING_TIME_LIMIT_DEBUG = False

BOOKING_TIME_LIMIT_MIN = 1




class MyPaginationMixin(PageNumberPagination):

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination 
        is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(
            queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given 
        output data.
        """
        assert self.paginator is not None
        sample = self.paginator.get_paginated_response(data)
        return self.paginator.get_paginated_response(data)




class UserdetailListAPIView(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer = UserListSerializer(users,many=True).data
        return Response(serializer,status = HTTP_200_OK)





class CreateServiceAPIView(APIView):
    # authentication_classes = [JSONWebTokenAuthentication]    
    # permission_classes = (IsAuthenticated,IsProvider)
    def post(self, request, format=None):
        
        SNAP_TO_TIME = False
        
        
        print("<-------------Service Create check------------>22AUG",request.data)
        user = request.user
        data  = request.data
        print("<-----------Raw Data------------------>",data)
        speciality = False

        try:
            speciality = data['speciality']
            if "description" in data:
                experience_description = data["description"]
            elif "experience_description" in data:
                experience_description = data["experience_description"]
                
        except:
            pass
        
        schedule = data['arrayofworkingdays']
        
        for schedule_object in schedule:
            checked = schedule_object['checked']
            print("<--------------Checked------------------>",checked)
            slot_array  = schedule_object['slots']
            print("<--------------Slot Array-------------->",slot_array)
            
            if checked:
                if len(slot_array) == 0:
                    print("<----------INvalid Time Slot--------------------->")
                    return Response({"msg":"Invalid Time Slots"},status=HTTP_400_BAD_REQUEST)


        
        
        
        serializer = ServiceCreateSerializer(data=data)      
        if serializer.is_valid():
            serializer.validated_data['experience_description'] = experience_description
            userobj = UserOtherInfo.objects.get(user=request.user)
            print("<-----------UserObject----------------->",userobj)
            try:
                SpecialServiceQS = Service.objects.filter(user=request.user,speciality = True)
                print("<--------------Special Service QS------------------------->",SpecialServiceQS)
                if len(SpecialServiceQS) == 0:
                    print("<----------------------Length of QS is zero----------------->")
                    serializer.validated_data['user'] = request.user
                    serializer.validated_data['speciality'] = True

                    serviceObject = serializer.save()
                else:
                    if speciality == True:
                        print("<------------------Length of QS is not zero-------------->")
                        SpecialServiceObject = SpecialServiceQS[0]
                        print("<--------------------SpecialServiceObject--------------->",SpecialServiceObject)
                        SpecialServiceObject.speciality = False
                        SpecialServiceObject.save()
                        serializer.validated_data['user'] =  request.user
                        serializer.validated_data['speciality'] = True

                        serviceObject = serializer.save()
                    else:
                        serializer.validated_data['user'] = request.user
                        serializer.validated_data['speciality'] = False

                        serviceObject = serializer.save()
            except:
                print("<------------Some Error Occured.Inside Exception Clause------------>")
                pass   
            
            
            
            
            schedule = data['arrayofworkingdays']

            service_images = data['service_images']
            ServiceImageObject = ServiceImage(service=serviceObject) 

        
            for i in range(0,len(service_images)):
                if i==0:
                    ServiceImageObject.service_img_file_1_s3 = service_images[i]
                    ServiceImageObject.service_img_file = service_images[i]

                elif i==1:
                    ServiceImageObject.service_img_file_2_s3 = service_images[i]
                    ServiceImageObject.service_img_file1 = service_images[i]
                elif i == 2:
                    ServiceImageObject.service_img_file_3_s3 = service_images[i]
                    ServiceImageObject.service_img_file2 = service_images[i]
            ServiceImageObject.save()
            

            for schedule_object in schedule:
                print("<---------------Inside Schedule Create Object--------------->")
                
                day = schedule_object['day']
                checked = schedule_object['checked']
                slot_array  = schedule_object['slots']
                print("<----------------Checked--------------->",checked)
                print("<----------------Slot Array------------>",slot_array)
                print("<----------------Len Slot Array------------->",len(slot_array))
                if checked and len(slot_array)>0:
                    print("<-----------------Valid Slot--------------------->")

                    for time_slot in slot_array:
                        if not SNAP_TO_TIME:
                            print("<--------------Open Time----------------->",time_slot['openTime'])
                            open_time = time_slot['openTime'].strip()
                            print("<---------------Cleaned------------->",open_time)
                            
                            if not NEW_TIME_FORMAT :
                                formatted_open_time = time.strptime(open_time,"%H:%M:%S")
                            else:
                                formatted_open_time = time.strptime(open_time,EXTERNAL_TIME_FORMAT)
                                
                            stand_open_time = time.strftime("%H:%M:%S",formatted_open_time)
                            print("<--------------Formatted Open Time---------------->",stand_open_time)
                            close_time = time_slot['closeTime'].strip()
                            
                            if not NEW_TIME_FORMAT:
                                formatted_close_time = time.strptime(close_time,"%H:%M:%S")
                            else:
                                formatted_close_time = time.strptime(close_time,EXTERNAL_TIME_FORMAT)
                                
                                                                
                            stand_close_time = time.strftime("%H:%M:%S",formatted_close_time)
                        else:
                            print("<--------------Inside Snap To Time--------------------->")
                            open_time = time_slot['openTime'].strip()
                            parsed_open = time.strptime(open_time,"%H:%M:%S")
                            minute_raw = time.strftime("%M",parsed_open)
                            minute = int(minute_raw)
                            hour = time.strftime("%H",parsed_open)
                            hour_int = int(hour)
                            
                            
                            if minute >= 8 and minute <= 22:
                                
                                minute = 15
                            elif minute >= 23 and minute <= 37:
                                minute = 30
                            elif minute >= 38 and minute <= 52:
                                minute = 45
                            elif minute >= 53 and minute <= 59:
                                hour_int+=1
                                minute = 0
                            elif minute >=0 and minute <= 7:
                                minute = 0
                            
                            stand_open_time = str(hour_int) + ":" + str(minute) + ":" + "00"
                            
                            close_time = time_slot['closeTime'].strip()
                            parsed_close = time.strptime(close_time,"%H:%M:%S")
                            minute_raw = time.strftime("%M",parsed_close)
                            minute = int(minute_raw)
                            hour = time.strftime("%H",parsed_close)
                            close_hour_int = int(hour)
                            
                            
                            if minute >= 8 and minute <= 22:
                                minute = 15
                            elif minute >= 23 and minute <= 37:
                                minute = 30
                            elif minute >= 38 and minute <= 52:
                                minute = 45
                            elif minute >= 53 and minute <= 59:
                                close_hour_int+=1
                                minute =0
                            elif minute >=0 and minute <= 7:
                                minute = 0
                            
                            stand_close_time = str(close_hour_int) + ":" + str(minute) + ":" + "00"                            
                            
                            
                            
                            

                        ServiceScheduleObject = ServiceSchedule(service=serviceObject,day=day,checked=checked,open_time=stand_open_time,close_time=stand_close_time)
                        ServiceScheduleObject.save()
                                    
                        
            
            service_user = serviceObject.user
            uoi_obj = UserOtherInfo.objects.get(user=service_user)
            if uoi_obj.total_services_count == "" or None:
                uoi_obj.total_services_count = 1
            else:
                uoi_obj.total_services_count = uoi_obj.total_services_count + 1
            
            uoi_obj.save()
            

            qa_list = data['QA']
            print("<-------_____------------QA List----------------->",qa_list)
            for qa_obj in qa_list:

                # if lang == en:
                question_id = qa_obj['question_id']
                Question_Object = QuestionFilledByAdmin.objects.get(id=question_id)
                answer = qa_obj['answer']
                question_text = qa_obj['question_text']
                username = user.get_full_name()
                service_name = serviceObject.service_name
                service_id = serviceObject
                provider = user
                # if lang == "en":
                #     option_selected_qs = OptionsFilledbyAdmin.objects.filter(question=Question_Object).filter(Option1=answer)
                # elif lang == "ar":
                #     option_selected_qs = OptionsFilledbyAdmin.objects.filter(question=Question_Object).filter(Option1_in_arabic=answer)
                
            
                
                try:
                    if question_text in ["Where do you prefer to provide Service ?","أين تفضل تقديم الخدمة؟"]:

                        serviceObject.service_place = answer
                        serviceObject.save()
                    
                    elif question_text in ["How far are you willing to travel to provide the service ?","إلى أي مدى أنت على استعداد للسفر لتقديم الخدمة؟"]:
                        serviceObject.distance_limit = answer
                        serviceObject.save()
                    
                    elif question_text in ["How many years of experience do you have ?","كم سنة من الخبرة لديك؟"]:
                        serviceObject.levelskill = answer
                        serviceObject.save()

                    elif question_text in ["At what price rate do you provide service ?","ما هو سعر السعر الذي تقدمه الخدمة؟"]:
                        serviceObject.pricing_timing_unit = answer
                        serviceObject.save()
                except Exception as e:
                    print("<-----------Some Exception occured in Service Creation----------->",e)

                
                lang = data['current_language']

                if lang in ["English","english","en"]:
                    AnswerObject = AnswerByProvider(service=service_id,
                                                    user=provider,
                                                    question=Question_Object,
                                                    option_Selected = answer,
                                                    user_name = username,
                                                    service_name = service_name,
                                                    question_string = question_text
                                                    )
                    AnswerObject.save()
                    serviceObject.service_langugae = "en"
                    serviceObject.save()

                elif lang in ["Arabic","arabic","ar"]:
                    AnswerObject = AnswerByProvider(service=service_id,
                                                    user=provider,
                                                    question=Question_Object,
                                                    option_Selected_in_arabic = answer,
                                                    user_name = username,
                                                    service_name = service_name,
                                                    question_string_arabic = question_text
                                                    )
                    AnswerObject.save()                    
                    serviceObject.service_langugae = "ar"
                    serviceObject.save()
                
                else:
                    return Response({"msg":"Invalid language code"},status=HTTP_400_BAD_REQUEST)
                print("<-------------------ANswer Object---------------->",AnswerObject)

                
                
            
            
            
            return Response(request.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



# Category
class CategoryListAPIView(APIView):
    # authentication_classes = [JSONWebTokenAuthentication]	
    # permission_classes = (IsAuthenticated,)
    def get(self,request):
        lang = request.GET.get("lang")
        queryset = Category.objects.all()
        final_list =[]
    
        for category in queryset:
            subcategoryqs = SubCategory.objects.filter(category = category)
            
            if lang == "ar": #Arabic
                subcategoryserialized = SubCategoryListArabicSerializer(subcategoryqs,many=True).data
                categoryserialized = CategoryListArabicSerializer(category).data
                categoryserialized['subcategories'] = subcategoryserialized
                final_list.append(categoryserialized)

            elif lang == "en": #English
                subcategoryserialized = SubCategoryListSerializer(subcategoryqs,many=True).data
                categoryserialized = CategoryListSerializer(category).data
                categoryserialized['subcategories'] = subcategoryserialized
                final_list.append(categoryserialized)  


        return Response(final_list, status=HTTP_200_OK)


# Feedback to MeenFee Service

# class MeenFeeFeedbackCreateAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JSONWebTokenAuthentication]
#     def post(self, request, format=None):
#         data = request.data
#         serializer = MeenFeeFeedbackCreateSerializer(data=data)
#         if serializer.is_valid():
#             serializer.validated_data['user'] = request.user
#             serializer.validated_data['timestamp'] = datetime.now().time()
#             serializer.save()
#             return Response(serializer.data, status=HTTP_200_OK)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# Help and Support
class HelpAndSupportListAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JSONWebTokenAuthentication]
    def get(self, request):
        lang = request.GET.get("lang")
        isarabic = request.GET.get("arabic")
        queryset = HelpAndSupport.objects.all()
        if lang == "Arabic":
            serializer = HelpAndSupportListArabicSerializer(queryset,many=True).data
        else:
            serializer = HelpAndSupportListSerializer(queryset,many=True).data
        return Response(serializer, status=HTTP_200_OK)



class QuestionAnswerForRequestorList(APIView):

    # authentication_classes = [JSONWebTokenAuthentication]	
    # permission_classes = (IsAuthenticated,)
    def get(self,request,format = None):
        subcategory_id = request.GET.get("subcategoryid")
        # isarabiclang = request.GET.get("arabic")
        lang = request.GET.get("lang")

        if lang == "ar":
            pass
        elif lang == "en":
            pass
        else:
            return Response({"msg":"Invalid language code"},status=HTTP_400_BAD_REQUEST)

        
        subcategory_object = SubCategory.objects.get(id=subcategory_id)
#         qs_questions = QuestionFilledByAdmin.objects.filter(SubCategory = subcategoryid)
        common_question_qs = QuestionFilledByAdmin.objects.filter(SubCategory = subcategory_object)
        questions_serialized = question_for_requestor_serialzer(common_question_qs,many=True).data
        return Response(questions_serialized,status=HTTP_200_OK)
    
    


class AnswerbyProviderCreateAPIView(APIView):

    # authentication_classes = [JSONWebTokenAuthentication]	
    # permission_classes = (IsAuthenticated,)

    print("<---------------In Function------------------>" )
    
    def post(self, request, format=None):
        isarabiclang = request.GET.get("arabic")
        data = request.data
        mutabledata = data.copy()
        # a = dict()
        print("<---------------In Function------------------>",mutabledata)
        # a.append(request.user.id)
        data.update({"user":request.user.id})

        if isarabiclang == "true":
            serializer = AnswerbyProviderCreateArabicSerializer(data=data,many=True)
        else:
            serializer = AnswerbyProviderCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['user_name'] = request.user.get_full_name()
            questionid = serializer.validated_data['question']
            print("<-------QuestionID------------>",questionid)
            print()
            QuestionObject = QuestionFilledByAdmin.objects.get(id=data['question'])
            serializer.validated_data['question_string'] = QuestionObject.question_for_provider
            serializer.save()
            return Response(request.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class AnswerByProv(APIView):
    def post(self,request,format=None):
        # isarabiclang = request.GET.get("arabic")
        data = request.data
        print("<-------------------->",data)
        queryset = AnswerByProvider.objects.all()
        write_serializer_class = AnswerbyProviderCreateSerializer
        return Response({"msg":"Success"},status=HTTP_200_OK)


class QuestionAnswerForProviderList(APIView):

    authentication_classes = [JSONWebTokenAuthentication]	
    # permission_classes = (IsAuthenticated,)

    def get(self,request,format = None):
        subcategoryid = request.GET.get("subcategoryid")
        isarabiclang = request.GET.get("arabic")
        qs_questions = QuestionFilledByAdmin.objects.filter(SubCategory = subcategoryid)
        if isarabiclang == "true":
            Serializer = QuestionForProviderListArabicSerializer(qs_questions,many=True).data
        else:
            Serializer = QuestionForProviderListSerializer(qs_questions,many =True).data
        return Response(Serializer, status=HTTP_200_OK)


class UserProfileUpdateAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]	
    permission_classes = (IsAuthenticated,)

    def put(self,request,format=None):
        userinfo = request.data
        user = request.user.id
        userObj = UserOtherInfo.objects.get(user = user)
        serializer = UserOtherInfoUpdate(data=userinfo)
        if serializer.is_valid():
            serializer.validated_data['idcard'] = userinfo['idcard']
            serializer.validated_data['phone'] = userinfo['phone']
            serializer.validated_data['name'] = userinfo['name']
            serializer.validated_data['bio'] = userinfo['bio']
            serializer.validated_data['user_address'] = userinfo['user_address']
            serializer.save()
            return Response(request.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
class FcmTokenUpdateAPIView(APIView):

    #authentication_classes = [JSONWebTokenAuthentication]	
    #permission_classes = (IsAuthenticated,)

    def post(self,request,format=None):
        user = request.user
        data =  request.data
        try:
            print("<---------------------FCM Token UPdate API View Data---------------->",data)
            print("<---------------------FCM Token Update API View User----------------->",user)
            userotherinfoObj = UserOtherInfo.objects.get(user = user)
            # userotherinfoObj.fcm_token = request.GET.get("fcmtoken")
            userotherinfoObj.fcm_token = data['fcm_token']
            userotherinfoObj.save()
            return Response({"status:sucess"}, status=HTTP_200_OK)
        except:
            return Response({"NULL_RESPONSE"},status=HTTP_200_OK)




class NewBooking(APIView):
    def post(self,request,format=None):
        
        day_dict = {
            "Monday"    : 0,
            "Tuesday"   : 1,
            "Wednesday" : 2,
            "Thursday"  : 3,
            "Friday"    : 4,
            "Saturday"  : 5,
            "Sunday"    : 6
            }
        day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        
        DEFAULT_NEXT_SLOT = False
        SLOT_ASSIGNED = True
        selected_slot = None
        
        creation_time = datetime.now()
        data = request.data
        user = request.user
        incoming_provider_id = data['provider_id']
        try:
            admin_charges = data['admin_charges']
            service_charges = data['service_charges']
        except:
            pass

        UserOtherInfoObject = UserOtherInfo.objects.get(user = incoming_provider_id)
        provider_id_modified = UserOtherInfoObject.id
        ProviderUserObject = User.objects.get(id=incoming_provider_id)
        data['provider_id'] = provider_id_modified
        
        
        if ProviderUserObject == user:
            return Response({"msg":"Invalid booking attempt.You cannot book yourself."},status=HTTP_400_BAD_REQUEST)

        
        
        
        quote_requested = data['quote_requested']
        if quote_requested == True:
            quote_by_requestor = True
        else:
            quote_by_requestor = False
        
        

        serializer = NewBookingSerializer(data=data)
        ProviderObject = User.objects.get(id=incoming_provider_id)
        ProviderFull  = UserOtherInfo.objects.get(id = provider_id_modified)
        ServiceObj     = Service.objects.get(id = data['service_ID'])



        service_time_available = False
        service_slot_id_available = False
        service_date_available = False
        
        try:
            if 'service_time' in data:
                if data['service_time'] != "" or data['service_time'] != None:
                    service_time_incoming = data['service_time']
                    service_time_available = True
            
            if 'service_slot_id' in data:
                if data['service_slot_id'] != "" or data['service_slot_id'] != None:
                    service_slot_id_incoming = data['service_slot_id']
                    service_slot_id_available = True
                
            if 'service_date' in data:
                if data['service_date'] != "" or data['service_date'] != None:
                    service_date_incoming = data['service_date']
                    service_date_available = True
            
            
            
            if LOCK_BOOKED_SLOT:
                
                if service_slot_id_available:
                    pass
                
                else:
                    if service_time_available:
                        if service_date_available:
                            service_date_object = datetime.strptime(service_date_incoming,EXTERNAL_DATE_FORMAT)
                            try:
                                service_time_object = datetime.strptime(service_time_incoming,EXTERNAL_TIME_FORMAT)
                            except:
                                service_time_object = datetime.strptime(service_time_incoming,"%H:%M:%S")                                

                            weekday_number = service_date_object.weekday()
                            weekday_string = day_list[weekday_number]
                            
                            ServiceScheduleQS = ServiceSchedule.objects.filter(service = ServiceObj).filter(day=weekday_string)
                            
                            for schedule in ServiceScheduleQS:
                                slot_open_time = schedule.open_time.strftime("%H:%M:%S")
                                slot_close_time = schedule.close_time.strftime("%H:%M:%S")
                                service_time   = service_time_object.strftime("%H:%M:%S")
                                
                                if slot_open_time <= service_time and service_time <= slot_close_time:
                                    current_capacity = schedule.service_capacity
                                    if current_capacity == 0:
                                        selected_slot = schedule
                                        pass
                                    else:
                                        new_capacity = current_capacity - 1
                                        schedule.service_capacity = new_capacity
                                        schedule.save()
                                        selected_slot = schedule
                                        SLOT_ASSIGNED = True
                                        break
                                
                            if not SLOT_ASSIGNED:
                                return Response({"msg":"Service Provider does not provide service on the selected date and time"})
                                          
        except Exception as e:
            print("<----------------_Some Exception occured---------------->",e)
            pass






        Provider_Name = ProviderObject.get_full_name()
        RequesterUserOtherInfoObject = UserOtherInfo.objects.get(user=user)

        if serializer.is_valid():
            serializer.validated_data['requestor'] = user.get_full_name()
            serializer.validated_data['requestor_id'] = RequesterUserOtherInfoObject
            serializer.validated_data['provider'] = Provider_Name
            serializer.validated_data['service_name'] = ServiceObj.service_name
            serializer.validated_data['service_ID'] = ServiceObj
            serializer.validated_data['created'] = creation_time
            serializer.validated_data['booking_id'] = str("MNF" + creation_time.strftime("%Y%m%d%H%M%S%f") )
            serializer.validated_data['accepted_by_requester'] = True
            message_body = "You have a new Booking Request from " + user.get_full_name()
            requestor_id    = serializer.validated_data['requestor_id']           

            data['booking_id'] = serializer.validated_data['booking_id']
            
            from_UserOtherInfoObject  = UserOtherInfo.objects.get(user=user)

            InAppBookingNotificationsObject = InAppBookingNotifications(
                from_user_id = from_UserOtherInfoObject,
                from_user_name = serializer.validated_data['requestor_id'],
                to_user_id = ProviderFull,
                to_user_name = ProviderUserObject.get_full_name(),
                notification_type = "New Booking Request",
                notification_title = message_body,
                service_name = serializer.validated_data['service_name'],
                requested_service_time = timezone.now(),
                requested_service_date= datetime.now(),
                notification_time = timezone.now(),
                notification_date = datetime.now(),
                service_pricing = ServiceObj.service_pricing,
                service_place = "At Provider's Place",
                to_user_usertype = PROVIDER_STRING,
                )
            
            InAppBookingNotificationsObject.save()

            fcm_provider = ProviderFull.fcm_token

            try:
                send_to_one(fcm_provider,message_body,"New Booking Request")
            except:
                pass
            

            serializer.save()
            UOI_Object_Requestor = UserOtherInfo.objects.get(user=user.id)
            data = request.data

            incoming_booking_ID = data['booking_id']
            payment_method = data['payment_method']
            
            
            NewBookingObject = NewBookingModel.objects.get(booking_id__exact = incoming_booking_ID)
            NewBookingObject.quote_requested_by_requestor = quote_by_requestor
            NewBookingObject.service_charges = ServiceObj.service_pricing
            service_charge = str(ServiceObj.service_pricing)
            NewBookingObject.service_charge_rate = str(service_charge + " " + ServiceObj.pricing_timing_unit)

            NewBookingObject.service_slot_id = selected_slot

            try:
                NewBookingObject.service_charges = service_charges
                NewBookingObject.admin_charges = admin_charges
            except:
                pass

            booking_request_timestamp = timezone.now()
            print("<---------------------Booking Request Time------------->",booking_request_timestamp)
            # if BOOKING_TIME_LIMIT_DEBUG:
            #     auto_cancellation_time =  booking_request_timestamp + timedelta(minutes=BOOKING_TIME_LIMIT_MIN)
            # else:
            auto_cancellation_time =  booking_request_timestamp + timedelta(hours = BOOKING_TIME_LIMIT_HOURS)
            print("<---------------------Auto Cancellation Time------------->",auto_cancellation_time)
            NewBookingObject.auto_cancellation_time = auto_cancellation_time

            NewBookingObject.point_of_service = ServiceObj.service_place

            NewBookingObject.save()
            
            if service_time_available and service_date_available:
                service_time_object = datetime.strptime(service_time_incoming,EXTERNAL_TIME_FORMAT)
                service_date_object = datetime.strptime(service_date_incoming,EXTERNAL_DATE_FORMAT)
                
                NewBookingObject.service_date = service_date_object
                NewBookingObject.service_time = service_time_object
                NewBookingObject.save()
            
            else:
                
                
            
                if DEFAULT_NEXT_SLOT:
                    
                    day_dict = {
                        "Sunday" : 0,
                        "Monday" : 1,
                        "Tuesday" : 2,
                        "Wednesday" : 3,
                        "Thursday" : 4,
                        "Friday" : 5,
                        "Saturday" : 6
                        }
                    day_list = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
                    ServiceScheduleQS = ServiceSchedule.objects.filter(service=ServiceObj)
                    today_weekday_number = int(datetime.strftime(creation_time,"%w"))
                    
                    available_days = ["","","","","","",""]
                    
                    for schedule in ServiceScheduleQS:
                        schedule_day = schedule.day
                        day_number = day_dict[schedule_day]
                        available_days[day_number] = day_number
                    
                    
                    day_pointer = today_weekday_number
                    
                    while True:
                        if available_days[day_pointer] == "":
                            day_pointer = (day_pointer + 1) % 7
                        else:
                            
                            
                            break
                    
                    if day_pointer == today_weekday_number:
                        
                        day = day_list[today_weekday_number]
                        slots_qs = ServiceSchedule.objects.filter(day=day)
                        
                        slot_open =[]
                        for slot in slots_qs:
                            slot_open.append(slot.open_time.strftime("%H:%M:%S"))
                        
                        sorted_open_time = sorted(slot_open)
                        
                        request_time = creation_time.strftime("%H:%M:%S")
                        
                        service_time = None
                        service_day_number = None
                        
                        for i in sorted_open_time:
                            if i >= request_time:
                                service_time = i
                                service_day_number = today_weekday_number
                                break
                        
                        if service_time == None:
                            
                            day_pointer = (today_weekday_number+1) % 7
                            
                            while True:
                                if available_days[day_pointer] == "":
                                    day_pointer = (day_pointer + 1) % 7
                                else:
                                    break
                            
                            day = day_list[day_pointer]
                            slots_qs = ServiceSchedule.objects.filter(day=day)
                            
                            slot_open = []
                            for slot in slots_qs:
                                slot_open.append(slot.open_time.strftime("%H:%M:%S"))
                                
                            sorted_open_time = sorted(slot_open)
                            
                            service_time = sorted_open_time[0]
                            service_day_number = day_pointer
                            
                        
                        
                        
                        
                    else:
                        NewBookingObject.service_date = datetime.now()
                        NewBookingObject.service_time = datetime.now()
                        NewBookingObject.save()
                        
            
            if payment_method == "Card":
                service    = data['service_ID']
                serviceObject = Service.objects.get(id=service)
                UOI_Object_Provider = UserOtherInfo.objects.get(user=serviceObject.user)
                service_charges = ServiceObj.service_pricing
                LivePaymentsObject = LivePayments(
                    payment_method = payment_method,
                    payment_request_date =  timezone.now(),
                    payment_request_time =  timezone.now(),
                    payment_from         =  UOI_Object_Requestor,
                    payment_to      =   UOI_Object_Provider,
                    booking_ID      =   incoming_booking_ID,
                    service         =   ServiceObj,
                    service_charges =   service_charges
                    )
                LivePaymentsObject.save()
            else:
      
                service   = data['service_ID']
                serviceObject  =    Service.objects.get(id=service)
                UOI_Object_Provider = UserOtherInfo.objects.get(user=serviceObject.user)
                service_charges = ServiceObj.service_pricing

                LivePaymentsObject  = LivePayments(
                    payment_method  =   payment_method,
                    payment_request_date = timezone.now(),
                    payment_request_time = timezone.now(),
                    payment_from    =  UOI_Object_Requestor,
                    payment_to      = UOI_Object_Provider,
                    booking_ID      =   incoming_booking_ID,
                    service         =   ServiceObj,
                    service_charges = service_charges
                    )
                fcm_receiver_token = UOI_Object_Provider.fcm_token
                
                try:
                    send_to_one(fcm_receiver_token,"You have a new booking request with cash payment mode. Please collect your waiver form from the admin.","New Cash Payment Booking Request")
                except:
                    pass

                LivePaymentsObject.save()          
            NewBookingObject.payment_mode = payment_method
            NewBookingObject.save()
            return Response(data,status=HTTP_200_OK)
        else:
            print("<---------------_Serialzier Error----------------->",serializer.errors)
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)









class ViewPendingActionsOnProviderEnd(APIView):
    '''
    This API is used to view the pending actions on provider end.
        
    '''

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self,request,format=None):
        user = request.user
        UserOtherInfoObject = UserOtherInfo.objects.get(user=user)
        usertype = UserOtherInfoObject.usertype
        if usertype == "provider" or usertype == "Provider":
            BookingObj = NewBookingModel.objects.filter(provider_id=UserOtherInfoObject.id). \
            filter(Q(accepted_by_provider = False) | Q(accepted_by_requester = False)). \
            exclude(booking_cancelled = True).order_by('service_date','service_time')
            serializer = PendingActionsSerializer(BookingObj,many=True,context={'uoi_object_id':UserOtherInfoObject.id}).data

        
        else:
            BookingObj = NewBookingModel.objects.filter(requestor_id=UserOtherInfoObject.id). \
            filter(Q(accepted_by_provider = False) | Q(accepted_by_requester = False)). \
            exclude(booking_cancelled = True).order_by('service_date','service_time')            
            serializer = PendingActionsSerializer(BookingObj,many=True,context={'uoi_object_id':UserOtherInfoObject.id}).data

        
        return Response(serializer,status=HTTP_200_OK)


class ViewPendingActionsOnRequesterEnd(APIView):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self,request,format=None):
        user = request.user
        UserOtherInfoObject = UserOtherInfo.objects.get(user= user)
        
        usertype = UserOtherInfoObject.usertype
        
        if usertype == "provider" or usertype == "Provider":
            BookingObj = NewBookingModel.objects.filter(requestor_id=UserOtherInfoObject.id). \
            filter(Q(accepted_by_provider = False) | Q(accepted_by_requester = False)). \
            exclude(booking_cancelled = True).order_by('service_date','service_time')
            serializer = PendingActionsSerializer(BookingObj,many=True,context={'uoi_object_id':UserOtherInfoObject.id}).data
        else:

            BookingObj = NewBookingModel.objects.filter(requestor_id=UserOtherInfoObject.id). \
            filter(Q(accepted_by_provider = False) | Q(accepted_by_requester = False)). \
            exclude(booking_cancelled = True).order_by('service_date','service_time')
            serializer = PendingActionsSerializer(BookingObj,many=True,context={'uoi_object_id':UserOtherInfoObject.id}).data
        return Response(serializer,status=HTTP_200_OK)




class ViewActiveBookingsRequestor(APIView):
    # This API View is used to view the bookings which are have the pending flag set
    
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self,request,format=None):
        user = request.user
        UserOtherInfoObject = UserOtherInfo.objects.get(user= user)
        
        if UserOtherInfoObject.usertype == "provider" or UserOtherInfoObject.usertype == "Provider":
            BookingObj = NewBookingModel.objects.filter(provider_id=UserOtherInfoObject.id). \
            filter(accepted_by_provider = True,accepted_by_requester = True). \
            exclude(Q(booking_cancelled = True)|Q(booking_completed = True)).order_by('service_date','service_time')
            serializer = PendingActionsSerializer(BookingObj,many=True,context={'uoi_object_id':UserOtherInfoObject.id}).data
        else:
            BookingObj = NewBookingModel.objects.filter(requestor_id=UserOtherInfoObject.id). \
            filter(accepted_by_provider = True,accepted_by_requester = True). \
            exclude(Q(booking_cancelled = True)|Q(booking_completed = True)).order_by('service_date','service_time')
            serializer = PendingActionsSerializer(BookingObj,many=True,context={'uoi_object_id':UserOtherInfoObject.id}).data
 
        return Response(serializer,status=HTTP_200_OK)


class ViewActiveBookingsProvider(APIView):
    # This API View is used to view the bookings which are have the pending flag set
    
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self,request,format=None):
        user = request.user
        UserOtherInfoObject = UserOtherInfo.objects.get(user= user)

        if UserOtherInfoObject.usertype == "provider" or UserOtherInfoObject.usertype == "Provider":
            BookingObj = NewBookingModel.objects.filter(provider_id=UserOtherInfoObject.id). \
            filter(accepted_by_provider = True,accepted_by_requester = True). \
            exclude(Q(booking_cancelled = True)|Q(booking_completed = True)).order_by('service_date','service_time')
            serializer = PendingActionsSerializer(BookingObj,many=True,context={'uoi_object_id':UserOtherInfoObject.id}).data
        else:
            BookingObj = NewBookingModel.objects.filter(requestor_id=UserOtherInfoObject.id). \
            filter(accepted_by_provider = True,accepted_by_requester = True). \
            exclude(Q(booking_cancelled = True)|Q(booking_completed = True)).order_by('service_date','service_time')
            serializer = PendingActionsSerializer(BookingObj,many=True,context={'uoi_object_id':UserOtherInfoObject.id}).data
        return Response(serializer,status=HTTP_200_OK)


class RescheduleBooking(APIView):
    def put(self,request,format=None):
        request_time = datetime.now()
        day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        
        user = request.user
        data = request.data
        try:
            UserObject = User.objects.get(id=user.id)
            print("<-------------------------------User Object-------------------->",UserObject)
        except:
            return Response({"msg":"User does not exist."},status=HTTP_400_BAD_REQUEST)


        
        bookingID = data['booking_id']

        try:
            BookingObj = NewBookingModel.objects.get(booking_id = bookingID)
        except:
            return Response({"msg":"Booking does not exist."},status=HTTP_400_BAD_REQUEST)
        
        re_service_date     =   data['service_date']
        raw_service_time    = data['service_time']
        re_service_time     =   raw_service_time.strip()
        
        if NEW_TIME_FORMAT == False:
            re_service_time_obj = datetime.strptime(re_service_time,"%H:%M")
        else:
            re_service_time_obj = datetime.strptime(re_service_time,EXTERNAL_TIME_FORMAT)
        
        
                        
        re_service_time_str = re_service_time_obj.strftime("%H:%M")

        CheckQS             =   NewBookings.objects.filter(booking_id=bookingID)
        if len(CheckQS) > 1:
            return Response({"msg":"More than two bookings exist for the given ID"},status=HTTP_400_BAD_REQUEST)
            print("<-------------Some Error Occured. QS returned more than one bookings------------------->",CheckQS)
        
        BookingObject = CheckQS[0]
        service_id = BookingObject.service_ID
        
        if NEW_TIME_FORMAT == False:
            temp_day            =   datetime.strptime(re_service_date,'%d-%m-%Y').weekday()
        else:
            temp_day            =   datetime.strptime(re_service_date,EXTERNAL_DATE_FORMAT).weekday()            
            
        day_string = day_list[temp_day]
        ServiceScheduleQS   =   ServiceSchedule.objects.filter(service=service_id,day=day_string)

        if len(ServiceScheduleQS) < 1:
            return Response({"msg":"Service Provider does not provide service on this day"},status=HTTP_400_BAD_REQUEST)

        flag = 0

        for schedule in ServiceScheduleQS:
            
            schedule_open_str = schedule.open_time.strftime("%H:%M")
        
            schedule_close_str = schedule.close_time.strftime("%H:%M")

            if not (re_service_time_str >= schedule_open_str and re_service_time_str <= schedule_close_str):
                flag = 1
            else:
                flag = 0
                break

        
        if flag ==1:
            return Response({"msg":"Service Provider is not available at your requested date and time. Kindly Reschedule",
            "day":temp_day,
            "available_slots":""},status=HTTP_400_BAD_REQUEST)
            
            
        if not NEW_TIME_FORMAT:
            temp_date           =   datetime.strptime(re_service_date,'%d-%m-%Y')
        else:
            temp_date           =   datetime.strptime(re_service_date,EXTERNAL_DATE_FORMAT)
            
        formatted_date      =  datetime.strftime(temp_date,'%Y-%m-%d')
        
        if not NEW_TIME_FORMAT:
            temp_time           =   datetime.strptime(re_service_time,'%H:%M')
        else:
            temp_time           =   datetime.strptime(re_service_time,EXTERNAL_TIME_FORMAT)
        
        formatted_time      =   datetime.strftime(temp_time,'%H:%M:%S')
        

        
        UOIObject = UserOtherInfo.objects.get(user=user)

        if UOIObject.usertype == "Provider" or UOIObject.usertype == "provider":

            InAppBookingNotificationsObject  = InAppBookingNotifications(
                from_user_id    =   UOIObject,
                from_user_name  =   UserObject.get_full_name(),
                to_user_id      =   BookingObj.requestor_id,
                to_user_name    =   BookingObj.requestor,
                notification_type   =   "Reschedule Request",
                notification_title  =   "Service Provider is not available at your requested date and time.Kindly Reschedule." + "(Booking ID: " + BookingObj.booking_id +")",
                service_name        =   BookingObj.service_name,
                to_user_usertype    =   REQUESTOR_STRING
            )
            InAppBookingNotificationsObject.save()
            fcm_receiver = BookingObj.requestor_id
            UserOtherInfoObject = UserOtherInfo.objects.get(id=fcm_receiver.id)
            fcm_receiver_token =    UserOtherInfoObject.fcm_token
            message_body = "Service Provider is not available at your requested date and time.Kindly Reschedule." + "(Booking ID : " + BookingObj.booking_id + ")",
            
            try:
                send_to_one(fcm_receiver_token,message_body,"Reschedule Request")
            except:
                pass

            BookingObj.accepted_by_requester = False
            BookingObj.save()
            return Response({"msg","OK"},status=HTTP_200_OK)
        else:
            InAppBookingNotificationsObject = InAppBookingNotifications(
                from_user_id        =   UOIObject,
                from_user_name      =   UserObject.get_full_name(),
                to_user_id          =   BookingObj.provider_id,
                to_user_name        =   BookingObj.provider,
                notification_type   =   "Reschedule Request",
                notification_title  =   "Service Requestor wants to reschedule the booking " + "(Booking ID: " + BookingObj.booking_id +")", 
                service_name        =   BookingObj.service_name,
                notification_time   =   timezone.now(),
                notification_date   =   datetime.now(),
                rescheduled_date    =   formatted_date,
                rescheduled_time    =   formatted_time,
                to_user_usertype    =   PROVIDER_STRING
            )

            re_service_date     =   data['service_date']

            if not NEW_TIME_FORMAT:
                temp_date           =   datetime.strptime(re_service_date,'%d-%m-%Y')
            else:
                temp_date           =   datetime.strptime(re_service_date,EXTERNAL_DATE_FORMAT)
                
            formatted_date       =  datetime.strftime(temp_date,'%Y-%m-%d')
            
            if not NEW_TIME_FORMAT:
                temp_time           =   datetime.strptime(re_service_time,'%H:%M')
            else:
                temp_time           =   datetime.strptime(re_service_time,EXTERNAL_TIME_FORMAT)
                
            formatted_time      =   datetime.strftime(temp_time,'%H:%M:%S')
            

            InAppBookingNotificationsObject.save()

            fcm_receiver = BookingObj.requestor_id
            UserOtherInfoObject = UserOtherInfo.objects.get(id=fcm_receiver.id)
            fcm_receiver_token =    UserOtherInfoObject.fcm_token
            message_body = "Service Requestor wants to reschedule the booking " + "(Booking ID: " + BookingObj.booking_id +")",
            try:
                send_to_one(fcm_receiver_token,message_body,"Reschedule Request")
            except:
                pass
            BookingObj.accepted_by_provider = False

            BookingObj.rescheduled_service_date = formatted_date
            
            try:
                BookingObj.reschedule_request_date = request_time
                BookingObj.reschedule_request_time = request_time
            except:
                pass
            
            BookingObj.rescheduled_service_time = formatted_time
            
            if NEW_RESCHEDULE_METHOD:
                BookingObj.cancellation_date = cancel_request_time
                BookingObj.cancellation_time = cancel_request_time
                BookingObj.booking_cancelled = True
                
                Rescheduled_Booking_Object = NewBookingModel(
                    booking_id = "MNF" + request_time.strftime("%Y%m%d%H%M%S%f"),
                    created = request_time,
                    
                    )
                
                
                if usertype == "requester" or usertype == "Requester":
                    BookingObject.cancelled_by_provider = True
                    InAppBookingNotificationsObject = InAppBookingNotifications(
                        from_user_id = UserOtherInfoObject,
                        from_user_name = UserObject.get_full_name(),
                        to_user_id = BookingObj.requestor_id,
                        to_user_name = BookingObj.requestor,
                        notification_type = "Booking Cancelled for Rescheduling",
                        notification_title = "Your booking request " + "(Booking ID: " + BookingObject.booking_id +")"+" has been cancelled for rescheduling.Kindly do a new booking.",
                        service_name      = BookingObj.service_name,
                        notification_time = timezone.now(),
                        notification_date  = datetime.now(),
                        to_user_usertype = REQUESTOR_STRING
                        )

                InAppBookingNotificationsObject.save()
            else:
                BookingObj.service_date = formatted_date
                BookingObj.service_time = formatted_time
                BookingObj.save()               
            
            
            BookingObj.save()
            return Response({"msg":"Success"},status=HTTP_200_OK)





class AcceptBooking(APIView):
    def put(self,request,format=None):
        DEBUG = False

        if DEBUG == True:
            accept_time = datetime(2019,7,11,14,6)
        else:
            accept_time = datetime.now()

        today = accept_time.strftime("%Y-%m-%d")

        data = request.data
        bookingid = data['booking_id']

        NewBookingObj = NewBookingModel.objects.get(booking_id__exact=bookingid)

        if NewBookingObj.auto_cancelled == True or NewBookingObj.booking_cancelled == True or NewBookingObj.booking_completed == True:
            return Response({"msg":"Time Limit Exceeded"},status=HTTP_400_BAD_REQUEST)

        creation_time = NewBookingObj.created

        service_date  = NewBookingObj.service_date

        service_date_formatted = service_date.strftime("%Y-%m-%d")

        if (NewBookingObj.accepted_by_provider == True) :
            print("<-------------------------Booking already accepted---------------------->")
            return Response({'accepted':False,"msg":"Booking already accepted"},status=HTTP_400_BAD_REQUEST)

        elif service_date_formatted == today:

            if (accept_time - creation_time).total_seconds()/60 > 180:
                NewBookingObj.booking_cancelled = True
                NewBookingObj.cancelled_by_provider = True
                NewBookingObj.cancelled_by_requestor = True
                NewBookingObj.save()
                return Response({'accepted':False,"msg":"Time Limit Exceeded"},status=HTTP_400_BAD_REQUEST)
            else:
                response_time = (accept_time - creation_time).total_seconds()/60
                
                UOI_Object = NewBookingObj.provider_id
                previous_count = UOI_Object.response_within_count
                previous_time  = UOI_Object.response_within
                
                
                if previous_time == 0 or previous_time == "" or previous_time == None:
                    new_sum = int(response_time)
                    UOI_Object.response_within = new_sum
                    if previous_count == 0 or previous_count == "" or previous_count == None:
                        UOI_Object.response_within_count = 1
                        UOI_Object.save()
                        
                else:
                    previous_sum = previous_count * previous_time
                    new_sum =   previous_sum + int(response_time)
                    new_count = previous_count + 1
                    new_avg_response_time = int(new_sum/new_count)
                    UOI_Object.response_within = new_avg_response_time
                    UOI_Object.response_within_count = new_count
                    UOI_Object.save()
                
                NewBookingObj.accepted_by_provider = True
                NewBookingObj.task_status = 'In Progress'
                NewBookingObj.save()
                
                fcm_receiver_user_object = NewBookingObj.requestor_id
                fcm_token = fcm_receiver_user_object.fcm_token
                message_title = "Request Accepted"
                message_body = "Service provider has accepted your booking request."
                try:
                    send_to_one(fcm_token,message_body,message_title)
                except:
                    pass
                requestor_uoi_object = NewBookingObj.requestor_id
                provider_uoi_object  = NewBookingObj.provider_id
                print("<------------------Requestor UOI Object----------------->",requestor_uoi_object)
                print("<------------------Provider UOI Object------------------>",provider_uoi_object)

                requestor_user_object = requestor_uoi_object.user
                

                provider_user_object  = provider_uoi_object.user
                print("<-------------------Requestor User Object------------------>",requestor_user_object)
                print("<------------------Retreived User Object----------------->",requestor_user_object)
                
                
                
                InAppBookingNotificationObject = InAppBookingNotifications(
                    from_user_id = provider_uoi_object,
                    from_user_name = provider_user_object.get_full_name(),
                    to_user_id  = requestor_uoi_object,
                    to_user_name = requestor_user_object.get_full_name(),
                    notification_type = "Booking Accepted",
                    notification_title = "Your Booking request has been accepted",
                    service_name       = NewBookingObj.service_name,
                    notification_time  = timezone.now(),
                    notification_date  = timezone.now(),
                    to_user_usertype    = REQUESTOR_STRING
                    )
                
                InAppBookingNotificationObject.save()
                
                return Response({'accepted':True,"msg":"Service Request Accepted"},status=HTTP_200_OK)
        elif service_date_formatted > today:
            print("<-------------------------Inside services after today----------------------->")
            print("<-----------------------Accept Time-------------------------->",accept_time)
            print("<-----------------------Accept Time Type------------------->",type(accept_time))
            print("<-----------------------Creation Time------------------------>",creation_time)
            print("<-----------------------Creation Time Type--------------------->",type(creation_time))
            print("<-----------------------Difference----------------------------->",((accept_time - creation_time).total_seconds()/60)/60)
            if (accept_time - creation_time).total_seconds()/60 > 1440:

                NewBookingObj.booking_cancelled = True
                NewBookingObj.cancelled_by_provider = True
                NewBookingObj.cancelled_by_requestor = True
                NewBookingObj.save()
                return Response({'accepted':False,"msg":"Time Limit Exceeded"},status=HTTP_400_BAD_REQUEST)
            else:
                response_time = (accept_time - creation_time).total_seconds()/60
                
                UOI_Object = NewBookingObj.provider_id
                print("<-------------UOI_Object fetched------------->",UOI_Object)
                previous_count = UOI_Object.response_within_count
                previous_time  = UOI_Object.response_within
                
                
                if previous_time == 0 or previous_time == "" or previous_time == None:
                    new_sum = int(response_time)
                    UOI_Object.response_within = new_sum
                    if previous_count == 0 or previous_count == "" or previous_count == None:
                        UOI_Object.response_within_count = 1
                        UOI_Object.save()
                        
                else:
                    previous_sum = previous_count * previous_time
                    new_sum =   previous_sum + int(response_time)
                    new_count = previous_count + 1
                    new_avg_response_time = int(new_sum/new_count)
                    UOI_Object.response_within = new_avg_response_time
                    UOI_Object.response_within_count = new_count
                    UOI_Object.save()
                
                
                NewBookingObj.accepted_by_provider =  True
                NewBookingObj.task_status = 'In Progress'
                NewBookingObj.save()



                fcm_receiver_user_object = NewBookingObj.requestor_id
                fcm_token = fcm_receiver_user_object.fcm_token
                message_title = "Request Accepted"
                message_body = "Service provider has accepted your booking request."

                try:
                    send_to_one(fcm_token,message_body,message_title)
                except:
                    pass

                requestor_uoi_object = NewBookingObj.requestor_id
                provider_uoi_object  = NewBookingObj.provider_id
                
                requestor_user_object = User.objects.get(id=requestor_uoi_object.user.id)
                provider_user_object  = User.objects.get(id=provider_uoi_object.user.id)
                
#                 requestor_user_object = User.objects.get(id=fcm_receiver_user_object.user)
                print("<------------------Retreived User Object----------------->",requestor_user_object)
                
                
                
                InAppBookingNotificationObject = InAppBookingNotifications(
                    from_user_id = provider_uoi_object,
                    from_user_name = provider_user_object.get_full_name(),
                    to_user_id  = requestor_uoi_object,
                    to_user_name = requestor_user_object.get_full_name(),
                    notification_type = "Booking Accepted",
                    notification_title = "Your Booking request has been accepted",
                    service_name       = NewBookingObj.service_name,
                    notification_time  = timezone.now(),
                    notification_date  = timezone.now(),
                    to_user_usertype    = REQUESTOR_STRING
                    )
                
                InAppBookingNotificationObject.save()    


                return Response({'accepted':True,"msg":"Service Request Accepted"},status=HTTP_200_OK)
        else:
            NewBookingObj.booking_cancelled = True
            NewBookingObj.cancelled_by_provider = True
            NewBookingObj.cancelled_by_requestor = True
            NewBookingObj.save()
            print("<---------------Invalid case------------------->")
            return Response({'accepted':False,"msg":"Time Limit Exceeded"},status=HTTP_400_BAD_REQUEST)




class MarkTaskCompleted(APIView):

    def put(self,request):
        data =  request.data
        user =  request.user
        if user.is_anonymous:
            return Response({"msg":"JWT missing in request"},status=HTTP_400_BAD_REQUEST)
        else:
            try:
                usertype = data['usertype']
            except:
                UOI_Object = UserOtherInfo.objects.get(user=user)
                usertype = UOI_Object.usertype
            
            booking_id = data['booking_id']
            NewBookingObj = NewBookingModel.objects.get(booking_id__exact = booking_id)

            if usertype in ["provider","Provider"]:
                NewBookingObj.booking_marked_completed_by_provider = True
                NewBooking.payment_incurred = True
                NewBookingObj.save()
                fcm_receiver_token = NewBookingObj.requestor_id.fcm_token
                message_body = "Provider has marked the appointment as complete"
                try:
                    send_to_one(fcm_receiver_token, message_body, "Appointment Complete")
                except:
                    pass
                InAppBookingNotificationsObject  =  InAppBookingNotifications(
                    from_user_id = NewBookingObj.provider_id,
                    from_user_name = NewBookingObj.provider_id.user.get_full_name(),
                    to_user_id = NewBookingObj.requestor_id,
                    to_user_name= NewBookingObj.requestor_id.user.get_full_name(),
                    notification_type = "Booking Completed",
                    notification_title = "Service Request has been marked completed by provider. Please mark the corresponding booking as completed on your end to initiate payment.",
                    service_name   = NewBookingObj.service_name,
                    notification_time = timezone.now(),
                    notification_date = timezone.now(),
                    to_user_usertype    = REQUESTOR_STRING
                    )
                InAppBookingNotificationsObject.save()
                return Response({"msg":"Task Marked as Completed"}, status=HTTP_200_OK)
            else:

                NewBookingObj.booking_marked_completed_by_requestor = True
                NewBookingObj.booking_completed = True
                NewBookingObj.payment_completed = True
                NewBookingObj.save()

                fcm_receiver_token = NewBookingObj.provider_id.fcm_token
                message_body = "Requestor has marked the appointment as complete."
                try:
                    send_to_one(fcm_receiver_token, message_body, "Appointment Complete")
                except:
                    pass
                InAppBookingNotificationsObject  =  InAppBookingNotifications(
                    from_user_id = NewBookingObj.requestor_id,
                    from_user_name = NewBookingObj.requestor_id.user.get_full_name(),
                    to_user_id = NewBookingObj.provider_id,
                    to_user_name= NewBookingObj.provider_id.user.get_full_name(),
                    notification_type = "Booking Completed",
                    notification_title = "Requester has marked the booking as completed.",
                    service_name   = NewBookingObj.service_name,
                    notification_time = timezone.now(),
                    notification_date = timezone.now(),
                    to_user_usertype    = PROVIDER_STRING
                    )
                InAppBookingNotificationsObject.save()

                LivePaymentObject = LivePayments.objects.get(booking_ID__exact=booking_id)

                SettledPaymentObject = SettledPayments(
                    payment_card                =   LivePaymentObject.payment_card,
                    payment_method              =   LivePaymentObject.payment_method,
                    payment_request_date        =   LivePaymentObject.payment_request_date,
                    payment_request_time        =   LivePaymentObject.payment_request_time,
                    payment_settle_date         =   timezone.now(),
                    payment_settle_time         =   timezone.now(),
                    service                     =   LivePaymentObject.service,
                    payment_from                =   LivePaymentObject.payment_from,
                    payment_to                  =   LivePaymentObject.payment_to,
                    booking_ID                  =   LivePaymentObject.booking_ID,
                    cash_paid_by_requestor      =   LivePaymentObject.cash_paid_by_requestor,
                    cash_collected_by_provider  =   LivePaymentObject.cash_collected_by_provider,
                    service_charges             =   LivePaymentObject.service_charges,
                    admin_charges               =   LivePaymentObject.admin_charges,
                    total_amount_paid           =   LivePaymentObject.service_charges +  LivePaymentObject.admin_charges,
                    payment_for                 =   "Completion"
                    )
                SettledPaymentObject.save()
                LivePaymentObject.delete()

                return Response({"msg":"Task Marked as Completed"},status=HTTP_200_OK)



        
        
# class MarkTaskCompleted_Old(APIView):

#     def put(self, request, format=None):
#         data = request.data
#         user = request.user
#         if user.is_anonymous:
#             print("<------------Incoming Request data--------------->", data)
#             booking_id = data['booking_id']
#             NewBookingObj = NewBookingModel.objects.get(booking_id__exact=booking_id)
#             print("<--------------Booking Object fetched--------------->", NewBookingObj)
#             NewBookingObj.task_status = 'Completed'
#             NewBookingObj.booking_completed = True
#             NewBookingObj.save()
            
            
#             Schedule_object = NewBookingObj.service_slot_id
#             try:
#                 if Schedule_object.service_capacity == 0:
#                     Schedule_object.service_capacity = 1
#                     Schedule_object.save()
                
#                 else:
#                     service_capacity.service_capacity = 1
#                     Schedule_object.save()
#             except:
#                 pass
                
                
#             print("<------------After Saving Task Status--------------->", NewBookingObj.task_status)
#             print("<------------After Saving Completed Flasg---------->", NewBookingObj.booking_completed)
#             return Response({"msg":"Task Marked as Completed"}, status=HTTP_200_OK)
#         else:
#             UOI_Object = UserOtherInfo.objects.get(user=user)
#             if UOI_Object.usertype == "Provider" or UOI_Object.usertype == "provider":
                
#                 print("<------------Incoming Request data--------------->", data)
#                 booking_id = data['booking_id']
#                 NewBookingObj = NewBookingModel.objects.get(booking_id__exact=booking_id)
#                 print("<--------------Booking Object fetched--------------->", NewBookingObj)
# #                 NewBookingObj.task_status = 'Completed'
#                 NewBookingObj.booking_marked_completed_by_provider = True
# #                 NewBookingObj.booking_completed = True
#                 fcm_receiver_user = NewBookingObj.requestor_id
#                 print("<-----------------Mark as completed FCM Receiver User--------------------------->", fcm_receiver_user)
                
# #                 fcm_receiver_user_object = UserOtherInfo.objects.get(id=fcm_receiever_user)
#                 fcm_receiver_token = fcm_receiver_user.fcm_token
#                 print("<-----------------------FCM Receiver Token---------------------------------------->", fcm_receiver_token)

#                 message_body = "Provider has marked the appointment as complete"
#                 try:
#                     send_to_one(fcm_receiver_token, message_body, "Appointment Complete")
#                 except:
#                     pass
# #                 NewBookingObj.booking_completed = True
#                 NewBookingObj.save()
                
#                 UserObject = UOI_Object.user
#                 Notif_To_UOI_Object = NewBookingObj.requestor_id
#                 Notif_user_Object = Notif_To_UOI_Object.user
                
#                 InAppBookingNotificationsObject  =  InAppBookingNotifications(
#                     from_user_id = UOI_Object,
#                     from_user_name = UserObject.get_full_name(),
#                     to_user_id = NewBookingObj.requestor_id,
#                     to_user_name= Notif_user_Object.get_full_name(),
#                     notification_type = "Booking Completed",
#                     notification_title = "Service Request has been marked completed by provider. Please mark the corresponding booking as completed on your end to initiate payment.",

#                     service_name   = NewBookingObj.service_name,
#                     notification_time = timezone.now(),
#                     notification_date = timezone.now(),
#                     to_user_usertype    = REQUESTOR_STRING
#                     )
#                 InAppBookingNotificationsObject.save()
#                 print("<------------After Saving Task Status--------------->", NewBookingObj.task_status)
#                 print("<------------After Saving Completed Flasg---------->", NewBookingObj.booking_completed)
#                 return Response({"msg":"Task Marked as Completed"}, status=HTTP_200_OK)
            
#             else:
#                 if RANDOM_TRANSACTION_FAIL == True:
#                     num = random.randint(0,1)
#                 else:
#                     num = 1
                
                
#                 if num == 0:
#                     return Response({"msg":"Transaction Failed. Any amount debited will be credited back within 3 working days.", "status":"TRANS_FAILED"}, status=HTTP_400_BAD_REQUEST)    
#                 else:
#                     print("<------------Incoming Request data--------------->", data)
#                     booking_id = data['booking_id']
#                     NewBookingObj = NewBookingModel.objects.get(booking_id__exact=booking_id)
#                     print("<--------------Booking Object fetched--------------->", NewBookingObj)
#     #                 NewBookingObj.task_status = 'Completed'
#                     NewBookingObj.booking_marked_completed_by_requestor = True
#                     NewBookingObj.booking_marked_completed_by_provider = True
#                     NewBookingObj.booking_completed = True
#                     NewBookingObj.save()
#                     UOI_Object = NewBookingObj.provider_id
                    
#                     UserObject = UOI_Object.user
#                     Notif_To_UOI_Object = NewBookingObj.provider_id
#                     Notif_user_Object = Notif_To_UOI_Object.user
#                     fcm_receiver_token = Notif_To_UOI_Object.fcm_token
#                     message_body = "Requestor has marked the appointment as complete and has initiated the payment."
#                     try:
#                         send_to_one(fcm_receiver_token, message_body, "Appointment Complete")
#                     except:
#                         pass
#                     InAppBookingNotificationsObject  =  InAppBookingNotifications(
#                         from_user_id = UOI_Object,
#                         from_user_name = UserObject.get_full_name(),
#                         to_user_id = NewBookingObj.provider_id,
#                         to_user_name= Notif_user_Object.get_full_name(),
#                         notification_type = "Booking Completed",
#                         service_name = NewBookingObj.service_name,
#                         notification_title = "Your Booking has been marked completed by service requestor and payment is complete.",
#                         notification_time = timezone.now(),
#                         notification_date = timezone.now(),
#                         to_user_usertype    = PROVIDER_STRING
#                         )
#                     InAppBookingNotificationsObject.save()

#                     print("<-------UOI Object Fethed-------------------->",UOI_Object)
                    
#                     completed_tasks =  UOI_Object.completed_tasks
#                     if completed_tasks == 0 or completed_tasks == "" or completed_tasks == None:
#                         UOI_Object.completed_tasks =  1
#                         UOI_Object.save()
#                     else:
#                         UOI_Object.completed_tasks = completed_tasks + 1
#                         UOI_Object.save()
                    
#                     try:
                        
#                         LivePaymentObject = LivePayments.objects.get(booking_ID__exact=booking_id)
                        
#                         live_payment_card = LivePaymentObject.payment_card
#                         live_payment_method = LivePaymentObject.payment_method
#                         live_payment_request_date = LivePaymentObject.payment_request_date
#                         live_payment_request_time = LivePaymentObject.payment_request_time
#                         live_service = LivePaymentObject.service
#                         live_payment_from = LivePaymentObject.payment_from
#                         live_payment_to = LivePaymentObject.payment_to
#                         live_booking_ID = LivePaymentObject.booking_ID
#                         live_cash_req = LivePaymentObject.cash_paid_by_requestor
#                         live_cash_pro = LivePaymentObject.cash_collected_by_provider
#                         live_service_charges = LivePaymentObject.service_charges
#                         live_admin_charges = LivePaymentObject.admin_charges
#                         total_amount  = live_admin_charges + live_service_charges

                        
                        
#                         SettledPaymentObject = SettledPayments(
#                             payment_card=live_payment_card,
#                             payment_method=live_payment_method,
#                             payment_request_date=live_payment_request_date,
#                             payment_request_time=live_payment_request_time,
#                             payment_settle_date=timezone.now(),
#                             payment_settle_time=timezone.now(),
#                             service=live_service,
#                             payment_from=live_payment_from,
#                             payment_to=live_payment_to,
#                             booking_ID=live_booking_ID,
#                             cash_paid_by_requestor = live_cash_req,
#                             cash_collected_by_provider = live_cash_pro,
#                             service_charges = live_service_charges,
#                             admin_charges = live_admin_charges,
#                             total_amount_paid = total_amount
                            
#                             )
#                         SettledPaymentObject.save()
#                         LivePaymentObject.delete()
#         #                 send_to_one()
#         #                 NewBookingObj.booking_completed = True
# #                         NewBookingObj.save()
#         #                 send_to
#                         print("<------------After Saving Task Status--------------->", NewBookingObj.task_status)
#                         print("<------------After Saving Completed Flasg---------->", NewBookingObj.booking_completed)
#                         return Response({"msg":"Task Marked as Completed"}, status=HTTP_200_OK)
#                     except:
#                         return Response({"msg":"Task has already been marked as complete."},status=HTTP_400_BAD_REQUEST)
                    




class ViewCompletedTask(APIView):
    def get(self,request,format=None):
        user = request.user
        userotherinfoObj = UserOtherInfo.objects.get(user=user)
        print("<----------User type------------------->",userotherinfoObj.usertype)
        if (userotherinfoObj.usertype == "provider" or userotherinfoObj.usertype == "Provider"):
            NewBookingObj =  NewBookingModel.objects.filter(provider_id=userotherinfoObj). \
            filter(Q(booking_completed =  True)| Q(booking_cancelled = True)).order_by('-booking_closure_time')
            
            print("<---------------NewBooking List--------------------------->",NewBookingObj)

            serializer = ViewCompletedTaskSerializer(NewBookingObj,many=True,context={'uoi_object_id':userotherinfoObj.id}).data

            return Response(serializer,status=HTTP_200_OK)

        else:
            print("<-----------------User------------------>",user)
            print("<--------------------User ID------------->",user.id)
            allbookings = NewBookingModel.objects.all()
            for i in allbookings:
                print("<------------Requestor ID----------------->",i.requestor_id)
            print("<-----------All Booking------------------->",allbookings)
            NewBookingObjTemp = NewBookingModel.objects.filter(requestor_id = userotherinfoObj)
            print("<---------------First Level Filtering------------------------->",NewBookingObjTemp)
            NewBookingObjTemp = NewBookingModel.objects.filter(requestor_id = userotherinfoObj).filter(booking_completed =  True)
            print("<------------Filtering Booking COmpleted---------------------->",NewBookingObjTemp)
            NewBookingObjTemp = NewBookingModel.objects.filter(requestor_id = userotherinfoObj).filter(booking_cancelled = True)
            print("<-------------Filtering Booking Cancelled-------------------------->",NewBookingObjTemp)
            NewBookingObj = NewBookingModel.objects.filter(requestor_id = userotherinfoObj). \
            filter(Q(booking_completed =  True)| Q(booking_cancelled = True)).order_by('-booking_closure_time')
            serializer = ViewCompletedTaskSerializer(NewBookingObj,many=True,context={'uoi_object_id':userotherinfoObj.id}).data
            print("<----------------Serializer------------------>",serializer)
            return Response(serializer,status=HTTP_200_OK)





class MarketingCarouselAPIView(APIView):
    def get(self, request, format=None):

        obj= BannerImage.objects.all().annotate(image=F('banner_img_file'))
        if len(obj) == 0:
            obj = BannerImage.objects.all()
            serializer = MarketingCarouselSerializer(obj,many=True).data
            print("<----------------Marketing Carousle returned--------------->",serializer)
            return Response(serializer,status=HTTP_200_OK)        
        else:
            obj = BannerImage.objects.all()
            serializer = MarketingCarouselSerializer(obj,many=True).data
            print("<----------------Marketing Carousle returned--------------->",serializer)
            return Response(serializer,status=HTTP_200_OK)   




class TrendingProvidersAPIVIew(APIView,MyPaginationMixin):
    
    pagination_class = PageNumberPagination
    
    def get(self,request):
        user = request.user
        distance = 0
        
        unique_user = []

        lang = request.GET.get('lang')
        if lang != None:
            if lang in ["English","english","en"]:
                context_lang = "en"
            elif lang in ["Arabic","arabic","ar"]:
                context_lang = "ar"
        else:
            context_lang = "en"


        ANON = False

        if user.is_anonymous:
            ANON = True
        else:
            UserObject =  User.objects.get(id=user.id)
            UOI_Object = UserOtherInfo.objects.get(user=UserObject)       
            logged_in_user_lat  = UOI_Object.user_address_lat
            logged_in_user_long = UOI_Object.user_address_long
            fav_qs = Favourites.objects.filter(user=UOI_Object)
            fav_id = [x.provider.id for x in fav_qs]


        previous_days = timedelta(days=30)
        today  = timezone.now()
        last_day = today - previous_days
        print("<------------Today------------------->",today)
        print("<-------------Previous Day--------------->",previous_days)
        print("<--------------Last Day------------------->",last_day)
        NewBookingQuerySet = NewBookings.objects.filter(created__gte = last_day)
        print("<-----------------NewBookingQuerySet----------------->",NewBookingQuerySet)

        serializers = BookingListSerializer(NewBookingQuerySet,many=True).data
        frequency = dict()


        for BookingObject in serializers:
            if not BookingObject['provider_id'] in frequency:
                frequency[BookingObject['provider_id']] = 1
            else:
                frequency[BookingObject['provider_id']]+=1
            print("<------------BookingObject--------------->",BookingObject['provider_id'])
        
        sorted_frequency = sorted(frequency.items(),key=lambda x: x[1], reverse=True)
        # limit_sorted = sorted_frequency[:10]
        provider_ids = []
        for element in sorted_frequency:
            provider_ids.append(element[0])




        trendingservices = []
        for provider in provider_ids:
            UserOtherInfoObject = UserOtherInfo.objects.get(id=provider)
            UserObject = User.objects.get(id=UserOtherInfoObject.user.id)
            if ANON == False:
                if UserObject != user:
                    print("<-----------------Not Same User-------------------->")
                    try:
                        print("<--------------Inside Try Block---------------->",UserOtherInfoObject)
                        UserOtherInfoObject = UserOtherInfo.objects.get(user=UserObject)
                        serializer = TrendingServiceListSerializer(UserOtherInfoObject,context={"lang":context_lang}).data
                        print("<--------------Inside Try Block---------------->",UserOtherInfoObject)
                        if serializer['switched_to_provider'] == True:
                            print("<-------------Switched to Provider User Object---------------->",UserOtherInfoObject)
                            if len(serializer['services_offered'])>=MIN_SERVICES:
                                print("<-------------Services Offered is more than zero----------------->")
                                if ANON == False:
                                    provider_lat = Decimal(serializer['user_address_lat'])
                                    provider_long = Decimal(serializer['user_address_long'])
                                    distance = GeoPointsDistance(logged_in_user_lat,logged_in_user_long,provider_lat,provider_long)
                                    serializer['distance'] = distance
                                    
                                    if UserOtherInfoObject.id in fav_id:
                                        serializer['favourite'] = True
                                    else:
                                        serializer['favourite'] = False
                                        
                                else:
                                    serializer['distance'] = distance
                                    serializer['favourite'] = False
                                
                                print("<---------------Appending to Trending------------------->",trendingservices)
                                
                                if UserObject not in unique_user and ENABLE_UNIQUE_USER:    
                                    trendingservices.append(serializer)
                                    unique_user.append(UserObject)
                                else:
                                    trendingservices.append(serializer)
                                    
                        print("<-------------Length of Trending Service---------------->",len(trendingservices))
                    except Exception as e:
                        print("<--------------Exception trace--------------->",e)
                        pass
                else:
                    pass
            else:
                print("<--------------------------UserObject--------------------->",UserObject)
                print("<---------------Before User Other Info------------------->")
                try:
                    UserOtherInfoObject = UserOtherInfo.objects.get(user=UserObject)
    
                    print("<---------------UserType------------------->",UserOtherInfo.usertype)

                    print("<----------------Sorted Frequency-------------------->",sorted_frequency)
                    print("<--------------Serailzied Data-------------------------->",serializers)
                    print("<---------------Frequency Counter------------------------>",frequency)
                    print("<-------------------------------------userOtherInfoObject------------------->",UserOtherInfoObject)
                    serializer = TrendingServiceListSerializer(UserOtherInfoObject,context={"lang":context_lang}).data

                    if serializer['switched_to_provider'] == True:

                        if len(serializer['services_offered'])>=MIN_SERVICES:
                            if ANON == False:
                                provider_lat = Decimal(serializer['user_address_lat'])
                                provider_long = Decimal(serializer['user_address_long'])
                                print("<----------------Provide Dlat----------------->",provider_lat)
                                print("<-----------------Provider long------------------->",provider_long)
                                print("<----------------Provider Lat type------------------>",type(provider_lat))
                                print("<----------------Provider Long Type------------------>",type(provider_long))
                                distance = GeoPointsDistance(logged_in_user_lat,logged_in_user_long,provider_lat,provider_long)
                                print("<------------------COMPUTED DISTANCE---------------------->",distance)
                                serializer['distance'] = distance
                                if UserOtherInfoObject.id in fav_id:
                                    serializer['favourite'] = True
                                else:
                                    serializer['favourite'] = False
                            else:
                                serializer['distance'] = distance
                                serializer['favourite'] = False
                                
                            if UserObject not in unique_user and ENABLE_UNIQUE_USER:
                                trendingservices.append(serializer)
                                unique_user.append(UserObject)
                            else:
                                trendingservices.append(serializer)                                

                    print("<-------------Length of Trending Service---------------->",len(trendingservices))
                except:
                    pass                
        
  
        if len(trendingservices) == 0:

            previous_days = timedelta(days=PREVIOUS_DAYS)
            today  = timezone.now()
            last_day = today - previous_days
            print("<------------Today------------------->",today)
            print("<-------------Previous Day--------------->",previous_days)
            print("<--------------Last Day------------------->",last_day)
            if ANON == True:
                MostRecentQuerySet = UserOtherInfo.objects.filter(created__gte = last_day)
            else:
                MostRecentQuerySet = UserOtherInfo.objects.filter(created__gte = last_day).exclude(user=user)
            print("<-----------------MostRecentQuerySet--------------------->",MostRecentQuerySet)
            UserObjectSerialized      = UserOtherInfoSerializer(MostRecentQuerySet,many=True).data
            print("<-------------------UserObjectQS-------------------------->",UserObjectSerialized)
            
            created_dict = dict()
            for UserObject in UserObjectSerialized:
                if not UserObject['user'] in created_dict:
                    created_dict[UserObject['user']] = UserObject['created']

            print("<----------Created Dict-------------->",created_dict)


            tuple_dict = [(k,v) for k,v in created_dict.items()]
            sorted_user       = sorted(tuple_dict,key=lambda x:x[1],reverse = True)
            user_ids = []
            for element in sorted_user:
                user_ids.append(element[0])

            print("<----------Sorteduser------------>",tuple_dict)
            print("<------------Tuple---------------->",sorted_user)

            most_recent = []

            for user in user_ids:
                try:
                    UserObject = User.objects.get(id=user)
                    try:
                        UserOtherInfoObject = UserOtherInfo.objects.get(user=UserObject)
                        
                        print("<---------------UserType------------------->",UserOtherInfoObject)
                        serializer = MostRecentSerializer(UserOtherInfoObject,context={"lang":context_lang}).data
                        print("<---------------UserType------------------->",serializer['usertype'])
                        if serializer['switched_to_provider'] == True:
                            if ANON == False:
                                provider_lat = Decimal(serializer['user_address_lat'])
                                provider_long = Decimal(serializer['user_address_long'])
                                print("<----------------Provide Dlat----------------->",provider_lat)
                                print("<-----------------Provider long------------------->",provider_long)
                                print("<----------------Provider Lat type------------------>",type(provider_lat))
                                print("<----------------Provider Long Type------------------>",type(provider_long))
                                distance = GeoPointsDistance(logged_in_user_lat,logged_in_user_long,provider_lat,provider_long)
                                print("<------------------COMPUTED DISTANCE---------------------->",distance)
                                serializer['distance'] = distance
                                
                                if UserOtherInfoObject.id in fav_id:
                                    serializer['favourite'] = True
                                else:
                                    serializer['favourite'] = False
                                
                            else:
                                serializer['distance'] = distance
                                serializer['favourite'] = False
                            
                            if UserObject not in unique_user and ENABLE_UNIQUE_USER:
                                most_recent.append(serializer)
                                unique_user.append(UserObject)
                            else:
                                most_recent.append(serializer)                                
                                
                    except UserOtherInfo.DoesNotExist:
                        pass
                except User.DoesNotExist:
                    pass
            print("<---------------Printing Most Recent Before Pagination---------->",most_recent)

            if PAGINATION == True:
                page = self.paginate_queryset(most_recent)
                return self.get_paginated_response(page)
            else:
                return Response(most_recent,status=HTTP_200_OK)

        else:
            print("<------------Printing Trending Before Pagination--------------->",trendingservices)

            
            if PAGINATION == True:
                page = self.paginate_queryset(trendingservices)
                return self.get_paginated_response(page)
            else:
                return Response(trendingservices ,status=HTTP_200_OK)



class FeaturedProviders(APIView,MyPaginationMixin):
    
    pagination_class = PageNumberPagination
    
    def get(self,request):
        
        unique_user = []
        start_time = datetime.now()
        print("<--------------------------Processing Start Time------------------>",start_time)
        user = request.user

        distance = 0
        
        lang = request.GET.get('lang')

        if lang != None:
            if lang in ["English","english","en"]:
                context_lang = "en"
            elif lang in ["Arabic","arabic","ar"]:
                context_lang = "ar"
        else:
            context_lang = "en"



        ANON = False

        if user.is_anonymous:

            ANON = True
        else:

            UserObject =  User.objects.get(id=user.id)
            UOI_Object = UserOtherInfo.objects.get(user=UserObject)
            logged_in_user_lat  = UOI_Object.user_address_lat
            logged_in_user_long = UOI_Object.user_address_long

            favqs = Favourites.objects.filter(user=UOI_Object)
            fav_id = [x.provider.id for x in favqs]


        if ANON == True:
            FeaturedProviderQuerySet    = FeaturedServiceProviders.objects.all()
        else:
            FeaturedProviderQuerySet    = FeaturedServiceProviders.objects.all().exclude(provider=user)
            
        if len(FeaturedProviderQuerySet) == 0:

            previous_days = timedelta(days=PREVIOUS_DAYS)
            today  = timezone.now()
            last_day = today - previous_days

            if ANON == True:
                MostRecentQuerySet = UserOtherInfo.objects.filter(created__gte = last_day)
            else:
                MostRecentQuerySet = UserOtherInfo.objects.filter(created__gte = last_day).exclude(user=user)

            UserObjectSerialized      = UserOtherInfoSerializer(MostRecentQuerySet,many=True).data

            
            created_dict = dict()
            for UserObject in UserObjectSerialized:
                if not UserObject['user'] in created_dict:
                    created_dict[UserObject['user']] = UserObject['created']


            tuple_dict = [(k,v) for k,v in created_dict.items()]
            sorted_user       = sorted(tuple_dict,key=lambda x:x[1],reverse = True)

            print("<----------------Sorted USr list-------------->",sorted_user)
            user_ids = []
            for element in sorted_user:
                user_ids.append(element[0])


            most_recent = []

            for user in user_ids:
                try:
                    UserObject = User.objects.get(id=user)
                    try:
                        UserOtherInfoObject = UserOtherInfo.objects.get(user=UserObject)
                        serializer = MostRecentSerializer(UserOtherInfoObject,context={"lang":context_lang}).data

                        if serializer['switched_to_provider'] == True:
                            if len(serializer['services_offered'])>=MIN_SERVICES:
                                if ANON == False:
                                    provider_lat = Decimal(serializer['user_address_lat'])
                                    provider_long = Decimal(serializer['user_address_long'])

                                    distance = GeoPointsDistance(logged_in_user_lat,logged_in_user_long,provider_lat,provider_long)
                                    serializer['distance'] = distance
                                    
                                    if UserOtherInfoObject.id in fav_id:
                                        serializer['favourite'] = True
                                    else:
                                        serializer['favourite'] = False
                                    
                                else:
                                    serializer['distance'] = distance
                                    serializer['favourite'] = False
                                
                                if ANON==False and UserObject not in unique_user and ENABLE_UNIQUE_USER:
                                    most_recent.append(serializer)
                                    unique_user.append(UserObject)
                                else:
                                    most_recent.append(serializer)                                    
                                    
                    except UserOtherInfo.DoesNotExist:
                        pass
                except User.DoesNotExist:
                    pass
            if PAGINATION == True:
                page = self.paginate_queryset(most_recent)
                end_time = datetime.now()
                print("<-------------------------Processing End Time----------------------->",end_time)
                print("<--------------------------Time Difference-------------------------->",end_time-start_time)
                return self.get_paginated_response(page)
            else:
                return Response(most_recent,status=HTTP_200_OK)

        else:

            featured = []
            for Object in FeaturedProviderQuerySet:

                try:
                    UserOtherInfoObject     = UserOtherInfo.objects.get(user=Object.provider)
                    serializer              = FeaturedSerializer(UserOtherInfoObject,context={"lang":context_lang}).data
                    if serializer['switched_to_provider'] == True:
                        if len(serializer['services_offered'])>=MIN_SERVICES:
                            if ANON == False:
                                provider_lat = Decimal(serializer['user_address_lat'])
                                provider_long = Decimal(serializer['user_address_long'])
                                distance = GeoPointsDistance(logged_in_user_lat,logged_in_user_long,provider_lat,provider_long)
                                serializer['distance'] = distance
                                
                                if UserOtherInfoObject.id in fav_id:
                                    serializer['favourite'] = True
                                else:
                                    serializer['favourite'] = False
                                    
                                
                            else:
                                serializer['distance'] = distance
                                serializer['favourite'] = False
                                
                            if ANON== False and UserObject not in unique_user and ENABLE_UNIQUE_USER:
                                featured.append(serializer)
                                unique_user.append(UserObject)
                            else:
                                featured.append(serializer)                                
                                
                except UserOtherInfo.DoesNotExist:
                    pass

            if PAGINATION == True:
                page = self.paginate_queryset(featured)
                end_time = datetime.now()
                print("<-------------------------Processing End Time----------------------->",end_time)
                print("<--------------------------Time Difference-------------------------->",end_time-start_time)
                return self.get_paginated_response(page)
            else:
                return Response(featured,status=HTTP_200_OK)



class MostRecentProviders(APIView,MyPaginationMixin):
    pagination_class = PageNumberPagination

    def get(self,request):
        
        unique_user = []
        
        user = request.user
        distance = 0
        
        lang = request.GET.get('lang')

        if lang != None:
            if lang in ["English","english","en"]:
                context_lang = "en"
            elif lang in ["Arabic","arabic","ar"]:
                context_lang = "ar"
        else:
            context_lang = "en"

        ANON = False

        if user.is_anonymous:
            ANON = True
        else:
            UserObject =  User.objects.get(id=user.id)
            UOI_Object = UserOtherInfo.objects.get(user=UserObject)       
            logged_in_user_lat  = UOI_Object.user_address_lat
            logged_in_user_long = UOI_Object.user_address_long
            favqs = Favourites.objects.filter(user=UOI_Object)
            fav_id = [x.provider.id for x in favqs]

        previous_days = timedelta(days=PREVIOUS_DAYS)
        today  = timezone.now()
        last_day = today - previous_days
        print("<------------Today------------------->",today)
        print("<-------------Previous Day--------------->",previous_days)
        print("<--------------Last Day------------------->",last_day)
        if ANON == True:
            MostRecentQuerySet = UserOtherInfo.objects.filter(created__gte = last_day)
        else:
            MostRecentQuerySet = UserOtherInfo.objects.filter(created__gte = last_day).exclude(user=user)
        print("<-----------------MostRecentQuerySet--------------------->",MostRecentQuerySet)
        UserObjectSerialized      = UserOtherInfoSerializer(MostRecentQuerySet,many=True).data
        print("<-------------------UserObjectQS-------------------------->",UserObjectSerialized)
        
        created_dict = dict()
        for UserObject in UserObjectSerialized:
            if not UserObject['user'] in created_dict:
                created_dict[UserObject['user']] = UserObject['created']

        print("<----------Created Dict-------------->",created_dict)

        tuple_dict = [(k,v) for k,v in created_dict.items()]
        sorted_user       = sorted(tuple_dict,key=lambda x:x[1],reverse = True)
        user_ids = []
        for element in sorted_user:
            user_ids.append(element[0])

        print("<----------Sorteduser------------>",tuple_dict)
        print("<------------Tuple---------------->",sorted_user)

        most_recent = []

        for user in user_ids:
            try:
                UserObject = User.objects.get(id=user)
                try:
                    UserOtherInfoObject = UserOtherInfo.objects.get(user=UserObject)
                    
                    print("<---------------UserType------------------->",UserOtherInfoObject)
                    serializer = MostRecentSerializer(UserOtherInfoObject,context={"lang":context_lang}).data
                    print("<---------------UserType------------------->",serializer['usertype'])
                    if serializer['switched_to_provider'] == True:
                        if len(serializer['services_offered']) >= MIN_SERVICES:
                            if ANON == False:
                                provider_lat = Decimal(serializer['user_address_lat'])
                                provider_long = Decimal(serializer['user_address_long'])
                                print("<----------------Provide Dlat----------------->",provider_lat)
                                print("<-----------------Provider long------------------->",provider_long)
                                print("<----------------Provider Lat type------------------>",type(provider_lat))
                                print("<----------------Provider Long Type------------------>",type(provider_long))
                                distance = GeoPointsDistance(logged_in_user_lat,logged_in_user_long,provider_lat,provider_long)
                                print("<------------------COMPUTED DISTANCE---------------------->",distance)
                                serializer['distance'] = distance
                                
                                if UserOtherInfoObject.id in fav_id:
                                    serializer['favourite'] = True
                                else:
                                    serializer['favourite'] = False
                                
                            else:
                                serializer['distance'] = distance
                                serializer['favorite'] = False
                            
                            if UserObject not in unique_user and ENABLE_UNIQUE_USER:
                                most_recent.append(serializer)
                                unique_user.append(UserObject)
                            else:
                                most_recent.append(serializer)                                
                                
                except UserOtherInfo.DoesNotExist:
                    pass
            except User.DoesNotExist:
                pass
            
        print("<----------------MOST RECENT PROVIDERS------------------->",most_recent)
        
        if PAGINATION == True:
            page = self.paginate_queryset(most_recent)
            return self.get_paginated_response(page)

        else:
            return Response(most_recent,status=HTTP_200_OK)


class SearchProvider(APIView,MyPaginationMixin):
    
    pagination_class = PageNumberPagination
    
    def put(self,request):
        
        unique_user = []
        user = request.user
        distance = 0

        lang = request.GET.get('lang')

        if lang != None:
            if lang in ["English","english","en"]:
                context_lang = "en"
            elif lang in ["Arabic","arabic","ar"]:
                context_lang = "ar"
        else:
            context_lang = "en"


        ANON = False

        if user.is_anonymous:
            ANON = True
        else:
            UserObject =  User.objects.get(id=user.id)
            UOI_Object = UserOtherInfo.objects.get(user=UserObject)       
            logged_in_user_lat  = UOI_Object.user_address_lat
            logged_in_user_long = UOI_Object.user_address_long



        query = request.data['query'].lower()
        
        if ANON == True:
            UserOtherInfoQuerySet = UserOtherInfo.objects.filter(switched_to_provider=True)
        else:
            UserOtherInfoQuerySet = UserOtherInfo.objects.filter(switched_to_provider=True).exclude(user=user)
        
        matching_uoi_id = []                 
        matching = []
        for UserOtherInfoObject in UserOtherInfoQuerySet:
            UserObject = User.objects.get(id=UserOtherInfoObject.user.id)
            if query in UserObject.get_full_name().lower():
                ServiceQuerySet = Service.objects.filter(user=UserOtherInfoObject.user).filter(service_langugae__exact=context_lang)
                print("<---------------ServiceQS-------------------->",ServiceQuerySet)
                if len(ServiceQuerySet) >= MIN_SERVICES:
                    if UserOtherInfoObject not in matching_uoi_id:
                        matching_uoi_id.append(UserOtherInfoObject)
                        print("<-----------------Length of QS--------------->",len(ServiceQuerySet))
                        serializer = SearchResultSerializer(UserOtherInfoObject,context={"lang":context_lang}).data
                        if ANON == False:
                            provider_lat = Decimal(serializer['user_address_lat'])
                            provider_long = Decimal(serializer['user_address_long'])
                            print("<----------------Provide Dlat----------------->",provider_lat)
                            print("<-----------------Provider long------------------->",provider_long)
                            print("<----------------Provider Lat type------------------>",type(provider_lat))
                            print("<----------------Provider Long Type------------------>",type(provider_long))
                            distance = GeoPointsDistance(logged_in_user_lat,logged_in_user_long,provider_lat,provider_long)
                            print("<------------------COMPUTED DISTANCE---------------------->",distance)
                            serializer['distance'] = distance
                        else:
                            serializer['distance'] = distance
                        
                        if UserOtherInfoObject not in unique_user and ENABLE_UNIQUE_USER:
                            matching.append(serializer)
                            unique_user.append(UserOtherInfoObject)
                        else:
                            matching.append(serializer)
                                                        
            else:
                ServiceQuerySet = Service.objects.filter(user=UserOtherInfoObject.user).filter(service_langugae__exact=context_lang)
                if len(ServiceQuerySet) >= MIN_SERVICES:
                    for serviceObject in ServiceQuerySet:
                        print("<----------------Service Name------------->",serviceObject.service_name)
                        service_name = str(serviceObject.service_name).lower()
                        found = service_name.find(query)
                        print("<-------------------Found-------------------->",found)
                        print("<---------------------Query-------------------->",query)
                        if found >= 0:
                            if UserOtherInfoObject not in matching_uoi_id:
                                matching_uoi_id.append(UserOtherInfoObject)
                                serializer = SearchResultSerializer(UserOtherInfoObject,context={"lang":context_lang}).data
                                if ANON == False:
                                    provider_lat = Decimal(serializer['user_address_lat'])
                                    provider_long = Decimal(serializer['user_address_long'])
                                    print("<----------------Provide Dlat----------------->",provider_lat)
                                    print("<-----------------Provider long------------------->",provider_long)
                                    print("<----------------Provider Lat type------------------>",type(provider_lat))
                                    print("<----------------Provider Long Type------------------>",type(provider_long))
                                    distance = GeoPointsDistance(logged_in_user_lat,logged_in_user_long,provider_lat,provider_long)
                                    print("<------------------COMPUTED DISTANCE---------------------->",distance)
                                    serializer['distance'] = distance
                                else:
                                    serializer['distance'] = distance
                                
                                
                                if UserOtherInfoObject not in unique_user and ENABLE_UNIQUE_USER:
                                    matching.append(serializer)
                                    unique_user.append(UserOtherInfoObject)
                                else:
                                    matching.append(serializer)                                    
                
        
        
        print("<------------------Searching Returning Data-------------->",matching)
        if PAGINATION == True:
            page = self.paginate_queryset(matching)
            return self.get_paginated_response(page)
        else:
            return Response(matching,status=HTTP_200_OK)




class SelfServices(APIView):
    def put(self,request):
        user =  request.user
        print("<---------------Request Data----------------->",request)
        print("<--------------User SElf Service------------>",user)
        try:
            UserOtherInfoObject = UserOtherInfo.objects.get(user=user)
            ServiceSerialized = SelfServiceSerializer(UserOtherInfoObject).data
            print("<==================Returning Data Self Service=====================>",ServiceSerialized)
            return Response(ServiceSerialized,status=HTTP_200_OK)
        except TypeError:
            return Response({"msg":"You need to Login First"},status=HTTP_400_BAD_REQUEST)

class MyProfile(APIView):
    def put(self,request):
        try:
            user = request.user
            UserOtherInfoObject     = UserOtherInfo.objects.get(user=user)
            MyProfileSerialized     = UserOtherInfoSerializer(UserOtherInfoObject).data
            print("<-----------Returning Data My Profile----------------->",MyProfileSerialized)
            return Response(MyProfileSerialized,status=HTTP_200_OK)
        except:
            return Response({"msg":"User Does not Exist"},status=HTTP_400_BAD_REQUEST)



class SortByPricing(APIView,MyPaginationMixin):

    pagination_class = PageNumberPagination

    def put(self,request):


        lang = request.GET.get('lang')

        if lang != None:
            if lang in ["English","english","en"]:
                context_lang = "en"
            elif lang in ["Arabic","arabic","ar"]:
                context_lang = "ar"
        else:
            context_lang = "en"
        
        print("<-----------Lang retiureved from request------------->",context_lang)


        order = request.data['order']
        
        service_ids_from_session = request.session['filtered_service_ids']
        

        final_service_list = []
        for service in service_ids_from_session:
            service_qs = Service.objects.get(id=service)
            final_service_list.append(service_qs)

        
        print("<---------------------Final Service List------------>",final_service_list)
        price_tuple = []
        
        for service in final_service_list:
            price_tuple.append((service.id,service.service_pricing))
        
        print("<-----------------Unsorted Price TUple-----------------?",price_tuple)
        
        if order == "ASC":
            sorted_list = sorted(price_tuple,key=itemgetter(1))
        elif order == "DES":
            sorted_list = sorted(price_tuple,key=itemgetter(1),reverse=True)
        else:
            return Response({"msg":"Invalid Request Body. Should contain either ASC for Ascending order or DES for Descending order."},status=HTTP_400_BAD_REQUEST)
        
            
        
        
        
        final_qs = []
        for price in sorted_list:
            serviceobj_id = price[0]
            serviceobject = Service.objects.get(id =serviceobj_id)
            final_qs.append(serviceobject)
        
        
        print("<--------------Final QS-------------------->",final_qs)

        
        final_service_provider_ids = []
        for serviceobj in final_qs:
            ServiceProvider = serviceobj.user
            ServiceProvider_uoi = UserOtherInfo.objects.get(user=ServiceProvider)
            
            if ServiceProvider_uoi not in final_service_provider_ids:
                final_service_provider_ids.append(ServiceProvider_uoi)


        print("<-------------------Final Service Provider ID---------------->",final_service_provider_ids)
        
        final_serialized = []
        for provider in final_service_provider_ids:
            serializer = FilteredProviderSerializer(provider,context={"lang":context_lang}).data
            final_serialized.append(serializer)

        if  PAGINATION == True:
            page = self.paginate_queryset(final_serialized)
            return self.get_paginated_response(page)
        else:
            return Response(final_serialized,status=HTTP_200_OK)
      
        



class SortByRating(APIView,MyPaginationMixin):

    pagination_class = PageNumberPagination

    def put(self,request):

        lang = request.GET.get('lang')

        if lang != None:
            if lang in ["English","english","en"]:
                context_lang = "en"
            elif lang in ["Arabic","arabic","ar"]:
                context_lang = "ar"
        else:
            context_lang = "en"


        order = request.data['order']
        
        filtered_providers = request.session['filtered_provider_ids']
        print("<-----------------Retreived Filtered PRovider IDS from session----------->",filtered_providers)
        
        
        uoi_objects = []
        
        for provider in filtered_providers:
            uoi_qs = UserOtherInfo.objects.get(id=provider)
            uoi_objects.append(uoi_qs)
            
            
        print("<-----------------UOi Object List------------------->",uoi_objects)        
        
        rating =[]
        
        for provider_obj in uoi_objects:
            rating.append((provider_obj.id,provider_obj.avg_rating)) 
               
        
        print("<--------------Unsorted Rating------------------>",rating)

        if order == "ASC":
            sorted_list = sorted(rating,key=itemgetter(1))
        elif order == "DES":
            sorted_list = sorted(rating,key=itemgetter(1),reverse=True)
        else:
            return Response({"msg":"Invalid Request Body. Should contain either ASC for Ascending order or DES for Descending order."},status=HTTP_400_BAD_REQUEST)            

        
        print("<-------------------Sorted Rating----------------->",rating)


        final_list = []
        for user in sorted_list:
            uoi_object_id = user[0]
            UoiObject = UserOtherInfo.objects.get(id=uoi_object_id)
            serializer = FilteredProviderSerializer(UoiObject,context={"lang":context_lang}).data
            final_list.append(serializer)
        
        
        print(",--------------_Final List--------------?",final_list)        
        



        if  PAGINATION == True:
            page = self.paginate_queryset(final_list)
            return self.get_paginated_response(page)
        else:
            return Response(final_serialized,status=HTTP_200_OK)



class SortByRatingTemp(APIView):
    def put(self,request):
        order = request.data['order']
        if(order == "ASC"):
            queryset = Service.objects.all().order_by('avg_rating')
        elif(order == "DES"):
            queryset = Service.objects.all().order_by('-avg_rating')
        else:
            return Response({"msg":"Invalid Request Body. Should contain either ASC for Ascending order or DES for Descending order."},status=HTTP_400_BAD_REQUEST)
        service_ids = []
        for services in queryset:
            service_ids.append(services.id)
        all_services = []

        for serviceid in service_ids:
            ServiceObj = Service.objects.get(id=serviceid)
            print("<------------------Service ID------------->",serviceid)
            Serializer = AllServicesSerializer(ServiceObj).data
            Serializer['service_ID'] = serviceid
            all_services.append(Serializer)

        # serializer = AllServicesSerializerTemp(user).data
        return Response(all_services ,status=HTTP_200_OK)





def GeoPointsDistance(lat1,lon1,lat2,lon2):
    # lat1, lon1 = origin
    # lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    
    rounded_value = round(d,2)
    return rounded_value


class SortByDistance(APIView,MyPaginationMixin):

    pagination_class = PageNumberPagination

    def put(self, request):

        lang = request.GET.get('lang')

        if lang != None:
            if lang in ["English","english","en"]:
                context_lang = "en"
            elif lang in ["Arabic","arabic","ar"]:
                context_lang = "ar"
        else:
            context_lang = "en"

        order = request.data['order']
        user = request.user
        UserObject = UserOtherInfo.objects.get(user=user)
        SelfLat = UserObject.user_address_lat
        SelfLong = UserObject.user_address_long
        
        
        filtered_providers = request.session['filtered_provider_ids']        
        print("<-----------------Retreived Filtered PRovider IDS from session----------->",filtered_providers)
        
        final_qs = UserOtherInfo.objects.none()
        
        uoi_objects = []
        
        for provider in filtered_providers:
            uoi_qs = UserOtherInfo.objects.get(id=provider)
            uoi_objects.append(uoi_qs)        
                
        print("<-----------------UOi Object List------------------->",uoi_objects)
        
        distance_list = []

        for uoi in uoi_objects:
            UserOtherInfoObject = uoi
            print("<-----------------------Sort By Distance UserOtherInfoObject---------------->",UserOtherInfoObject)
            ProviderLat = UserOtherInfoObject.user_address_lat
            ProviderLong = UserOtherInfoObject.user_address_long
            distance = GeoPointsDistance(SelfLat,SelfLong,ProviderLat,ProviderLong)
            distance_list.append((uoi.id,distance))
        
        
        print("<------------------Unsorted List Distance----------------->",distance_list)
        
        if order == "ASC":
            sorted_distance = sorted(distance_list,key=itemgetter(1))
        elif order == "DES":
            sorted_distance = sorted(distance_list,key=itemgetter(1),reverse=True)
            
        
        print("<------------Sorted List Distance------------------------>",distance_list)



        final_list = []
        for user in sorted_distance:
            uoi_object_id = user[0]
            UoiObject = UserOtherInfo.objects.get(id=uoi_object_id)
            serializer = FilteredProviderSerializer(UoiObject,context={"lang":context_lang}).data
            final_list.append(serializer)

        print(",--------------_Final List--------------?",final_list)        
        



        if  PAGINATION == True:
            page = self.paginate_queryset(final_list)
            return self.get_paginated_response(page)
        else:
            return Response(final_serialized,status=HTTP_200_OK)





class SortByResponseTime(APIView,MyPaginationMixin):
    pagination_class = PageNumberPagination
    def put(self,request):

        lang = request.GET.get('lang')

        if lang != None:
            if lang in ["English","english","en"]:
                context_lang = "en"
            elif lang in ["Arabic","arabic","ar"]:
                context_lang = "ar"
        else:
            context_lang = "en"


        order = request.data['order']
        
        filtered_providers = request.session['filtered_provider_ids']
        print("<-----------------Retreived Filtered PRovider IDS from session----------->",filtered_providers)
        
        final_qs = UserOtherInfo.objects.none()
        
        uoi_objects = []
        
        for provider in filtered_providers:
            uoi_qs = UserOtherInfo.objects.get(id=provider)
            uoi_objects.append(uoi_qs)
            
            
        print("<-----------------UOi Object List------------------->",uoi_objects)
        
        response_time =[]
        
        for provider_obj in uoi_objects:
            response_time.append((provider_obj.id,provider_obj.response_within))
        
        
        print("<----------------Tuple List Repsonse time------------->",response_time)
        
        
        
        if order == "ASC":
            sorted_list = sorted(response_time,key=itemgetter(1))
        elif order == "DES":
            sorted_list = sorted(response_time,key=itemgetter(1),reverse=True)
        else:
            return Response({"msg":"Invalid Request Body. Should contain either ASC for Ascending order or DES for Descending order."},status=HTTP_400_BAD_REQUEST)            


        print("<----------------SOrted Response Time----------------->",response_time)
        
        final_list = []
        for user in sorted_list:
            uoi_object_id = user[0]
            UoiObject = UserOtherInfo.objects.get(id=uoi_object_id)
            serializer = FilteredProviderSerializer(UoiObject,context={"lang":context_lang}).data
            final_list.append(serializer)
        
        
        print(",--------------_Final List--------------?",final_list)
            
    

        if  PAGINATION == True:
            page = self.paginate_queryset(final_list)
            return self.get_paginated_response(page)
        else:
            return Response(final_serialized,status=HTTP_200_OK)
        
        

class ViewAllNotifications(APIView):
    def post(self, request):
        user = request.user
        print("<------------------Incoming Request User ID---------------->",user.id)
        UserOtherInfoObject = UserOtherInfo.objects.get(user=user)
        usertype = UserOtherInfoObject.usertype
        
        if usertype == "provider" or usertype == "Provider":
             
            print("<------------------User Other Info ID------------------------->",UserOtherInfoObject.id)
            MyNotifications =   InAppBookingNotifications.objects.filter(to_user_id = UserOtherInfoObject.id).filter(to_user_usertype=PROVIDER_STRING).order_by('-notification_created')
        else:
            MyNotifications =   InAppBookingNotifications.objects.filter(to_user_id = UserOtherInfoObject.id).filter(to_user_usertype=REQUESTOR_STRING).order_by('-notification_created')
        
        read_notifs = len(MyNotifications.filter(notification_read=False))
        print("<------------------Unread Count-------------------------->",read_notifs)
        serializer =  NotificationSerializer(MyNotifications,many=True).data
        return Response(serializer,status=HTTP_200_OK)


class ReadAllNotifications(APIView):
    def get(self,request):
        user = request.user
        try:
            UserOtherInfoObject = UserOtherInfo.objects.get(user=user)
            usertype = UserOtherInfoObject.usertype
            if usertype == "provider" or usertype == "Provider":
                NotifQS = InAppBookingNotifications.objects.filter(to_user_id=UserOtherInfoObject).filter(to_user_usertype=PROVIDER_STRING)
            else:
                NotifQS = InAppBookingNotifications.objects.filter(to_user_id=UserOtherInfoObject).filter(to_user_usertype=REQUESTOR_STRING)
            
            for notif in NotifQS:
                notif.notification_read = True
                notif.save()
            
            return Response({"msg":"Notifications marked as read"},status=HTTP_200_OK)
        except Exception as e:
            print("<----------An Exception occured-------------->",e)
            return Response({"msg":"An error occured"},status=HTTP_400_BAD_REQUEST)


class MarkNotificationAsRead(APIView):
    def put(self,request):
        user = request.user
        data = request.data
        print("<-----------------Mark Notification as Read Incoming Data-------------->",data)
        notification_id = data['notification_id']
        try:
            InAppBookingNotifications.objects.get(id=notification_id).delete()
        except:
            pass
        
        return Response({"msg":"Notification marked as read"},status=HTTP_200_OK)



class ClearAllNotification(APIView):
    def put(self,request):
        user = request.user
        UserOtherInfoObject = UserOtherInfo.objects.get(user=user)
        usertype = UserOtherInfoObject.usertype
        if usertype == "provider" or usertype == "Provider":
            InAppBookingNotifications.objects.filter(to_user_id=UserOtherInfoObject).filter(to_user_usertype=PROVIDER_STRING).delete()
        else:
            InAppBookingNotifications.objects.filter(to_user_id=UserOtherInfoObject).filter(to_user_usertype=REQUESTOR_STRING).delete()
        return Response({"msg":"All Notifications Cleared"},status=HTTP_200_OK)




class MarkProviderAsFavourite(APIView):
    def put(self,request):
        user = request.user
        UserOtherInfoObject = UserOtherInfo.objects.get(user=user)
        data =  request.data
        provider_id = data['provider_id']
        print("<------------Incoming Data------------->",data)
        ProviderUserObject = User.objects.get(id=provider_id)
        ProviderUserOtherInfoObject = UserOtherInfo.objects.get(user=ProviderUserObject)
        
        try:
            Fav = Favourites.objects.filter(user = UserOtherInfoObject).filter(provider = ProviderUserOtherInfoObject)
            if len(Fav) > 0:
                for obj in Fav:
                    print("<---------------Deleting Object----------->",obj)
                    obj.delete()
                
                return Response({"msg":"Provider unmarked as Favourite"},status=HTTP_200_OK)
            else:
                Fav = Favourites(user = UserOtherInfoObject, provider = ProviderUserOtherInfoObject)
                Fav.save()
                print("<-----------------Marked as fav---------------------->")
                return Response({"msg":"Provider Marked as Favourite"},status=HTTP_200_OK)
        except:
            print("<========Some Error Occured--------------->")
            return Response({"msg":"Some error occured"},status=HTTP_400_BAD_REQUEST) 



class TestFeatured(APIView):
    def get(self,request):
        serviceqs =  Service.objects.all()
        featuredservices = []
        for service in serviceqs:
            serializer  = FeaturedServiceListSerializer(service).data
            print("<------------TestFeatured------------------>",serializer)
        
        return Response({"msg":"Success"},status=HTTP_200_OK)



class FilterServicesList(APIView,MyPaginationMixin):
    pagination_class = PageNumberPagination
    


    
    def put(self,request):



        lang = request.GET.get('lang')

        if lang != None:
            if lang in ["English","english","en"]:
                context_lang = "en"
            elif lang in ["Arabic","arabic","ar"]:
                context_lang = "ar"
        else:
            context_lang = "en"

        user = request.user
        if not user.is_anonymous:
            request_uoi_object = UserOtherInfo.objects.get(user=user)

        
        THRESHOLD = 0
        
        data = request.data
        print("<---------------------Incoming Data--------------->",data)
        qa_list = data['QA']
        # lang = data['current_language']
        print("<---------------------QA List--------------------->",qa_list)
        
        try:
            subcategory_id = data['subcategory_id']
            subcategory_object = SubCategory.objects.get(id=subcategory_id)
            print("<--------------Subcategory Selected================>",subcategory_object)
            masterQS = Service.objects.filter(subcategory=subcategory_object,service_langugae__exact=context_lang)

        except:
            masterQS = Service.objects.all()
        print("<---------------------Master QS------------------->",masterQS)
        
        match_score = OrderedDict()
        
        for service in masterQS:
            match_score[service.id] = 0
        
        print("<---------------------Initial Match Score--------------->",match_score)
        
        
        REMOTE = False
        

        
        for question in qa_list:
            
            if 'question_id' in question:
                question_object = QuestionFilledByAdmin.objects.get(id=question['question_id'])
                print("<------------------------Question in QA List---------------->",question)
                print("<-----------------------Question ID------------------------->",question['question_id'])
                if context_lang == "en":
                    matching = AnswerByProvider.objects.filter(question=question_object).filter(option_Selected=question['answer'])
                elif context_lang == "ar":
                    matching = AnswerByProvider.objects.filter(question=question_object).filter(option_Selected_in_arabic=question['answer'])


                question_match = []
                for service in matching:
                    question_match.append(service.service.id)
                
                for service_id in match_score:
                    if service_id in question_match:
                        match_score[service_id] = match_score[service_id] + 1
                
                print("<--------------------Before Date Time Match Score-------------------->",match_score)
            
            
            elif 'Service_date' in question:
                day_list = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
                
                service_date = question['Service_date']
                service_time = question['service_time']
                print("<-------------------Raw Date Received---------------->",service_date)
                print("<-------------------Raw Time Received---------------->",service_time)
                service_date_object = datetime.strptime(service_date,EXTERNAL_DATE_FORMAT)
                service_time_cleaned = service_time.strip()
                service_time_object = datetime.strptime(service_time_cleaned,EXTERNAL_TIME_FORMAT)
                today_object = datetime.today()
                today_weekday_number = int(datetime.strftime(today_object,"%w"))
                print("<----------------------Today Weekday Number-------------------->",today_weekday_number)
                service_weekday_number = int(datetime.strftime(service_date_object,"%w"))
                service_day_of_year = int(datetime.strftime(service_date_object,"%j"))
                print("<---------------Service Day of Year--------------->",service_day_of_year)
                print("<----------------Type of Service Day of Year-------->",type(service_day_of_year))
                
                today_day_of_year = int(datetime.strftime(today_object,"%j"))
                print("<-----------------Today Day of Year--------------->",today_day_of_year)
                print("<----------------Type of Today Day of Year-------->",type(today_day_of_year))
                
                if service_day_of_year <  today_day_of_year:
                    return Response({"msg":"You cannont select a time in the past"},status=HTTP_400_BAD_REQUEST)
                else:
                    service_week_number = int(datetime.strftime(service_date_object,"%W"))
                    print("<------------------Service Week Number------------>",service_week_number)
                    today_week_number = int(datetime.strftime(today_object,"%W"))
                    print("<---------------------Today Week Number--------------->",today_week_number)
                    
                    service_schedule_list = []
                    for service in masterQS:
                        schedule_qs = ServiceSchedule.objects.filter(service=service)
                        for schedule in schedule_qs:
                            service_schedule_list.append(schedule)
                    
                    print("<-----------------Service Schedules Retrevied------------------->",service_schedule_list)
                    
                    if service_week_number > today_week_number:
                        
                        print("<-------------------Inside Next Week Clause---------------------->")
                        
                        
                        service_weekday_number = int(datetime.strftime(service_date_object,"%w"))
                        print("<----------------------Service Weekday Number------------------>",service_weekday_number)
                        service_weekday_string = datetime.strftime(service_date_object,"%A")
                        print("<----------------------Service Weekday String------------------>",service_weekday_string)
                        today_weekday_number = int(datetime.strftime(today_object,"%w"))
                        print("<----------------------Today Weekday Number-------------------->",today_weekday_number)
                        today_weekday_string = datetime.strftime(today_object,"%A")
                        print("<-------------------Today weekday String----------------------->",today_weekday_string)
                        
                        if service_weekday_number >= today_weekday_number:
                        
                            print("<-----------------Inside Week Completed----------------->")
                            final_selected_service_ids = []
                            for service in service_schedule_list:
                                print("<-------------------------Service Open Time---------------->",service.open_time)
                                print("<-------------------------Type Service Open Time----------->",type(service.open_time))
                                print("<-------------------------Service Close Time--------------->",service.close_time)
                                print("<------------------------Type Service Close Time----------->",type(service.close_time))
                                
                                service_open_time_str = service.open_time.strftime("%H:%M")
                                service_close_time_str = service.close_time.strftime("%H:%M")

                                if service_time_cleaned >= service_open_time_str and service_time_cleaned <= service_close_time_str:
                                    final_selected_service_ids.append(service.service.id)                                    
                                
#                                     if service_time_object >= service.open_time and service_time_object <= service.close_time:
#                                         final_selected_service_ids.append(service.id)
                        
                        
                        
                        
                        else:
                            print("<-------------------Inside Partial Week----------------->")
                            
                            final_selected_service_ids = []
                            weekday_pointer = today_weekday_number+1
                            while weekday_pointer != service_weekday_number:
                                print("<---------------------------Weekday Pointer Absolute Value----------->",weekday_pointer)
#                                 weekday_pointer_object = datetime.strptime(weekday_pointer,"%w")
                                # print("<------------------Weekday Pointer Object---------------->",weekday_pointer_object)

#                                     weekday_pointer_string = datetime.strftime(weekday_pointer_object,"%A")
                                weekday_pointer_string = day_list[weekday_pointer]
                                print("<-----------------Weekday Pointer String-------------->",weekday_pointer_string)
                                
                                for service in service_schedule_list:
                                    print("<-------------------------Service Open Time---------------->",service.open_time)
                                    print("<-------------------------Type Service Open Time----------->",type(service.open_time))
                                    print("<-------------------------Service Close Time--------------->",service.close_time)
                                    print("<------------------------Type Service Close Time----------->",type(service.close_time))
                                    if service.day == weekday_pointer_string:
                        
                                        service_open_time_str = service.open_time.strftime("%H:%M")
                                        print("<---------------------------Service Open Time STR-------------->",service_open_time_str)
                                        service_close_time_str = service.close_time.strftime("%H:%M")
                                        print("<--------------------------Service Close Time STR---------------->",service_close_time_str)
                                        
                                        print("<--------------------------Service Time Cleaned------------------->",service_time_cleaned)
    
                                        if service_time_cleaned >= service_open_time_str and service_time_cleaned <= service_close_time_str:
                                            final_selected_service_ids.append(service.service.id)                                  

#                                             if service_time_object >= service.open_time and service_time_object <= service.close_time:
#                                                 final_selected_service_ids.append(service.id)
                                
                                
                                weekday_pointer = (weekday_pointer+1)%7 
                                print("<==========================Weekday Pointer Incremented----------------->",weekday_pointer)
                                                                   
                                
                            
                                                     
                    else:
                        print("<------------------Inside THis Week Clause----------------->")
                        final_selected_service_ids = []
                        weekday_pointer = today_weekday_number
                        print("<-----------------Service Weekday Number---------------------->",service_weekday_number)
                        while weekday_pointer <= service_weekday_number:
                            print("<---------------------------Weekday Pointer Absolute Value----------->",weekday_pointer)
                            weekday_pointer_object = datetime.strptime(str(weekday_pointer),"%w")
                            print("<------------------Weekday Pointer Object---------------->",weekday_pointer_object)

                            weekday_pointer_string = day_list[weekday_pointer]
                            print("<-----------------Weekday Pointer String-------------->",weekday_pointer_string)
                            
                            for service in service_schedule_list:
                                if service.day == weekday_pointer_string:
                                    
                                    
                                    # service_open_time_str = time.strftime(service.open_time,"%H:%M")
                                    service_open_time_str = service.open_time.strftime("%H:%M")
                                    print("<---------------------------Service Open Time STR-------------->",service_open_time_str)
                                    service_close_time_str = service.close_time.strftime("%H:%M")
                                    print("<--------------------------Service Close Time STR---------------->",service_close_time_str)
                                    
                                    print("<--------------------------Service Time Cleaned------------------->",service_time_cleaned)

                                    if service_time_cleaned >= service_open_time_str and service_time_cleaned <= service_close_time_str:
                                        final_selected_service_ids.append(service.service.id)      

                                    
#                                         if service_time_object >= service.open_time and service_time_object <= service.close_time:
#                                             final_selected_service_ids.append(service.id)
                            
                            
                            weekday_pointer = (weekday_pointer+1)%7
                            print("<==========================Weekday Pointer Incremented----------------->",weekday_pointer)
                            if weekday_pointer == 0:
                                break
                        
                        print("<------------Final Selected Service IDs----------------->",final_selected_service_ids)
                    
                    for service in final_selected_service_ids:
                        match_score[service] = match_score[service] + 1


    
  
  
        print("<------------------After For Loop=========================>")
        
        print("<--------------------After mtaching Match Score-------------------->",match_score)
        
        sorted_match_score = sorted(match_score.items(),key=itemgetter(1),reverse=True)
        
        filtered_service_id = []
        
        print("<---------------------Sorted match Score------------------->",sorted_match_score)

        
        for service in sorted_match_score:
            if service[1] > THRESHOLD:
                filtered_service_id.append(service[0])
        
        
        
        print("<-------------------Above Threshold---------------------->",filtered_service_id)
        
        
        final_service_provider_ids = []
        
        for service_id in filtered_service_id:
            ServiceObj = Service.objects.get(id=service_id)
            ServiceProvider = ServiceObj.user
            ServiceProvider_uoi = UserOtherInfo.objects.get(user=ServiceProvider)
            

            if not user.is_anonymous:
                if ServiceProvider_uoi != request_uoi_object:
                    if ServiceProvider_uoi not in final_service_provider_ids:
                        final_service_provider_ids.append(ServiceProvider_uoi)
            else:
                if ServiceProvider_uoi not in final_service_provider_ids:
                    final_service_provider_ids.append(ServiceProvider_uoi)                
        
        
        print("<-------------------Final Service Provider ID---------------->",final_service_provider_ids)
        
        final_serialized = []
        for provider in final_service_provider_ids:
            serializer = FilteredProviderSerializer(provider,context={"lang":context_lang}).data
            final_serialized.append(serializer)
        

        session_list_provider_uoi_ids = [x.id for x in final_service_provider_ids]
        
        request.session['filtered_provider_ids'] = session_list_provider_uoi_ids
        request.session['filtered_service_ids']  = filtered_service_id

        if  PAGINATION == True:
            page = self.paginate_queryset(final_serialized)
            return self.get_paginated_response(page)
        else:
            return Response(final_serialized,status=HTTP_200_OK)                
            
            

SLOTS_VALID = False

class CheckTimeSlots(APIView):
    def post(self,request):

        weekdays_translation = {
            "اَلْإِثْنَيْن" : "Monday",
            "اَلثَّلَاثَاء" : "Tuesday",
            "اَلْأَرْبَعَاء" : "Wednesday",
            "اَلْخَمِيس" : "Thursday",
            "اَلْجُمْعَة" : "Friday",
            "اَلسَّبْت" : "Saturday",
            "اَلْأَحَد" : "Sunday"
        }
        lang = request.GET.get('lang')

        if lang != None:
            if lang in ["English","english","en"]:
                context_lang = "en"
            elif lang in ["Arabic","arabic","ar"]:
                context_lang = "ar"
        else:
            context_lang = "en"


        user =  request.user
        data =  request.data
        schedule = data['arrayofworkingdays']
        slot_check = []

        print("<---------------------Incoming Schedule----------------->",schedule)

        for schedule_object in schedule:
            day_raw = schedule_object['day']

            if context_lang == "ar":
                day = weekdays_translation[day_raw]
            else:
                day = day_raw

            # day = schedule_object['day']
            checked = schedule_object['checked']
            slot_array  = schedule_object['slots']

            if checked:
                for time_slot in slot_array:
                    print("<--------------Open Time----------------->",time_slot['openTime'])
                    open_time = time_slot['openTime'].strip()
                    print("<---------------Cleaned------------->",open_time)
                    if not NEW_TIME_FORMAT:
                        formatted_open_time = time.strptime(open_time,"%H:%M:%S")
                    else:
                        formatted_open_time = time.strptime(open_time,EXTERNAL_TIME_FORMAT)                        
                    # print("<--------------Open Time----------------->",open_time)
                    stand_open_time = time.strftime("%H:%M:%S",formatted_open_time)
                    print("<--------------Standard Open Time---------------->",stand_open_time)
                    close_time = time_slot['closeTime'].strip()
                    
                    if not NEW_TIME_FORMAT:
                        formatted_close_time = time.strptime(close_time,"%H:%M:%S")
                    else:
                        formatted_close_time = time.strptime(close_time,EXTERNAL_TIME_FORMAT)   
                                             
                    stand_close_time = time.strftime("%H:%M:%S",formatted_close_time)
                    print("<-------------------Standard Close Time-------------->",stand_close_time)

                    if stand_open_time > stand_close_time:
                        return Response({"msg":"Invalid Time Slot"},status=HTTP_400_BAD_REQUEST)
                    
                    t = (stand_open_time,stand_close_time)
                    slot_check.append(t)


                print("<-------------Slot Tuple List------------------->",slot_check)
                
                sorted_slot_check = sorted(slot_check,key=itemgetter(1))
                print("<----------Sorted Tuple List--------------------->",sorted_slot_check)

                plain_slot_list = []
                for item in sorted_slot_check:
                    for time_slot in item:
                        plain_slot_list.append(time_slot)
                print("<----------Plain SLot List----------------->",plain_slot_list)
        
                for i in range(len(plain_slot_list)-1):
                    if plain_slot_list[i] > plain_slot_list[i+1]:
                        return Response({"msg":"Invalid Time Slot"},status=HTTP_400_BAD_REQUEST)
                
                print("<---------TIME SLOT IS VALID-------------------->")
                
                
                other_service_schedules = []
                ServiceQS   =   Service.objects.filter(user=user.id)
                for services in ServiceQS:
                    ServiceScheduleQS = ServiceSchedule.objects.filter(service=services.id).filter(day=day)
                    for schedule in ServiceScheduleQS:
                        open_time = schedule.open_time
                        close_time = schedule.close_time
                        stand_open_time = open_time.strftime("%H:%M:%S")
                        stand_close_time = close_time.strftime("%H:%M:%S")
                        t = (stand_open_time,stand_close_time)
                        print("<-----------Other Services Open Time--------------->",stand_open_time)
                        print("<-----------Other Services Close Time------------------>",stand_close_time)
                        other_service_schedules.append(t)
                
                print("<----------------Other Service Schedules-------------->",other_service_schedules)

                merged_time_slots = other_service_schedules + slot_check
                print("<-----------------Merged list------------------------->",merged_time_slots)
                
                sorted_merged_time_slots = sorted(merged_time_slots,key=itemgetter(1))
                print("<----------Sorted Merged Tuple List--------------------->",sorted_merged_time_slots)

                plain_slot_list = []
                for item in sorted_merged_time_slots:
                    for time_slot in item:
                        plain_slot_list.append(time_slot)
                print("<----------Plain SLot List Merged----------------->",plain_slot_list)
        
                for i in range(len(plain_slot_list)-1):
                    if plain_slot_list[i] > plain_slot_list[i+1]:
                        return Response({"msg":"Selected time slots overlap with your existing services."},status=HTTP_400_BAD_REQUEST)
                SLOTS_VALID = True
                return Response({"msg":"Valid Slots"},status=HTTP_200_OK)





class CancelAppointment(APIView):
    def post(self,request):

        print("<----------Incoming Request Data--------------->",request.data)
        data = request.data
        try:
            booking_id = data['booking_id']
        except:
            return Response({"msg":"Booking ID missing in request"},status=HTTP_400_BAD_REQUEST)

        try:
            usertype = data['usertype']
        except:
            return Response({"msg":"Usertype missing in request"},status=HTTP_400_BAD_REQUEST)

        try:
            cancel_request_timestamp = data["cancel_request_timestamp"]
        except:
            return Response({"msg":"Cancel Request Timestamp missing in request"},status=HTTP_400_BAD_REQUEST)

        try:
            user_id = data['user_id']
        except:
            return Response({"msg":"User ID missing in request"},status=HTTP_400_BAD_REQUEST)


        BookingObject = NewBookingModel.objects.get(booking_id = booking_id)
        uoi_object = UserOtherInfo.objects.get(id=int(user_id))
        fcm_receiver_token = uoi_object.fcm_token

        if usertype in ["provider","Provider"]:
            BookingObject.cancelled_by_provider = True
            BookingObject.booking_cancelled = True
            BookingObject.save()

            return Response({"msg":"Booking Declined"},status=HTTP_200_OK)

        else:
            BookingObject.cancelled_by_requestor = True
            BookingObject.booking_cancelled = True
            BookingObject.save()
            return Response({"msg":"Booking Declined"},status=HTTP_200_OK)            




class CancelAppointment_Old(APIView):
    def post(self,request):
        # cancel_request_time = datetime(2019,9,20,19,45)        
        cancel_request_time = datetime.now()
        data =  request.data
        print("<--------------Request Data----------------->",data)
        user =  request.user
        UserObject = User.objects.get(id=user.id)
        booking_id = data['booking_id']

        try:
            usertype = data['usertype']
        except:
            return Response({"msg":"Usertype missing in request"},status=HTTP_400_BAD_REQUEST)

        try:
            cancel_request_timestamp = data["cancel_request_timestamp"]
        except:
            return Response({"msg":"Cancel Request Timestamp missing in request"},status=HTTP_400_BAD_REQUEST)

        try:
            user_id = data['user_id']
        except:
            return Response({"msg":"User ID missing in request"},status=HTTP_400_BAD_REQUEST)

        today  = cancel_request_time.strftime("%Y-%m-%d")
        

        BookingObject = NewBookings.objects.get(booking_id = booking_id)
        BookingObject_created   =   BookingObject.created

        LivePaymentObject = LivePayments.objects.get(booking_ID__exact = booking_id)


        service_date  = BookingObject.service_date
        service_time  = BookingObject.service_time
        service_time_formatted = service_time.strftime("%H:%M:%S")
        service_date_formatted = service_date.strftime("%Y-%m-%d")
        merged_service_time = service_date_formatted + " " + service_time_formatted

        merged_service_time_object = datetime.strptime(merged_service_time,"%Y-%m-%d %H:%M:%S")

        print("<--------------Merged Service TIme------------->",merged_service_time_object)
        print("<--------------Merged Service TIme------------->",type(merged_service_time_object))
        UOI_Object  = UserOtherInfo.objects.get(user = user)
        print("<---------------UOI object----------->",UOI_Object)
        print("<---------------UOI Object ID----------->",UOI_Object.id)
        print("<---------------user object ID----------->",user.id)
        usertype    = UOI_Object.usertype


        print("<----------------Cancel Request Time---------------------->",cancel_request_time)
        BookingObject.cancellation_date = cancel_request_time
        BookingObject.cancellation_time = cancel_request_time


        if usertype in ["provider","Provider"]:
            BookingObject.cancelled_by_provider = True
            BookingObject.booking_cancelled = True
            BookingObject.save()

#===============Notification Handler=======================
            # InAppBookingNotificationsObject = InAppBookingNotifications(
            #     from_user_id = UOI_Object,
            #     from_user_name = UserObject.get_full_name(),
            #     to_user_id = BookingObject.requestor_id,
            #     to_user_name = BookingObject.requestor,
            #     notification_type = "Booking Cancelled",
            #     notification_title = "Your booking request " + "(Booking ID: " + BookingObject.booking_id +")"+" has been declined by the service provider.",
            #     service_name      = BookingObject.service_name,
            #     notification_time = timezone.now(),
            #     notification_date  = datetime.now(),
            #     to_user_usertype = REQUESTOR_STRING
            #     )

            # InAppBookingNotificationsObject.save()
            # BookingObject.save()
            # fcm_receiver = BookingObject.requestor_id
            # print("<-----------------FCM Receiver------------->",fcm_receiver)
            # UserOtherInfoObject = UserOtherInfo.objects.get(id=fcm_receiver.id)
            # fcm_receiver_token = UserOtherInfoObject.fcm_token
            # message_body = "Service provider declined your request." 
            
            # try:
            #     send_to_one(fcm_receiver_token,message_body,"Booking Declined")
            # except:
            #     pass
#===============Notification Handler=======================
            
            return Response({"msg":"Booking Declined"},status=HTTP_200_OK)


        else:
            if LivePaymentObject.payment_method == "Cash":
                if (merged_service_time_object - cancel_request_time) < timedelta(hours=24):                
                    return Response({"msg":"You cannot cancel this booking.Please contact provider.","status":"CANCELLATION_ERR"},status=HTTP_200_OK)
                else:
                    BookingObject.cancelled_by_requestor = True
                    BookingObject.booking_cancelled = True
                    BookingObject.save()

#=================Notification handler================================
                    # InAppBookingNotificationsObject = InAppBookingNotifications(
                    #     from_user_id = UOI_Object,
                    #     from_user_name = UserObject.get_full_name(),
                    #     to_user_id = BookingObject.provider_id,
                    #     to_user_name = BookingObject.provider,
                    #     notification_type = "Booking Cancelled",
                    #     notification_title = "Your booking request " + "(Booking ID:" + BookingObject.booking_id +")"+" has been declined by the service requestor.",
                    #     service_name      = BookingObject.service_name,
                    #     notification_time = timezone.now(),
                    #     notification_date  = datetime.now(),
                    #     to_user_usertype  = PROVIDER_STRING
                    #     )
                    # InAppBookingNotificationsObject.save()
                    # BookingObject.save()
                    # fcm_receiver = BookingObject.provider_id
                    # UserOtherInfoObject = UserOtherInfo.objects.get(id=fcm_receiver.id)
                    # fcm_receiver_token = UserOtherInfoObject.fcm_token
                    # message_body = "Service requestor declined your request."
                    # try:
                    #     send_to_one(fcm_receiver_token,message_body,"Request Declined")
                    # except:
                    #     pass
#=================Notification handler================================
                    return Response({"msg":"Booking Declined"},status=HTTP_200_OK)
            else:
                if service_date_formatted == today:
                    BookingObject.cancellation_fee_applicable  = True
                    BookingObject.cancelled_by_requestor = True
                    BookingObject.cancellation_fee = round((((BookingObject.service_charges + BookingObject.admin_charges) * CANCELLATION_FEE_PERCENTAGE)/100),2)
                    BookingObject.save()
                    return Response({"msg":"Cancellation fees applicable"},status=HTTP_200_OK)
                else:
                    BookingObject_created   =   BookingObject.created
                    if (merged_service_time_object - cancel_request_time) < timedelta(hours=24):
                        BookingObject.cancellation_fee_applicable  = True
                        BookingObject.cancelled_by_requestor = True
                        BookingObject.cancellation_fee = round((((BookingObject.service_charges + BookingObject.admin_charges) * CANCELLATION_FEE_PERCENTAGE)/100),2)
                        BookingObject.save()
                        return Response({"msg":"Cancellation fees applicable"},status=HTTP_200_OK) 



        # if LivePaymentObject.payment_method == "Cash":
        #     if not (usertype == "provider" or usertype == "Provider"):
        #         if (cancel_request_time - BookingObject_created) > timedelta(hours=24):
        #             return Response({"msg":"You cannot cancel this booking.Please contact provider.","status":"CANCELLATION_ERR"},status=HTTP_400_BAD_REQUEST)
        #         else:
        #             BookingObject.cancelled_by_requestor = True
        #             BookingObject.booking_cancelled = True
        #             BookingObject.save()
        #             return Response({"msg":"Booking Declined"},status=HTTP_200_OK)
            


        # if usertype == "provider" or usertype == "Provider":
        #     # return Response({"msg":"Provider cannot decline a booking"},status=HTTP_400_BAD_REQUEST)
        #     BookingObject.cancelled_by_provider = True
        #     BookingObject.booking_cancelled = True
        #     BookingObject.save()

        # else:
        #     if service_date_formatted == today:
        #         BookingObject.cancellation_fee_applicable  = True
        #         BookingObject.cancelled_by_requestor = True
        #         BookingObject.cancellation_fee = round((((BookingObject.service_charges + BookingObject.admin_charges) * CANCELLATION_FEE_PERCENTAGE)/100),2)
        #         BookingObject.save()
        #         print("<-----------------Cancellation Fee Requstor Today================>")
        #         return Response({"msg":"Cancellation fees applicable"},status=HTTP_200_OK)

        # # 15 Ca%
        #     else:
        #         BookingObject_created   =   BookingObject.created
        #         # today_object            =   cancel_request_time
        #         if (cancel_request_time - BookingObject_created) > timedelta(hours=24):
        #             print("Cancel time more than 24")
        #             BookingObject.cancellation_fee_applicable  = True
        #             BookingObject.cancelled_by_requestor = True
        #             BookingObject.cancellation_fee = round((((BookingObject.service_charges + BookingObject.admin_charges) * CANCELLATION_FEE_PERCENTAGE)/100),2)
        #             BookingObject.save()
        #             print("<-----------------Cancellation Fee Requstor Future================>")
        #             return Response({"msg":"Cancellation fees applicable"},status=HTTP_200_OK)                

        # print("<--------------------Incoming Booking ID------------------>",booking_id)
        # BookingObject.booking_cancelled = True
        
        try:
            Schedule_object = BookingObject.service_slot_id
            if Schedule_object.service_capacity == 0:
                Schedule_object.service_capacity = 1
                Schedule_object.save()
            else:
                Schedule_object.service_capacity = 1
                Schedule_object.save()
        except:
            pass
        
        
        # BookingObject.save()
            # try:
        UOI_Object  = UserOtherInfo.objects.get(user = user)
        print("<---------------UOI object----------->",UOI_Object)
        print("<---------------UOI Object ID----------->",UOI_Object.id)
        print("<---------------user object ID----------->",user.id)
        usertype    = UOI_Object.usertype
        print("<-----------------------Incoming request usertype-------------->",usertype)
        if usertype == "provider" or usertype == "Provider":
            BookingObject.cancelled_by_provider = True
            InAppBookingNotificationsObject = InAppBookingNotifications(
                from_user_id = UOI_Object,
                from_user_name = UserObject.get_full_name(),
                to_user_id = BookingObject.requestor_id,
                to_user_name = BookingObject.requestor,
                notification_type = "Booking Cancelled",
                notification_title = "Your booking request " + "(Booking ID: " + BookingObject.booking_id +")"+" has been declined by the service provider.",
                service_name      = BookingObject.service_name,
                notification_time = timezone.now(),
                notification_date  = datetime.now(),
                to_user_usertype = REQUESTOR_STRING
                )

            InAppBookingNotificationsObject.save()
            BookingObject.save()
            fcm_receiver = BookingObject.requestor_id
            print("<-----------------FCM Receiver------------->",fcm_receiver)
            UserOtherInfoObject = UserOtherInfo.objects.get(id=fcm_receiver.id)
            fcm_receiver_token = UserOtherInfoObject.fcm_token
            message_body = "Service provider declined your request." 
            
            try:
                send_to_one(fcm_receiver_token,message_body,"Booking Declined")
            except:
                pass
            
            return Response({"msg":"Booking Declined"},status=HTTP_200_OK)
        
        
        else:  #If cancellation is done by requestor
            BookingObject.cancelled_by_requestor = True
            InAppBookingNotificationsObject = InAppBookingNotifications(
                from_user_id = UOI_Object,
                from_user_name = UserObject.get_full_name(),
                to_user_id = BookingObject.provider_id,
                to_user_name = BookingObject.provider,
                notification_type = "Booking Cancelled",
                notification_title = "Your booking request " + "(Booking ID:" + BookingObject.booking_id +")"+" has been declined by the service requestor.",
                service_name      = BookingObject.service_name,
                notification_time = timezone.now(),
                notification_date  = datetime.now(),
                to_user_usertype  = PROVIDER_STRING
                
                )
            InAppBookingNotificationsObject.save()
            BookingObject.save()
            fcm_receiver = BookingObject.provider_id
            UserOtherInfoObject = UserOtherInfo.objects.get(id=fcm_receiver.id)
            fcm_receiver_token = UserOtherInfoObject.fcm_token
            message_body = "Service requestor declined your request."
            try:
                send_to_one(fcm_receiver_token,message_body,"Request Declined")
            except:
                pass
            return Response({"msg":"Booking Declined"},status=HTTP_200_OK)



class EditProfile(APIView):
    def put(self,request):
        user = request.user
        data = request.data
        print("<----------------Request Data Payload------------>",data)
        UserObj = User.objects.get(id=user.id)
        UOIObject = UserOtherInfo.objects.get(user=UserObj)
        try:
            UserObj.first_name          = data['first_name']
            UserObj.last_name           = data['last_name']
            UOIObject.profile_image_s3 = data['profile_image']
            UOIObject.user_address       = data['user_address']
            UOIObject.user_address_lat  = data['user_address_lat']
            UOIObject.user_address_long = data['user_address_long']
            UOIObject.locality          = data['locality']
            UOIObject.bio               = data['bio']
            UOIObject.idcard             = data['id_card']
            print("<----------Before saving User Object--------------->")
            UserObj.save()
            print("<----------After Saving User Object--------------->")

            print("<------------Before Saving UOI Object----------------->")
            UOIObject.save()
            print("<-----------After Saving UOI Object------------------------>")
            return Response({"msg":"Profile Successfully updated"},status=HTTP_200_OK)
        except:
            return Response({"msg":"Missing info/Key.Please check."},status=HTTP_400_BAD_REQUEST)




class EditService(APIView):
    def post(self,request):
        # user = request.user
        data =  request.data
        print("<------------------Incoming request data-------------->",data)
        service_id = data['service_id']
        try:
            ServiceObject                       =   Service.objects.get(id = service_id)
            print("<-------------------Service object------------------->",ServiceObject)
            ServiceObject.service_name          =   data['service_name']
            ServiceObject.experience            =   data['experience']
            ServiceObject.levelskill            =   data['levelskill']
            ServiceObject.service_place         =   data['service_place']
            ServiceObject.distance_limit        =   data['distance_limit']
            ServiceObject.service_pricing       =   data['service_pricing']
            ServiceObject.pricing_timing_unit   =   data['pricing_timing_unit']
            ServiceObject.quote_at_request      =   data['quote_at_request']
            ServiceObject.provider_tools        =   data['provide_tools']
            ServiceObject.tool_specify          =   data['tool_specify']
            ServiceObject.instant_booking       =   data['instant_booking']
            ServiceObject.service_location      =   data['service_location']
            ServiceObject.service_location_lat  =   data['service_location_lat']
            ServiceObject.service_location_long =   data['service_location_long']
            ServiceObject.locality              =   data['locality']
            ServiceObject.save()

            try:

                ServiceImageObject = ServiceImage.objects.get(service=ServiceObject)
                ServiceImageObject.delete()

                ServiceImageObject = ServiceImage(service=ServiceObject)
                service_images = data['service_images']

                for i in range(0,len(service_images)):
                    if (service_images[i] != "" or serviceimages[i] != None):
                        if i==0:
                            ServiceImageObject.service_img_file_1_s3    =   service_images[i]
                            ServiceImageObject.service_img_file         =   service_images[i]
                        
                        elif i==1:
                            ServiceImageObject.service_img_file_2_s3    =   service_images[i]
                            ServiceImageObject.service_img_file1        =   service_images[i]

                        elif i==2:
                            ServiceImageObject.service_img_file_3_s3    =   service_images[i]
                            ServiceImageObject.service_img_file2        =   service_images[i]

                ServiceImageObject.save()

            except:
                ServiceImageObject = ServiceImage(service=ServiceObject)
                service_images = data['service_images']

                for i in range(0,len(service_images)):
                    if (service_images[i] != "" or serviceimages[i] != None):
                        if i==0:
                            ServiceImageObject.service_img_file_1_s3    =   service_images[i]
                            ServiceImageObject.service_img_file         =   service_images[i]
                        
                        elif i==1:
                            ServiceImageObject.service_img_file_2_s3    =   service_images[i]
                            ServiceImageObject.service_img_file1        =   service_images[i]

                        elif i==2:
                            ServiceImageObject.service_img_file_3_s3    =   service_images[i]
                            ServiceImageObject.service_img_file2        =   service_images[i]

                ServiceImageObject.save()


            new_schedule    =   data['arrayofworkingdays']
            print("<----------------Captured Working Days-------------->",new_schedule)

            try:
                ServiceScheduleObjects   =   ServiceSchedule.objects.filter(service=ServiceObject)
                print("<--------------------Service Schedule--------------------->",ServiceScheduleObjects)
                if len(ServiceScheduleObjects) == 0:
                    for schedule_object in new_schedule:
                        day         =   schedule_object['day']
                        checked     =   schedule_object['checked']
                        slot_array  =   schedule_object['slots']

                        if checked  == "True":
                            for time_slot in slot_array:
                                open_time               =   time_slot['openTime'].strip()
                                
                                if not NEW_TIME_FORMAT:
                                    formatted_open_time     =   time.strptime(open_time,"%H:%M:%S")
                                else:
                                    formatted_open_time     =   time.strptime(open_time,EXTERNAL_TIME_FORMAT)
                                    
                                stand_open_time         =   time.strftime("%H:%M:%S",formatted_open_time)
                                
                                
                                close_time              =   time_slot['closeTime'].strip()
                                
                                if not NEW_TIME_FORMAT:
                                    formatted_close_time    =   time.strptime(close_time,"%H:%M:%S")
                                else:
                                    formatted_close_time    =   time.strptime(close_time,EXTERNAL_TIME_FORMAT)
                                                                        
                                stand_close_time        =   time.strftime("%H:%M:%S",formatted_close_time)

                                ServiceScheduleObject   =   ServiceSchedule(
                                    service     =   ServiceObject,
                                    day         =   day,
                                    checked     =   checked,
                                    open_time   =   stand_open_time,
                                    close_time  =   stand_close_time,
                                    )
                                ServiceScheduleObject.save()

                else:
                    print("<------------------------Inside Schedule Delete clause--------------->")
                    for schedule in ServiceScheduleObjects:
                        schedule.delete()
                    print("<--------------------After deleting Service Schedules---------------->")
                    for schedule_object in new_schedule:
                        day         =   schedule_object['day']
                        checked     =   schedule_object['checked']
                        slot_array  =   schedule_object['slots']

                        if checked  == "True":
                            for time_slot in slot_array:
                                open_time               =   time_slot['openTime'].strip()
                                
                                if not NEW_TIME_FORMAT:
                                    formatted_open_time     =   time.strptime(open_time,"%H:%M:%S")
                                else:
                                    formatted_open_time     =   time.strptime(open_time,EXTERNAL_TIME_FORMAT)
                                    
                                stand_open_time         =   time.strftime("%H:%M:%S",formatted_open_time)
                                close_time              =   time_slot['closeTime'].strip()
                                
                                if not NEW_TIME_FORMAT:
                                    formatted_close_time    =   time.strptime(close_time,"%H:%M:%S")
                                else:
                                    formatted_close_time    =   time.strptime(close_time,EXTERNAL_TIME_FORMAT)
                                    
                                stand_close_time        =   time.strftime("%H:%M:%S",formatted_close_time)

                                ServiceScheduleObject   =   ServiceSchedule(
                                    service     =   ServiceObject,
                                    day         =   day,
                                    checked     =   checked,
                                    open_time   =   stand_open_time,
                                    close_time  =   stand_close_time,
                                    )
                                ServiceScheduleObject.save()
                return Response({"msg":"Service successfully edited","Status":"SERVICE_EDIT_SAVED"},status=HTTP_200_OK)
            except:
                pass            
        except Exception as e:
            print("<-------------Exception---------->",e)
            print("<---------------------Some error occurred.Inside Exception clause-------------------->")
            return Response({"msg":"Some error occured","Status":"SERVICE_EDIT_FAILED"},status=HTTP_400_BAD_REQUEST)




class BookingCalender(APIView):
    def get(self,request):
        user = request.user
        UOIObject = UserOtherInfo.objects.get(user=user)

        BookingQS = NewBookingModel.objects.filter(provider_id = UOIObject).filter(Q(accepted_by_requester = True) | Q(accepted_by_provider = True)).\
            exclude(Q(booking_cancelled = True) | Q(booking_completed = True))
        
    
        unique_dates = []
        for BookingObj in BookingQS:
            if BookingObj.service_date not in unique_dates:
                unique_dates.append(BookingObj.service_date)
        
        return Response(unique_dates,status=HTTP_200_OK)





def compute_avg_rating(service_id,rating):
    '''
    Function to re-compute average of Service and User when a new rating is provided.
    '''
    print("<-------------------Inside Compute Average----------------->")
    print("<-------------------")
    serviceObject = Service.objects.get(id = service_id)
    print("<------------------Service Object fetched------------------->",serviceObject)
    user_Object = User.objects.get(id=serviceObject.user.id)
    print("<------------------User Object fetched--------------->",user_Object)
    UOI_Object  = UserOtherInfo.objects.get(user=user_Object)
    print("<-------------------UOI Object----------------------->",UOI_Object)
    current_avg_rating = serviceObject.avg_rating
    print("<-----------------------current avg rating----------------------->",current_avg_rating)

    current_rating_count  = serviceObject.count_of_rating
    print("<-----------------------Current rating Count-------------------->",current_rating_count)
    incoming_rating  = int(rating)


    if current_rating_count == 0 or current_rating_count == None:
        print("<---------------First Rating on service---------------->")
        if current_avg_rating == 0 or current_rating_count == None:
            print("<--------------First avg rating------------------->")
            new_rating = incoming_rating
            new_count = 1
            serviceObject.avg_rating = new_rating
            serviceObject.count_of_rating = new_count
            serviceObject.save()
            if UOI_Object.count_of_rating == 0 or UOI_Object.count_of_rating == None:
                print("<---------First Rating on person----------------->")
                if UOI_Object.avg_rating == 0 or UOI_Object.avg_rating == None:
                    print("<---------------------First avg rating on person-------->")
                    UOI_Object.avg_rating = incoming_rating
                    UOI_Object.count_of_rating = 1
                    UOI_Object.avg_rating_rounded = round(incoming_rating, 1)
                    UOI_Object.save()
                    return "OK"
                
                else:
                    print("<--------------Invalid Case-------------------->")
                    return "Error"
            print("<-----------Invalid Case--------------->")
            return "Error"
    
    
    else:
        sum_of_rating = current_avg_rating * current_rating_count
        print("<--------------------Sum_of_ OLD Rating_------------------>",sum_of_rating)
        new_sum_of_rating = sum_of_rating + incoming_rating
        new_count_of_rating  = current_rating_count + 1
        new_avg_rating  =  round((new_sum_of_rating / new_count_of_rating),5)
        print("<---------------New Avg Rating---------------------->",new_avg_rating)
        serviceObject.avg_rating  = new_avg_rating
        serviceObject.count_of_rating = new_count_of_rating
        serviceObject.save()


        user_current_rating = UOI_Object.avg_rating
        user_current_count_of_rating = UOI_Object.count_of_rating 

        user_sum_of_rating = user_current_rating * user_current_count_of_rating
        new_user_sum_of_rating = user_sum_of_rating + new_avg_rating
        new_user_count_of_rating = user_current_count_of_rating + 1
        new_user_avg_rating = round((new_user_sum_of_rating / new_user_count_of_rating), 5)

        UOI_Object.avg_rating = new_user_avg_rating
        UOI_Object.count_of_rating = new_user_count_of_rating
        
        UOI_Object.avg_rating_rounded = round(new_user_avg_rating,1)
        UOI_Object.save()
        return "OK"





class SubmitFeedback(APIView):
    '''
    API to Submit Feedback after completion of Task
    '''
    def post(self,request):
        print("<------------Incoming request Data--------------->",request.data)
        print("<------------Incoming request User--------------->",request.user)
        user = request.user
        data = request.data
        UOIObject = UserOtherInfo.objects.get(user=user)
        booking_id      =   data['booking_id']
        feedback_user   =   UOIObject
        rating          =   data['rating']
        compliment      =   data['compliment']
        try:
            review          =   data['review']
        except:
            review  = ""
        feedback_date   =   timezone.now()
        print("<-------------------Feedback Date------------------>",feedback_date)
        feedback_time   =   timezone.now()
        print("<--------------------Feedback Time--------------------->",feedback_time)
        BookingObj       =   NewBookings.objects.get(booking_id__exact=booking_id)
        print("<-----------------Booking Object----------------------->",BookingObj)
        service_id      =   BookingObj.service_ID
        print("<-------------Before Saving Object------------------------>")
        booking_object  =   NewBookingModel.objects.get(booking_id__exact=booking_id)
        ProviderObject  = booking_object.provider_id
        
        fcm_receiver_token =  ProviderObject.fcm_token
        message_body = "Service Requestor has given a review to your service."
        try:
            send_to_one(fcm_receiver_token,message_body,"New Feedback received.")
        except:
            pass
        ServiceFeedbackObject = ServiceFeedback(
            booking_id = BookingObj,
            service_id = service_id,
            feedback_user = feedback_user,
            rating = rating,
            compliment = compliment,
            review = review,
            feedback_date = feedback_date,
            feedback_time = feedback_time
        )
        ServiceFeedbackObject.save()
        data = compute_avg_rating(service_id.id,rating)
        if data == "OK":
            return Response({"msg":"Feedback Submitted Successfully","status":"FEEDBACK_SAVED"},status=HTTP_200_OK)
        else:
            return Response({"msg":"Feedback submission failed.","status":"FEEDBACK_SUBMISSION_FAILED"},status=HTTP_200_OK)




            
class FetchMonthAvailability(APIView):

    def post(self,request):
        start_time = datetime.now()
        request_date_time = datetime.now()
        # request_date_time = datetime(9999,9,9,2)
        INTERNAL_TIME_FORMAT_LOCAL = "%H:%M:%S"
        INTERNAL_DATE_FORMAT_LOCAL = "%Y-%m-%d"

        lang = request.GET.get('lang')

        if lang != None:
            if lang in ["English","english","en"]:
                context_lang = "en"
            elif lang in ["Arabic","arabic","ar"]:
                context_lang = "ar"
        else:
            context_lang = "en"

        

        data = request.data
        print("<-------------Data Fetch MOnth------------>",data)
        service_id = data['service_id']
        
        request_time_string = request_date_time.strftime(INTERNAL_TIME_FORMAT_LOCAL)
        request_date_string = request_date_time.strftime(INTERNAL_DATE_FORMAT_LOCAL)

        try:
            service_object = Service.objects.get(id=service_id)
        except:
            return Response({"msg":"Service ID does not exist"},status=HTTP_400_BAD_REQUEST)
        
        day_dict = {
            "Monday"    : 0,
            "Tuesday"   : 1,
            "Wednesday" : 2,
            "Thursday"  : 3,
            "Friday"    : 4,
            "Saturday"  : 5,
            "Sunday"    : 6
            }
        day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        
        day_dict_arabic = {
            "اَلْإِثْنَيْن"     : 0,
            "اَلثَّلَاثَاء"    : 1,
            "اَلْأَرْبَعَاء"    : 2,
            "اَلْخَمِيس"     : 3,
            "اَلْجُمْعَة"     : 4,
            "اَلسَّبْت"      : 5,
            "اَلْأَحَد"       : 6,
        }

        day_list_arabic = [ "اَلْإِثْنَيْن","اَلثَّلَاثَاء","اَلْأَرْبَعَاء","اَلْخَمِيس","اَلْجُمْعَة","اَلْجُمْعَة","اَلْأَحَد"]


        request_date_number = request_date_time.weekday()


        BookingQS = NewBookingModel.objects.filter(service_ID = service_object).\
            filter(Q(accepted_by_requester = True) | Q(accepted_by_provider = True)).\
            exclude(Q(booking_completed = True) | Q(booking_cancelled = True))


        booked_dates = {}

        for booking in BookingQS:
            service_date = booking.service_date.strftime(INTERNAL_DATE_FORMAT_LOCAL)
            service_time = booking.service_time.strftime(INTERNAL_TIME_FORMAT_LOCAL)

            if service_date in booked_dates:
                booked_dates[service_date].append(service_time)
            else:
                service_time_list = []
                service_time_list.append(service_time)
                booked_dates[service_date] = service_time_list

        ServiceScheduleQS = ServiceSchedule.objects.filter(service=service_object)
        print("<-------------_ServiceScheduleQS------------->",ServiceScheduleQS)
        available_day_number_raw = []
        for schedule_raw in ServiceScheduleQS:
            print("<----------Schedule------------>",schedule_raw.id)
            schedule = ServiceSchedule.objects.get(id=schedule_raw.id)
            print("<-------------Schedule object----------->",schedule)
            print("<-------------Schedule object day-------->",schedule.day)

            if context_lang == "en":
                if day_dict[schedule.day] not in available_day_number_raw:
                    available_day_number_raw.append(day_dict[schedule.day])
            elif context_lang == "ar":
                if day_dict_arabic[schedule.day] not in available_day_number_raw:
                    available_day_number_raw.append(day_dict_arabic[schedule.day])

        available_day_number_sorted = sorted(available_day_number_raw)

        final_response_array_object ={}
        final_response_array = []

        for day_number in available_day_number_sorted:

            dates_of_month = []
            final_response_array_object ={}

            if day_number >= request_date_number:
                delta = day_number - request_date_number
            else:
                delta = 7 - (request_date_number - day_number) 

            start_date = request_date_time + timedelta(days=delta)
            end_date = start_date + timedelta(days=AVAILABILITY_MAX_DAYS)


            date_pointer_string     =   start_date.strftime(INTERNAL_DATE_FORMAT_LOCAL)
            end_date_string         =   end_date.strftime(INTERNAL_DATE_FORMAT_LOCAL)
            date_pointer_object     =   start_date

            if context_lang == "en":
                Service_Schedule_QS     =   ServiceScheduleQS.filter(day=day_list[day_number])
            elif context_lang == "ar":
                Service_Schedule_QS     =   ServiceScheduleQS.filter(day=day_list_arabic[day_number])                
            
            slots_raw = []

            for schedule in Service_Schedule_QS:
                slots_raw.append((schedule.open_time.strftime(INTERNAL_TIME_FORMAT_LOCAL),schedule.close_time.strftime(INTERNAL_TIME_FORMAT_LOCAL)))

            sorted_slots = sorted(slots_raw,key=itemgetter(1))
            
            final_slot_array = []
            dates_of_month_array = []

            while date_pointer_string <= end_date_string:

                selected_time_slots = []
                final_slot_array_object = {}

                if date_pointer_string in booked_dates:
                    if date_pointer_string == request_date_string: #Today's Booking
                        for time_slot in sorted_slots:
                            if time_slot[0] >= request_time_string:

                                for service_time in booked_dates[date_pointer_string]:

                                    open_time_object = datetime.strptime(time_slot[0],INTERNAL_TIME_FORMAT_LOCAL)
                                    close_time_object = datetime.strptime(time_slot[1],INTERNAL_TIME_FORMAT_LOCAL)
                                    
                                    open_time_string = open_time_object.strftime(EXTERNAL_TIME_FORMAT)
                                    close_time_string = close_time_object.strftime(EXTERNAL_TIME_FORMAT)

                                    if time_slot[0] <= service_time and service_time <= time_slot[1]:

                                        slot_object = {
                                            "open_time" : open_time_string,
                                            "close_time": close_time_string,
                                            "available" : False
                                        }
                                    else:
                                        slot_object = {
                                            "open_time" : open_time_string,
                                            "close_time": close_time_string,
                                            "available" : True
                                        }

                                    selected_time_slots.append(slot_object)
                    else:
                        for time_slot in sorted_slots:
                            for service_time in booked_dates[date_pointer_string]:

                                open_time_object = datetime.strptime(time_slot[0],INTERNAL_TIME_FORMAT_LOCAL)
                                close_time_object = datetime.strptime(time_slot[1],INTERNAL_TIME_FORMAT_LOCAL)
                                
                                open_time_string = open_time_object.strftime(EXTERNAL_TIME_FORMAT)
                                close_time_string = close_time_object.strftime(EXTERNAL_TIME_FORMAT)

                                if time_slot[0] <= service_time and service_time <= time_slot[1]:

                                    slot_object = {
                                        "open_time" : open_time_string,
                                        "close_time": close_time_string,
                                        "available" : False
                                    }
                                else:
                                    slot_object = {
                                        "open_time" : open_time_string,
                                        "close_time": close_time_string,
                                        "available" : True
                                    }
                                    
                                selected_time_slots.append(slot_object)
                    
                else:
                    for time_slot in sorted_slots:

                        open_time_object = datetime.strptime(time_slot[0],INTERNAL_TIME_FORMAT_LOCAL)
                        close_time_object = datetime.strptime(time_slot[1],INTERNAL_TIME_FORMAT_LOCAL)
                        
                        open_time_string = open_time_object.strftime(EXTERNAL_TIME_FORMAT)
                        close_time_string = close_time_object.strftime(EXTERNAL_TIME_FORMAT)


                        slot_object = {
                            "open_time" : open_time_string,
                            "close_time": close_time_string,
                            "available" : True
                        }
                        
                        selected_time_slots.append(slot_object)

                if len(selected_time_slots) > 0:

                    date_pointer_object = datetime.strptime(date_pointer_string,INTERNAL_DATE_FORMAT_LOCAL)
                    date_pointer_string_external = date_pointer_object.strftime(EXTERNAL_DATE_FORMAT)

                    final_slot_array_object["date"] = date_pointer_string_external
                    final_slot_array_object["details"] = selected_time_slots

                    final_slot_array.append(final_slot_array_object)

                    dates_of_month_array.append(date_pointer_string_external)

                date_pointer_object = date_pointer_object + timedelta(days=7)
                date_pointer_string = date_pointer_object.strftime(INTERNAL_DATE_FORMAT_LOCAL)

            if context_lang == "en":
                final_response_array_object["day"] = day_list[day_number]
            elif context_lang == "ar":
                final_response_array_object["day"] = day_list_arabic[day_number]

            final_response_array_object["dates_of_month"] = dates_of_month_array
            final_response_array_object["slots"] = final_slot_array
            final_response_array.append(final_response_array_object)

        end_time = datetime.now()
        print("<-------------Start Time-------------->",start_time)
        print("<-------------End Time---------------->",end_time)
        print("<-------------Time Delta-------------->",end_time-start_time)
        return Response(final_response_array,status=HTTP_200_OK)
            
        
        




def card_validation(card_number):
    
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10



class ValidateAndSaveCard(APIView):
    def post(self,request):
        print("<----------------Card Details Request Data------------>")

        DEBUG = False


        user                =   request.user
        data                =   request.data
        print("<----------------Card Details Request Data------------>",data)
        card_number         =   data['card_number']
        valid_upto          =   data['valid_upto']
        card_holder_name    =   data['card_holder_name']
        card_number_cleaned =   card_number.replace("-","")
        
        if not card_number_cleaned.isdigit():
            return Response({"msg":"Card is invalid","status":"CARD_INVALID"},status=HTTP_400_BAD_REQUEST)
        

        valid               =   card_validation(card_number_cleaned)


        UOI_Object          =   UserOtherInfo.objects.get(user=user.id)
        if card_holder_name == "" or card_holder_name == None:
            card_holder_name = user.get_full_name()
        else:
            card_holder_name = ""
        
        print("<------------------------Credit Card Holder Name---------------------->",card_holder_name)
        credit_card_last_segment =   card_number[-4:]
        print("<------------Credit Card Components--------------->",credit_card_last_segment)

        if valid == 0:
            BankingInfoObject = BankingInfo(
                card_holder   = UOI_Object,
                card_holder_name    =   card_holder_name,
                credit_card_number  =   card_number_cleaned,
                credit_card_masked      =   "XXXX-XXXX-XXXX-" + credit_card_last_segment,
                valid_upto          =   valid_upto,
                )
            BankingInfoObject.save()
            
            return Response({"msg":"Card is Valid","status":"CARD_VALID"},status=HTTP_200_OK)
        else:
            if DEBUG:
                BankingInfoObject = BankingInfo(
                    card_holder   = UOI_Object,
                    card_holder_name    =   card_holder_name,
                    credit_card_number  =   card_number,
                    credit_card_masked      =   "XXXX-XXXX-XXXX-" + credit_card_last_segment,
                    valid_upto          =   valid_upto,
                    )
                BankingInfoObject.save()
                return Response({"msg":"Card is Valid","status":"CARD_VALID"},status=HTTP_200_OK)
            else:
                return Response({"msg":"Card is invalid","status":"CARD_INVALID"},status=HTTP_400_BAD_REQUEST)






class FetchSavedCards(APIView):
    def get(self,request):
        user        =   request.user
        print("<-------------------Fetched User------------------------------>",user)
        if user.is_anonymous:
            return Response({"msg":"You are not logged in.","status":"ANONYMOUS_USER"},status=HTTP_400_BAD_REQUEST)
        UOI_Object  =   UserOtherInfo.objects.get(user=user)
        SavedCardQS =   BankingInfo.objects.filter(card_holder = UOI_Object)
        
        saved_cards = []
        for card in SavedCardQS:
            serializer = SavedCardSerializer(card).data
            saved_cards.append(serializer)
        
        return Response(saved_cards,status=HTTP_200_OK)
            
        
         
      
class RecordPayment(APIView):
    def post(self,request):
        user = request.user
        UOI_Object_Requestor = UserOtherInfo.objects.get(user=user.id)
        data = request.data
        print("<-----------------------------Record Payemnt Incoming Data-------------->",data)
        print("<----------------------------Record Payment Incoming User----------------->",user)
        print("<---------------------------Record User Other Info object fetched----------->",UOI_Object_Requestor)
        incoming_booking_ID     = data['booking_id']
        BookingObject  = NewBookingModel.objects.get(booking_id__exact = booking_ID)
        payment_method = data['payment_method']
        if payment_method == "Card":
                
            credit_card_number = data['credit_card_number']
            paymentCard = BankingInfo.objects.get(credit_card_number = credit_card_number)
            service    = data['service_ID']
            print("<-------------------Service ID---------------->",service)
            serviceObject = Service.objects.get(id=service)
            print("<--------------------Service Object------------->",serviceObject)
            UserObject = User.objects.get(id=serviceObject.user)
            UOI_Object_Provider = UserOtherInfo.objects.get(user=UserObject)
            LivePaymentsObject = LivePayments(
                payment_card   = paymentCard,
                payment_method = payment_method,
                payment_request_date =  timezone.now,
                payment_request_time =  timezone.now,
                payment_from         =  UOI_Object_Requestor,
                payment_to      =   UOI_Object_Provider,
                booking_ID      =   incoming_booking_ID
                )
            LivePaymentsObject.save()
            return Response({"msg":"Payment request recorded successfully","status":"PAYMENT_REQUEST_RECORDED"},status=HTTP_200_OK)
        else:
  
            service   = data['service_ID']
            serviceObject  =    Service.objects.get(id=service)
            UserObject     =    User.objects.get(id=serviceObject.user)
            UOI_Object_Provider = UserOtherInfo.objects.get(user=UserObject)
            LivePaymentsObject  = LivePayments(
                payment_card    =   paymentCard,
                payment_method  =   payment_method,
                payment_request_date = timezone.now,
                payment_request_time = timezone.now,
                payment_from    =  UOI_Object_Requestor,
                payment_to      = UOI_Object_Provider,
                booking_ID      =   incoming_booking_ID
                )
            LivePaymentsObject.save()
            return Response({"msg":"Payment request recorded successfully","status":"PAYMENT_REQUEST_RECORDED"},status=HTTP_200_OK)
#             
           

class MarkReviewForModeration(APIView):
    def post(self,request):
        user = request.user
        data = request.data
        print("<-------------------Incoming Request Data---------------------------->",data)
        service_feedback_id = data['feedback_id']
        ServiceFeedbackObject = ServiceFeedback.objects.get(id=service_feedback_id)
        ServiceFeedbackObject.marked_for_moderation = True
        ServiceFeedbackObject.save()
        return Response({"msg":"Feedback marked for moderation","status":"FEDBAK_FOR_MOD"},status=HTTP_200_OK)
    




class FetchLegalText(APIView):
    def get(self,request):
        ContentQs  = ContentMaster.objects.all()
        print("<----------------------CONTENT DATA------------------>",ContentQs)

        text_list = {
            "TC":"",
            "Privacy":"",
            "Community":""
        }
        for text in ContentQs:
            serializer = LegalTextSerializer(text).data
            title = serializer['title']
            if title == "Terms and Conditions":
                text_list['TC'] = serializer['legal_text']
            elif title == "Privacy Policy":
                text_list['Privacy'] = serializer['legal_text']
            elif title == "Community Guidelines":
                text_list['Community'] = serializer['legal_text']
            else:
                print("<--------------Content Output---------------->",serializer['content'])
#             text_list.append(serializer)
        return Response(text_list,status=HTTP_200_OK)
    
    



class TestServices(APIView):
    def get(self,request):
        ServiceQS = Service.objects.all()
        url_param = request.GET.get("val")
        print("<-----------------All Service QS--------------->",ServiceQS)
        print("<------------------URL Param Type--------------->",type(url_param))
        url_param = int(url_param)
        RetreivedService = ServiceQS[url_param]
        print("<-----------------Retreived Service----------------->",RetreivedService)
        serializedService = ServiceSerializer(RetreivedService).data
        request.session['my_qs'] = serializedService
        return Response({"msg":"Stored value in Session"},status=HTTP_200_OK)


class FetchSession(APIView):
    def get(self,request):
        session_val = request.session['my_qs']
        print("<----------------Session Value retrieved--------------------->",session_val)
        return Response(status=HTTP_200_OK)
        




class MarkCashCollectedByProvider(APIView):
    def put(self,request):
        user = request.user
        data = request.data
        booking_id = data['booking_id']
        LivePaymentsObject = LivePayments.objects.get(booking_ID__exact = booking_id)
        LivePaymentsObject.cash_collected_by_provider = True
        LivePaymentsObject.save()
        return Response({"msg":"Cash collected by Provider"},status=HTTP_200_OK)



class MarkCashPaidByRequestor(APIView):
    def put(self,request):
        user = request.user
        data = request.data
        booking_id = data['booking_id']
        LivePaymentsObject = LivePayments.objects.get(booking_ID__exact = booking_id)
        LivePaymentsObject.cash_paid_by_requestor = True
        LivePaymentsObject.save()
        return Response({"msg":"Cash paid to Provider"},status=HTTP_200_OK)


        
        
        


class FetchQuestionsForProvider(APIView):
    def put(self,request):
        lang = request.GET.get('lang')




        user = request.user
        data = request.data
#         service_id = data['service_id']
#         ServiceObject = ServiceList.objects.get(id=service_id)
        subcategory_id = data['subcategory_id']
        subcategory_object = SubCategory.objects.get(id=subcategory_id)
        
        common_question_qs = QuestionFilledByAdmin.objects.filter(SubCategory = subcategory_object)
#         service_question_qs = QuestionFilledByAdmin.objects.filter(service = ServiceObject)
        
#         final_question_qs = common_question_qs.union(service_question_qs)
        
        if lang == "en":
            questions_serialized = question_for_provider_serialzer(common_question_qs,many=True).data
        elif lang == "ar":
            questions_serialized = question_for_provider_serializer_arabic(common_question_qs,many=True).data
        else:
            return Response({"msg":"Invalid language code"},status=HTTP_400_BAD_REQUEST)

        print(questions_serialized)
        return Response(questions_serialized,status=HTTP_200_OK)
        
        

class FetchQuestionsForRequestor(APIView):
    def put(self,request):

        lang = request.GET.get('lang')
        user = request.user
        data = request.data
        subcategory_id = data['subcategory_id']

        subcategory_object = SubCategory.objects.get(id=subcategory_id)

        common_question_qs = QuestionFilledByAdmin.objects.filter(SubCategory = subcategory_object)
        if lang == "en":
            questions_serialized = question_for_requestor_serialzer(common_question_qs,many=True).data
        elif lang == "ar":
            questions_serialized = question_for_requestor_serializer_arabic(common_question_qs,many=True).data            
        else:
            return Response({"msg":"Invalid language code"},status=HTTP_400_BAD_REQUEST)
        
        return Response(questions_serialized,status=HTTP_200_OK)
        
        




class ManageBookingProDetails(APIView):
    def put(self,request):
        
        data = request.data
        provider_id = data['provider_id']
        
        ProviderObject = UserOtherInfo.objects.get(id=provider_id)
        serializer = UserOtherInfoSerializer(ProviderObject).data
        return Response(serializer,status=HTTP_200_OK)


        


class PopulateDBNew(APIView):
    def put(self,request):

        data = request.data

        # <=============================CREATING CATEGORIES===========================>
    

        
        LessonsCategoryObject = Category(
            category = "Lessons"
            )
        LessonsCategoryObject.save()

        HomeRepairCategoryObject = Category(
            category = "Home Maintenance and Family"
        )
        HomeRepairCategoryObject.save()

        BeautyAndFashionCategoryObj = Category(
            category = "Beauty and Fashion"
        )
        BeautyAndFashionCategoryObj.save()

        EventsAndCateringObj  = Category(
            category = "Events and Catering"
        )
        EventsAndCateringObj.save()


        ProfessionalServicesCategoryObj = Category(
            category = "Professional Services"
        )
        ProfessionalServicesCategoryObj.save()


        WellnessCategoryObj = Category(
            category = "Wellness"
        )
        WellnessCategoryObj.save()
        
        
        



        TCObject = ContentMaster(
            title = "Terms and Conditions",
            legal_text = "Terms and Conditions for Company Name Introduction These Website Standard Terms and Conditions written on this webpage shall manage your use of our website, Webiste Name accessible at Website.com. These Terms will be applied fully and affect to your use of this Website. By using this Website, you agreed to accept all terms and conditions written in here. You must not use this Website if you disagree with any of these Website Standard Terms and Conditions. Minors or people below 18 years old are not allowed to use this Website. Intellectual Property Rights Other than the content you own, under these Terms, Company Name and/or its licensors own all the intellectual property rights and materials contained in this Website. You are granted limited license only for purposes of viewing the material contained on this Website. Restrictions You are specifically restricted from all of the following: publishing any Website material in any other media; selling, sublicensing and/or otherwise commercializing any Website material; publicly performing and/or showing any Website material; using this Website in any way that is or may be damaging to this Website; using this Website in any way that impacts user access to this Website; using this Website contrary to applicable laws and regulations, or in any way may cause harm to the Website, or to any person or business entity; engaging in any data mining, data harvesting, data extracting or any other similar activity in relation to this Website; using this Website to engage in any advertising or marketing. Certain areas of this Website are restricted from being access by you and Company Name may further restrict access by you to any areas of this Website, at any time, in absolute discretion. Any user ID and password you may have for this Website are confidential and you must maintain confidentiality as well. Your Content In these Website Standard Terms and Conditions, “Your Content” shall mean any audio, video text, images or other material you choose to display on this Website. By displaying Your Content, you grant Company Name a non-exclusive, worldwide irrevocable, sub licensable license to use, reproduce, adapt, publish, translate and distribute it in any and all media. Your Content must be your own and must not be invading any third-party's rights. Company Name reserves the right to remove any of Your Content from this Website at any time without notice. No warranties This Website is provided “as is,” with all faults, and Company Name express no representations or warranties, of any kind related to this Website or the materials contained on this Website. Also, nothing contained on this Website shall be interpreted as advising you. Limitation of liability In no event shall Company Name, nor any of its officers, directors and employees, shall be held liable for anything arising out of or in any way connected with your use of this Website whether such liability is under contract.  Company Name, including its officers, directors and employees shall not be held liable for any indirect, consequential or special liability arising out of or in any way related to your use of this Website. Indemnification You hereby indemnify to the fullest extent Company Name from and against any and/or all liabilities, costs, demands, causes of action, damages and expenses arising in any way related to your breach of any of the provisions of these Terms. Severability If any provision of these Terms is found to be invalid under any applicable law, such provisions shall be deleted without affecting the remaining provisions herein. Variation of Terms Company Name is permitted to revise these Terms at any time as it sees fit, and by using this Website you are expected to review these Terms on a regular basis. Assignment The Company Name is allowed to assign, transfer, and subcontract its rights and/or obligations under these Terms without any notification. However, you are not allowed to assign, transfer, or subcontract any of your rights and/or obligations under these Terms. Entire Agreement These Terms constitute the entire agreement between Company Name and you in relation to your use of this Website, and supersede all prior agreements and understandings. Governing Law & Jurisdiction These Terms will be governed by and interpreted in accordance with the laws of the State of Country, and you submit to the non-exclusive jurisdiction of the state and federal courts located in Country for the resolution of any disputes."
            
        )
        TCObject.save()

        PrivacyObject = ContentMaster(
            title = "Privacy Policy",
            legal_text = "Privacy Policy for Company Name At Website Name, accessible at Website.com, one of our main priorities is the privacy of our visitors. This Privacy Policy document contains types of information that is collected and recorded by Website Name and how we use it. If you have additional questions or require more information about our Privacy Policy, do not hesitate to contact us through email at Email@Website.com Log Files Website Name follows a standard procedure of using log files. These files log visitors when they visit websites. All hosting companies do this and a part of hosting services' analytics. The information collected by log files include internet protocol (IP) addresses, browser type, Internet Service Provider (ISP), date and time stamp, referring/exit pages, and possibly the number of clicks. These are not linked to any information that is personally identifiable. The purpose of the information is for analyzing trends, administering the site, tracking users' movement on the website, and gathering demographic information. Cookies and Web Beacons Like any other website, Website Name uses ‘cookies'. These cookies are used to store information including visitors' preferences, and the pages on the website that the visitor accessed or visited. The information is used to optimize the users' experience by customizing our web page content based on visitors' browser type and/or other information. DoubleClick DART Cookie Google is one of a third-party vendor on our site. It also uses cookies, known as DART cookies, to serve ads to our site visitors based upon their visit to www.website.com and other sites on the internet. However, visitors may choose to decline the use of DART cookies by visiting the Google ad and content network Privacy Policy. Some of advertisers on our site may use cookies and web beacons. Our advertising partners are listed below. Each of our advertising partners has their own Privacy Policy for their policies on user data. For easier access, we hyperlinked to their Privacy Policies below. Google Privacy Policies You may consult this list to find the Privacy Policy for each of the advertising partners of Website Name. Third-party ad servers or ad networks uses technologies like cookies, JavaScript, or Web Beacons that are used in their respective advertisements and links that appear on Website Name, which are sent directly to users' browser. They automatically receive your IP address when this occurs. These technologies are used to measure the effectiveness of their advertising campaigns and/or to personalize the advertising content that you see on websites that you visit. Note that Website Name has no access to or control over these cookies that are used by third-party advertisers. Third Part Privacy Policies Website Name's Privacy Policy does not apply to other advertisers or websites. Thus, we are advising you to consult the respective Privacy Policies of these third-party ad servers for more detailed information. It may include their practices and instructions about how to opt-out of certain options. You may find a complete list of these Privacy Policies and their links here: Privacy Policy Links. You can choose to disable cookies through your individual browser options. To know more detailed information about cookie management with specific web browsers, it can be found at the browsers' respective websites. What Are Cookies? Children's Information Another part of our priority is adding protection for children while using the internet. We encourage parents and guardians to observe, participate in, and/or monitor and guide their online activity. Website Name does not knowingly collect any Personal Identifiable Information from children under the age of 13. If you think that your child provided this kind of information on our website, we strongly encourage you to contact us immediately and we will do our best efforts to promptly remove such information from our records. Online Privacy Policy Only This privacy policy applies only to our online activities and is valid for visitors to our website with regards to the information that they shared and/or collect in Website Name. This policy is not applicable to any information collected offline or via channels other than this website. Consent By using our website, you hereby consent to our Privacy Policy and agree to its Terms and Conditions."
    
        )
        PrivacyObject.save()

        CommunityObject = ContentMaster(
            title = "Community Guidelines",
            legal_text = "Community Guidelines WELCOME TO POLYGON! Here on Polygon, you'll find a vibrant community of gamers, enthusiasts and smart, knowledgeable people. As always, our goal is to foster conversations that are insightful, helpful, and most of all, fun. In order to do this we need your help, so here are some guidelines to get your started! THE SHORT VERSION Don't be rude, don't call people names, or respond to trolls. We'll remove any bad stuff when we see it, which will unfortunately include any nicer comments made in response. Respect and help the moderators not by replying to bad comments, but by flagging bad comments. It's a small team of dedicated, caring robots humans working hard to make things better. Got a correction or suggestion for an article? Use the contact page to let us know. It's quicker and we'll heart you for that rather than derailing a thread. OUR WAY OR THE (INTERNET SUPER) HIGHWAY Here's a list of things that will get your comment or forum post removed, and might get your account banned. Remember that this is not a comprehensive list and our moderators reserve the right to remove anything we deem inappropriate and that skirts the boundaries of good taste. See any of the stuff below? You can help us out by flagging (more on that below). Spam: Zero tolerance, of course! If it comes from a human or a robot, spam will be deleted. This includes self-promotion. Generally speaking, promoting your games, projects, YouTube channel, website or copy pasting entire articles/scans from other sites/magazines will be treated like any other spam on Polygon. It goes in the bin. Personal attacks: Don't attack or insult another user. It's not helpful and it doesn't make Polygon a friendly place. This includes referring to other people as trolls, fanboys, sheep, white knights, etc. If you're thinking of using a specific term such as a racial or derogatory insult, think again about why that's a bad idea, and don't do it. Illegal activities: If you post links to illegal downloads, ways to steal service, describe how to perform unauthorized hacks and exploits, or any other nefarious activity, then it's game over for you, kid. NSFW material: Nope, not allowed. Even images or links that could be considered borderline are not acceptable. A good rule of thumb is that anything beyond PG-13 will get you in trouble, but we reserve the right to remove any post we deem offensive. This goes for pornographic material, vile language, gore and generally gross stuff. Racism, sexism, and other discrimination: Attacking entire classes of people is just like attacking a single person: we'll be having words with you about it. Trolling: If you're making off-topic comments, taking threads off-topic, or posting flamebait, you're likely to find that your post has suddenly disappeared. An example of that would be spelling company names using dollar signs such as or wordplay like It could also be going off topic on what constitutes a good review score, or bringing up other review scores in an unrelated review to make an off-topic point. Offensive usernames: If your username contains language or terms that could be construed as offensive, we'll put a hold on your account and start a dialogue with you to change your username to something more appropriate. If you provide unsuitable replacements, we reserve the right to choose a new username at random in order to get you up and running on a temporary basis until you provide a more permanent option. Multiple accounts and throwaway emails: We don't allow multiple accounts per user. Using a disposable email address signals to us that you're not here for the right reasons and we'll go ahead and block those, and offer to open a dialogue with you when you get in touch using a legitimate email account. You also may not create accounts designed to impersonate another person. Cross posting: Don't make duplicate posts across different forums — it clogs things up and fractures the conversation Complaining about coverage: We cover a wide array of topics, not all of which are easy, comfortable, or reflective of your personal views and may touch on issues normally considered  of gaming such as feminism, sexual assault or religious beliefs. While we're not against discussions of our coverage, comments containing plainly stated accusations of bias, complaints about the frequency of articles on a topic, and complaints about whether something is newsworthy are usually an indication that you're not trying to be a productive member of the community. We'll have words and remove posts to get conversation back on track. This also applies to review scores. Complaining about moderation: See  below. Site bashing: Whether it's Polygon, or another website - don't bash them or their staff. It's not cool and it's disrespectful to a lot of people. Be the better person here, please. Posting unmarked spoilers: We have a spoiler tag in the text editor for when you make your comment. Use it! Posting unmarked spoilers will usually get your comment removed. Generally speaking, anything older than 12 months of its U.S. release is considered fair game. Abuse of the flag system: If we catch you flagging comments that have no business being flagged because you disagree on semantics, we will have words with you. rule: All of the behavior listed above? You could say we're not fond of it. We're even less likely to tolerate it if you made an account on Polygon specifically to engage in it, since it tells us that you aren't here to contribute in any meaningful manner. If your first post breaks the rules above, we'll usually go ahead and issue a ban and open a dialogue."
        )
        CommunityObject.save()


        # <=============================CREATING CATEGORIES ENDS HERE===========================>        




        # <=============================CREATING SUB-CATEGORIES===========================>



        LessonsSubObj = SubCategory(
            category = LessonsCategoryObject,
            subcategory = "Academic"
            )
        LessonsSubObj.save()
        
        LessonsSubObj = SubCategory(
            category = LessonsCategoryObject,
            subcategory = "Languages"
            )
        LessonsSubObj.save()
        
        LessonsSubObj = SubCategory(
            category = LessonsCategoryObject,
            subcategory = "Music"
            )
        LessonsSubObj.save()
        
        LessonsSubObj = SubCategory(
            category = LessonsCategoryObject,
            subcategory = "Dance"
            )
        LessonsSubObj.save()
        
        
        
        
        HomeMaintainSubObj = SubCategory(
            category = HomeRepairCategoryObject,
            subcategory = "Maintenance"
            )
        HomeMaintainSubObj.save()

        HomeMaintainSubObj = SubCategory(
            category = HomeRepairCategoryObject,
            subcategory = "Family"
            )
        HomeMaintainSubObj.save()

        
        BeautyAndFashionSubObj = SubCategory(
            category = BeautyAndFashionCategoryObj,
            subcategory = "Beauty"
            )
        BeautyAndFashionSubObj.save()

        BeautyAndFashionSubObj = SubCategory(
            category = BeautyAndFashionCategoryObj,
            subcategory = "Fashion"
            )
        BeautyAndFashionSubObj.save()
        
        
        EventsSubObj = SubCategory(
            category = EventsAndCateringObj,
            subcategory = "Event Planning"
            )
        EventsSubObj.save()

        EventsSubObj = SubCategory(
            category = EventsAndCateringObj,
            subcategory = "Event Entertainment"
            )
        EventsSubObj.save()
        
        
        
        ProfessionalServiceSubObj = SubCategory(
            category = ProfessionalServicesCategoryObj,
            subcategory = "Software Development"
            )
        ProfessionalServiceSubObj.save()

        ProfessionalServiceSubObj = SubCategory(
            category = ProfessionalServicesCategoryObj,
            subcategory = "Graphic and Design"
            )
        ProfessionalServiceSubObj.save()

        ProfessionalServiceSubObj = SubCategory(
            category = ProfessionalServicesCategoryObj,
            subcategory = "Business"
            )
        ProfessionalServiceSubObj.save()
        
        
        
        WellnessSubObj = SubCategory(
            
            category = WellnessCategoryObj,
            subcategory = "Fitness"
            )
        WellnessSubObj.save()


        WellnessSubObj = SubCategory(
            
            category = WellnessCategoryObj,
            subcategory = "Coaching"
            )
        WellnessSubObj.save()

        WellnessSubObj = SubCategory(
            
            category = WellnessCategoryObj,
            subcategory = "Diet"
            )
        WellnessSubObj.save()
        




        # <=============================CREATING SUB-CATEGORIES ENDS HERE===========================>


        # <=============================CREATING USERS==============================================>

        if 'users' in data:
            if data['users'] == True:

                AbhishekRanaUser        = User(
                    username            =   "abhishekrana@gmail.com+918375856324",
                    first_name          =   "Abhishek",
                    last_name           =   "Rana",
                    email               =   "abhishekrana@gmail.com"
                    )
                AbhishekRanaUser.save()

                AbhishekRanaUser.set_password("test@1234")

                AbhishekRanaUOI         =   UserOtherInfo(
                    user                =   AbhishekRanaUser,
                    phone               =   "+918375856324",
                    usertype            =   "requester",
                    user_address        =   "Alpha Road, Block A, Alpha I, Greater Noida, Uttar Pradesh, India",
                    user_address_lat    =   "28.4693600000",
                    user_address_long   =   "77.5094800000",
                    is_phone_verified   =   True,
                    profile_image_s3    =   "https://meenfee.s3.amazonaws.com/public%2FAvtar1566387004785.png",
                    locality            =   "Alpha Road",
                    current_language    =   "English"
                )
                AbhishekRanaUOI.save()


                AmitabhGuptaUser        =   User(
                    username            =   "amitabhgupta@gmail.com+919811406552",
                    first_name          =   "Amitabh",
                    last_name           =   "Gupta",
                    email               =   "amitabhgupta@gmail.com"
                    )
                AmitabhGuptaUser.save()

                AmitabhGuptaUser.set_password("test@1234")

                AmitabhGuptaUserUOI     =   UserOtherInfo(
                    user                =   AmitabhGuptaUser,
                    phone               =   "+919811406552",
                    usertype            =   "requester",
                    user_address        =   "Surajpur Kasna Road, Block B, Phi III, Greater Noida, Uttar Pradesh, India",
                    user_address_lat    =   "28.4564100000",
                    user_address_long   =   "77.5225600000",
                    is_phone_verified   =   True,
                    profile_image_s3    =   "https://meenfee.s3.amazonaws.com/public%2FAvtar1566386873772.png",
                    locality            =   "Surajpur Kasna Road",
                    current_language    =   "English"
                )
                AmitabhGuptaUserUOI.save()



                PrabhasSreekumarUser        =   User(
                    username            =   "prabhas@gmail.com+918375865235",
                    first_name          =   "Prabhas",
                    last_name           =   "Sreekumar",
                    email               =   "prabhas@gmail.com"
                    )
                PrabhasSreekumarUser.save()

                PrabhasSreekumarUser.set_password("test@1234")

                PrabhasSreekumarUOI     =   UserOtherInfo(
                    user                =   PrabhasSreekumarUser,
                    phone               =   "+918375865235",
                    usertype            =   "requester",
                    user_address        =   "Kasna Village, Greater Noida, Uttar Pradesh, India",
                    user_address_lat    =   "28.4367600000",
                    user_address_long   =   "77.5375800000",
                    is_phone_verified   =   True,
                    profile_image_s3    =   "https://meenfee.s3.amazonaws.com/public%2FAvtar1566387273873.png",
                    locality            =   "Kasna Village",
                    current_language    =   "English"
                )
                PrabhasSreekumarUOI.save()





                DeeptiDhyaniUser        =   User(
                    username            =   "deepti@gmail.com+918375896421",
                    first_name          =   "Deepti",
                    last_name           =   "Dhyani",
                    email               =   "deepti@gmail.com"
                    )
                DeeptiDhyaniUser.save()

                DeeptiDhyaniUser.set_password("test@1234")

                DeeptiDhyaniUOI         =   UserOtherInfo(
                    user                =   DeeptiDhyaniUser,
                    phone               =   "+918375896421",
                    usertype            =   "requester",
                    user_address        =   "Segovia, Spain",
                    user_address_lat    =   "40.9429000000",
                    user_address_long   =   "-4.1088100000",
                    is_phone_verified   =   True,
                    profile_image_s3    =   "https://meenfee.s3.amazonaws.com/public%2FAvtar1566387524823.png",
                    locality            =   "Segovia",
                    current_language    =   "English"
                )
                DeeptiDhyaniUOI.save()





                NishaGoelUser        =   User(
                    username            =   "nishagoel@gmail.com+918375845632",
                    first_name          =   "Nisha",
                    last_name           =   "Goel",
                    email               =   "nishagoel@gmail.com"
                    )
                NishaGoelUser.save()

                NishaGoelUser.set_password("test@1234")

                NishaGoelUOI         =   UserOtherInfo(
                    user                =   NishaGoelUser,
                    phone               =   "+918375845632",
                    usertype            =   "requester",
                    user_address        =   "Cupertino Road, Cupertino, CA, USA",
                    user_address_lat    =   "37.3231000000",
                    user_address_long   =   "-122.0650900000",
                    is_phone_verified   =   True,
                    profile_image_s3    =   "https://meenfee.s3.amazonaws.com/public%2FAvtar1566387645872.png",
                    locality            =   "Cupertino Road",
                    current_language    =   "English"
                )
                NishaGoelUOI.save()





                RohitAggarwalUser        =   User(
                    username            =   "rohitaggarwal@gmail.com+919811056322",
                    first_name          =   "Rohit",
                    last_name           =   "Aggarwal",
                    email               =   "rohitaggarwal@gmail.com"
                    )
                RohitAggarwalUser.save()

                RohitAggarwalUser.set_password("test@1234")

                RohitAggarwalUOI                =   UserOtherInfo(
                    user                    =   RohitAggarwalUser,
                    phone                   =   "+919811056322",
                    idcard                  =   "100020003004000abcde",
                    usertype                =   "provider",
                    user_address            =   "Pitampura Road, AP Block, Block AD, Dakshini Pitampura, Pitam Pura, Delhi, India",
                    user_address_lat        =   "28.7075900000",
                    user_address_long       =   "77.1367000000",
                    is_phone_verified       =   True,
                    profile_image_s3        =   "https://meenfee.s3.amazonaws.com/public%2FAvtar1566381089600.png",
                    locality                =   "Pitampura Road",
                    current_language        =   "English",
                    switched_to_provider    =   True

                )
                RohitAggarwalUOI.save()




                RohanSharmaUser         =   User(
                    username            =   "rohansharma@gmail.com+919811096552",
                    first_name          =   "Rohan",
                    last_name           =   "Sharma",
                    email               =   "rohansharma@gmail.com"
                    )
                RohanSharmaUser.save()

                RohanSharmaUser.set_password("test@1234")

                RohanSharmaUOI            =   UserOtherInfo(
                    user                    =   RohanSharmaUser,
                    phone                   =   "+919811096552",
                    idcard                  =   "100020030004000abcds",
                    usertype                =   "provider",
                    user_address            =   "Janakpuri West, Janakpuri District Center, Janakpuri, Delhi, India",
                    user_address_lat        =   "28.6296800000",
                    user_address_long       =   "77.0796500000",
                    is_phone_verified       =   True,
                    profile_image_s3        =   "https://meenfee.s3.amazonaws.com/public%2FAvtar1566382042033.png",
                    locality                =   "Janakpuri West",
                    current_language        =   "English",
                    switched_to_provider    =   True

                )
                RohanSharmaUOI.save()



                SartajSinghUser         =   User(
                    username            =   "sartajsingh@gmail.com+919811589665",
                    first_name          =   "Sartaj",
                    last_name           =   "Singh",
                    email               =   "sartajsingh@gmail.com"
                    )
                SartajSinghUser.save()

                SartajSinghUser.set_password("test@1234")

                SartajSingUOI            =   UserOtherInfo(
                    user                    =   SartajSinghUser,
                    phone                   =   "+919811589665",
                    idcard                  =   "1000200030004000abcd",
                    usertype                =   "provider",
                    user_address            =   "Gopalmath, Durgapur, West Bengal, India",
                    user_address_lat        =   "23.5750600000",
                    user_address_long       =   "87.2294900000",
                    is_phone_verified       =   True,
                    profile_image_s3        =   "https://meenfee.s3.amazonaws.com/public%2FAvtar1566383111289.png",
                    locality                =   "Gopalmath",
                    current_language        =   "English",
                    switched_to_provider    =   True

                )
                SartajSingUOI.save()



                ShwethaSharmaUser         =   User(
                    username            =   "shwethasharma@gmail.com+919811408551",
                    first_name          =   "Shwetha",
                    last_name           =   "Sharma",
                    email               =   "shwethasharma@gmail.com"
                    )
                ShwethaSharmaUser.save()

                ShwethaSharmaUser.set_password("test@1234")

                ShwethaSharmaUOI            =   UserOtherInfo(
                    user                    =   ShwethaSharmaUser,
                    phone                   =   "+919811408551",
                    idcard                  =   "10020003004000abcded",
                    usertype                =   "provider",
                    user_address            =   "Kartarpur, Punjab, India",
                    user_address_lat        =   "31.4358200000",
                    user_address_long       =   "75.5009400000",
                    is_phone_verified       =   True,
                    profile_image_s3        =   "https://meenfee.s3.amazonaws.com/public%2FAvtar1566383573721.png",
                    locality                =   "Kartarpur",
                    current_language        =   "English",
                    switched_to_provider    =   True

                )
                ShwethaSharmaUOI.save()



                AnushkaRaiUser         =   User(
                    username            =   "anushkarai@gmail.com+918378965234",
                    first_name          =   "Anushka",
                    last_name           =   "Rai",
                    email               =   "anushkarai@gmail.com"
                    )
                AnushkaRaiUser.save()

                AnushkaRaiUser.set_password("test@1234")

                AnushkaRaiUOI            =   UserOtherInfo(
                    user                    =   AnushkaRaiUser,
                    phone                   =   "+918378965234",
                    idcard                  =   "1000200030004000500a",
                    usertype                =   "provider",
                    user_address            =   "Mayur Vihar Phase 1 Extension, Mayur Vihar, New Delhi, Delhi, India",
                    user_address_lat        =   "28.6005100000",
                    user_address_long       =   "77.2936700000",
                    is_phone_verified       =   True,
                    profile_image_s3        =   "https://meenfee.s3.amazonaws.com/public%2FAvtar1566385097327.png",
                    locality                =   "Mayur Vihar Phase 1 Extension, Mayur Vihar",
                    current_language        =   "English",
                    switched_to_provider    =   True

                )
                AnushkaRaiUOI.save()




        # <============================CREATING USERS END===========================================>



        # <=============================CREATING HELP AND SUPPORT===========================>
        
        HelpObject = HelpAndSupport(
            contactaddress = "Third Floor, City Mall,King Abdulla II Street, Amman, Jordan",
            contactnumber = "+96212345678",
            email = "support@meenfee.com",
            website = "www.meenfee.com/support"
            )
        HelpObject.save()        
        
        
        # <=============================CREATING HELP AND SUPPORT ENDS HERE===========================>        
        

        # <=============================CREATING QUESTIONS===========================>

        SubcategoryQS  = SubCategory.objects.all()

        for subcategory in SubcategoryQS:
            
            category_object = subcategory.category





            PointofServiceQuesObj   =   QuestionFilledByAdmin(
                Question_name           =   "Point of Service",
                SubCategory             =    subcategory,
                question_for_provider   = "Where do you prefer to provide Service ?",
                question_for_requestor  = "Where do you prefer to avail the Service ?",
                category   = category_object
            )
            PointofServiceQuesObj.save()
            print("<------------------Point of Service Object--------->",PointofServiceQuesObj)
            PointofServiceOption = OptionsFilledbyAdmin(
                question = PointofServiceQuesObj,
                Option1  = "At service provider's place"
                )
            PointofServiceOption.save()
            
            PointofServiceOption = OptionsFilledbyAdmin(
                question = PointofServiceQuesObj,
                Option1  = "At service requestor's place"
                )
            PointofServiceOption.save()

            PointofServiceOption = OptionsFilledbyAdmin(
                question = PointofServiceQuesObj,
                Option1  = "Remotely"
                )
            PointofServiceOption.save()





            DistanceOfTravelQuesObj   =   QuestionFilledByAdmin(
                Question_name           =   "Distance of Travel",
                SubCategory             =    subcategory,
                question_for_provider   = "How far are you willing to travel to provide the service ?",
                question_for_requestor  = "How far are you willing to travel to seek service ?",
                category   = category_object
            )
            DistanceOfTravelQuesObj.save()
            
            DistanceOfTravelOption = OptionsFilledbyAdmin(
                question = DistanceOfTravelQuesObj,
                Option1  = "5 KM away"
                )
            DistanceOfTravelOption.save()
            
            DistanceOfTravelOption = OptionsFilledbyAdmin(
                question = DistanceOfTravelQuesObj,
                Option1  = "10 KM away"
                )
            DistanceOfTravelOption.save()

            DistanceOfTravelOption = OptionsFilledbyAdmin(
                question = DistanceOfTravelQuesObj,
                Option1  = "20 KM away"
                )
            DistanceOfTravelOption.save()
            







            ModeOfContactQuesObj   =   QuestionFilledByAdmin(
                Question_name           =   "Mode of Contact",
                SubCategory             =    subcategory,
                question_for_provider   = "Where would you like requestor to contact you ?",
                question_for_requestor  = "How would you like to contact service provider ?",
                category   = category_object
            )
            ModeOfContactQuesObj.save()
            
            
            ModeOfContactOption = OptionsFilledbyAdmin(
                question = ModeOfContactQuesObj,
                Option1  = "Email"
                )
            ModeOfContactOption.save()
            
            ModeOfContactOption = OptionsFilledbyAdmin(
                question = ModeOfContactQuesObj,
                Option1  = "Phone"
                )
            ModeOfContactOption.save()

            ModeOfContactOption = OptionsFilledbyAdmin(
                question = ModeOfContactQuesObj,
                Option1  = "SMS"
                )
            ModeOfContactOption.save()


            YearsOfExpQuesObj   =   QuestionFilledByAdmin(
                Question_name           =   "Years of Experience",
                SubCategory             =    subcategory,
                question_for_provider   = "How many years of experience do you have ?",
                question_for_requestor  = "How much experienced provider are you seeking ?",
                category   = category_object
            )
            YearsOfExpQuesObj.save()
            
            YearsOfExpOption = OptionsFilledbyAdmin(
                question = YearsOfExpQuesObj,
                Option1  = "0-3 Years (Beginner)"
                )
            YearsOfExpOption.save()
            
            YearsOfExpOption = OptionsFilledbyAdmin(
                question = YearsOfExpQuesObj,
                Option1  = "3-7 Years (Medium)"
                )
            YearsOfExpOption.save()

            YearsOfExpOption = OptionsFilledbyAdmin(
                question = YearsOfExpQuesObj,
                Option1  = "7+ Years (Expert)"
                )
            YearsOfExpOption.save()
            
            
            
            if category_object == LessonsCategoryObject:
                PriceRateQuesObj   =   QuestionFilledByAdmin(
                    Question_name           =   "Price Rate",
                    SubCategory             =    subcategory,
                    question_for_provider   = "At what price rate do you provide service ?",
                    question_for_requestor  = "At what price rate are you willing to seek service ?",
                    category   = category_object
                )
                PriceRateQuesObj.save()
                
                PriceRateOption = OptionsFilledbyAdmin(
                    question = PriceRateQuesObj,
                    Option1  = "Per Hour"
                    )
                PriceRateOption.save()



            
            elif category_object == HomeRepairCategoryObject:
                
                PriceRateQuesObj   =   QuestionFilledByAdmin(
                    Question_name           =   "Price Rate",
                    SubCategory             =    subcategory,
                    question_for_provider   = "At what price rate do you provide service ?",
                    question_for_requestor  = "At what price rate are you willing to seek service ?",
                    category   = category_object
                )
                PriceRateQuesObj.save()
                
                PriceRateOption = OptionsFilledbyAdmin(
                    question = PriceRateQuesObj,
                    Option1  = "Per Hour"
                    )
                PriceRateOption.save()
                
                PriceRateOption = OptionsFilledbyAdmin(
                    question = PriceRateQuesObj,
                    Option1  = "Per Project"
                    )
                PriceRateOption.save()                  


            elif category_object == BeautyAndFashionCategoryObj:
                
                PriceRateQuesObj   =   QuestionFilledByAdmin(
                    Question_name           =   "Price Rate",
                    SubCategory             =    subcategory,
                    question_for_provider   = "At what price rate do you provide service ?",
                    question_for_requestor  = "At what price rate are you willing to seek service ?",
                    category   = category_object
                )
                PriceRateQuesObj.save()
                
                PriceRateOption = OptionsFilledbyAdmin(
                    question = PriceRateQuesObj,
                    Option1  = "Per Hour"
                    )
                PriceRateOption.save()
                
                PriceRateOption = OptionsFilledbyAdmin(
                    question = PriceRateQuesObj,
                    Option1  = "Per Project"
                    )
                PriceRateOption.save()      

            elif category_object == EventsAndCateringObj:
                
                PriceRateQuesObj   =   QuestionFilledByAdmin(
                    Question_name           =   "Price Rate",
                    SubCategory             =    subcategory,
                    question_for_provider   = "At what price rate do you provide service ?",
                    question_for_requestor  = "At what price rate are you willing to seek service ?",
                    category   = category_object
                )
                PriceRateQuesObj.save()
                
                PriceRateOption = OptionsFilledbyAdmin(
                    question = PriceRateQuesObj,
                    Option1  = "Per Hour"
                    )
                PriceRateOption.save()
                
                PriceRateOption = OptionsFilledbyAdmin(
                    question = PriceRateQuesObj,
                    Option1  = "Per Project"
                    )
                PriceRateOption.save()
                      
            elif category_object == ProfessionalServicesCategoryObj:
                
                PriceRateQuesObj   =   QuestionFilledByAdmin(
                    Question_name           =   "Price Rate",
                    SubCategory             =    subcategory,
                    question_for_provider   = "At what price rate do you provide service ?",
                    question_for_requestor  = "At what price rate are you willing to seek service ?",
                    category   = category_object
                )
                PriceRateQuesObj.save()
                
                PriceRateOption = OptionsFilledbyAdmin(
                    question = PriceRateQuesObj,
                    Option1  = "Per Hour"
                    )
                PriceRateOption.save()
                
                PriceRateOption = OptionsFilledbyAdmin(
                    question = PriceRateQuesObj,
                    Option1  = "Per Project"
                    )
                PriceRateOption.save()   


            elif category_object == WellnessCategoryObj:
                
                PriceRateQuesObj   =   QuestionFilledByAdmin(
                    Question_name           =   "Price Rate",
                    SubCategory             =    subcategory,
                    question_for_provider   = "At what price rate do you provide service ?",
                    question_for_requestor  = "At what price rate are you willing to seek service ?",
                    category   = category_object
                )
                PriceRateQuesObj.save()
                
                PriceRateOption = OptionsFilledbyAdmin(
                    question = PriceRateQuesObj,
                    Option1  = "Per Hour"
                    )
                PriceRateOption.save()
                
                PriceRateOption = OptionsFilledbyAdmin(
                    question = PriceRateQuesObj,
                    Option1  = "Per Project"
                    )
                PriceRateOption.save()   


            if 'users' in data:
                if data['users'] == True:
                    if 'services' in data:
                        if data['services'] == True:

                            if subcategory.subcategory == "Academic":

                                EnglishTutionServiceObject = Service(
                                    user            =   RohitAggarwalUser,
                                    service_name    =   "English Tution",
                                    category        =   subcategory.category,
                                    subcategory     =   subcategory,
                                    service_pricing =   500,
                                    pricing_timing_unit = "Per Hour",
                                    speciality          =   True,
                                    service_location    =   "Saket, New Delhi, Delhi, India",
                                    service_location_lat =  28.5221000000,
                                    service_location_long = 77.2101500000,
                                    locality               = "Saket"
                                )
                                EnglishTutionServiceObject.save()

                                EnglishTutionScheduleObject = ServiceSchedule(
                                    service             =   EnglishTutionServiceObject,
                                    day                 =   "Monday",
                                    checked             =   True,
                                    open_time           =   "07:00:00",
                                    close_time          =   "09:00:00"
                                )
                                EnglishTutionScheduleObject.save()


                                EnglishTutionScheduleObject = ServiceSchedule(
                                    service             =   EnglishTutionServiceObject,
                                    day                 =   "Monday",
                                    checked             =   True,
                                    open_time           =   "10:00:00",
                                    close_time          =   "12:00:00"
                                )
                                EnglishTutionScheduleObject.save()


                                EnglishTutionScheduleObject = ServiceSchedule(
                                    service             =   EnglishTutionServiceObject,
                                    day                 =   "Monday",
                                    checked             =   True,
                                    open_time           =   "15:00:00",
                                    close_time          =   "18:00:00"
                                )
                                EnglishTutionScheduleObject.save()

                                EnglishTutionImagesObject  = ServiceImage(
                                    service         =   EnglishTutionServiceObject,
                                    service_img_file_1_s3 = "https://meenfee.s3.amazonaws.com/public%2FEnglish+Tution1.png",
                                    service_img_file_2_s3 = "https://meenfee.s3.amazonaws.com/public%2FEnglish+Tution2.png",

                                    service_img_file = "https://meenfee.s3.amazonaws.com/public%2FEnglish+Tution1.png",
                                    service_img_file1 = "https://meenfee.s3.amazonaws.com/public%2FEnglish+Tution2.png"

                                )
                                EnglishTutionImagesObject.save()

                                EnglishTutionAnswerObject = AnswerByProvider(
                                    service     =   EnglishTutionServiceObject,
                                    user        =   RohitAggarwalUser,
                                    option_Selected = "At service requestor's place",
                                    question        =   PointofServiceQuesObj,
                                    user_name       =   "Rohit Aggarwal",
                                    service_name    =   "English Tution",
                                    question_string  =  "Where do you prefer to provide Service ?"
                                )
                                EnglishTutionAnswerObject.save()


                                EnglishTutionAnswerObject = AnswerByProvider(
                                    service     =   EnglishTutionServiceObject,
                                    user        =   RohitAggarwalUser,
                                    option_Selected = "10 KM away",
                                    question        =   DistanceOfTravelQuesObj,
                                    user_name       =   "Rohit Aggarwal",
                                    service_name    =   "English Tution",
                                    question_string  =  "How far are you willing to travel to provide the service ?"
                                )
                                EnglishTutionAnswerObject.save()

                                EnglishTutionAnswerObject = AnswerByProvider(
                                    service     =   EnglishTutionServiceObject,
                                    user        =   RohitAggarwalUser,
                                    option_Selected = "Phone",
                                    question        =   ModeOfContactQuesObj,
                                    user_name       =   "Rohit Aggarwal",
                                    service_name    =   "English Tution",
                                    question_string  =  "Where would you like requestor to contact you ?"
                                )
                                EnglishTutionAnswerObject.save()


                                EnglishTutionAnswerObject = AnswerByProvider(
                                    service     =   EnglishTutionServiceObject,
                                    user        =   RohitAggarwalUser,
                                    option_Selected = "3-7 Years (Medium)",
                                    question        =   YearsOfExpQuesObj,
                                    user_name       =   "Rohit Aggarwal",
                                    service_name    =   "English Tution",
                                    question_string  =  "How many years of experience do you have ?"
                                )
                                EnglishTutionAnswerObject.save()


                                EnglishTutionAnswerObject = AnswerByProvider(
                                    service     =   EnglishTutionServiceObject,
                                    user        =   RohitAggarwalUser,
                                    option_Selected = "Per Hour",
                                    question        =   PriceRateQuesObj,
                                    user_name       =   "Rohit Aggarwal",
                                    service_name    =   "English Tution",
                                    question_string  =  "At what price rate do you provide service ?"
                                )
                                EnglishTutionAnswerObject.save()

                            elif subcategory.subcategory == "Maintenance":

                                KitchenCleanServiceObject = Service(
                                    user            =   RohitAggarwalUser,
                                    service_name    =   "Kitchen Deep Cleaning",
                                    category        =   subcategory.category,
                                    subcategory     =   subcategory,
                                    service_pricing =   600,
                                    pricing_timing_unit = "Per Hour",
                                    speciality          =   False,
                                    service_location    =   "Haldwani, Uttarakhand, India",
                                    service_location_lat =  29.2182600000,
                                    service_location_long = 79.5129800000,
                                    locality               = "Haldwani"
                                )
                                KitchenCleanServiceObject.save()

                                KitchenCleanScheduleObject = ServiceSchedule(
                                    service             =   KitchenCleanServiceObject,
                                    day                 =   "Monday",
                                    checked             =   True,
                                    open_time           =   "19:00:00",
                                    close_time          =   "21:00:00"
                                )
                                KitchenCleanScheduleObject.save()


                                KitchenCleanScheduleObject = ServiceSchedule(
                                    service             =   KitchenCleanServiceObject,
                                    day                 =   "Tuesday",
                                    checked             =   True,
                                    open_time           =   "20:00:00",
                                    close_time          =   "22:00:00"
                                )
                                KitchenCleanScheduleObject.save()


                                KitchenCleanScheduleObject = ServiceSchedule(
                                    service             =   KitchenCleanServiceObject,
                                    day                 =   "Tuesday",
                                    checked             =   True,
                                    open_time           =   "14:00:00",
                                    close_time          =   "17:00:00"
                                )
                                KitchenCleanScheduleObject.save()




                                KitchenCleanImagesObject  = ServiceImage(
                                    service         =   KitchenCleanServiceObject,
                                    service_img_file_1_s3 = "https://meenfee.s3.amazonaws.com/public%2FKitchen+Deep+Cleaning1.png",


                                    service_img_file = "https://meenfee.s3.amazonaws.com/public%2FKitchen+Deep+Cleaning1.png",


                                )
                                KitchenCleanImagesObject.save()

                                KitchenCleanAnswerObject = AnswerByProvider(
                                    service     =   KitchenCleanServiceObject,
                                    user        =   RohitAggarwalUser,
                                    option_Selected = "At service requestor's place",
                                    question        =   PointofServiceQuesObj,
                                    user_name       =   "Rohit Aggarwal",
                                    service_name    =   "Kitchen Deep Cleaning",
                                    question_string  =  "Where do you prefer to provide Service ?"
                                )
                                KitchenCleanAnswerObject.save()


                                KitchenCleanAnswerObject = AnswerByProvider(
                                    service     =   KitchenCleanServiceObject,
                                    user        =   RohitAggarwalUser,
                                    option_Selected = "5 KM away",
                                    question        =   DistanceOfTravelQuesObj,
                                    user_name       =   "Rohit Aggarwal",
                                    service_name    =   "Kitchen Deep Cleaning",
                                    question_string  =  "How far are you willing to travel to provide the service ?"
                                )
                                KitchenCleanAnswerObject.save()

                                KitchenCleanAnswerObject = AnswerByProvider(
                                    service     =   KitchenCleanServiceObject,
                                    user        =   RohitAggarwalUser,
                                    option_Selected = "SMS",
                                    question        =   ModeOfContactQuesObj,
                                    user_name       =   "Rohit Aggarwal",
                                    service_name    =   "Kitchen Deep Cleaning",
                                    question_string  =  "Where would you like requestor to contact you ?"
                                )
                                KitchenCleanAnswerObject.save()


                                KitchenCleanAnswerObject = AnswerByProvider(
                                    service     =   KitchenCleanServiceObject,
                                    user        =   RohitAggarwalUser,
                                    option_Selected = "3-7 Years (Medium)",
                                    question        =   YearsOfExpQuesObj,
                                    user_name       =   "Rohit Aggarwal",
                                    service_name    =   "Kitchen Deep Cleaning",
                                    question_string  =  "How many years of experience do you have ?"
                                )
                                KitchenCleanAnswerObject.save()


                                KitchenCleanAnswerObject = AnswerByProvider(
                                    service     =   KitchenCleanServiceObject,
                                    user        =   RohitAggarwalUser,
                                    option_Selected = "Per Hour",
                                    question        =   PriceRateQuesObj,
                                    user_name       =   "Rohit Aggarwal",
                                    service_name    =   "Kitchen Deep Cleaning",
                                    question_string  =  "At what price rate do you provide service ?"
                                )
                                KitchenCleanAnswerObject.save()

                            elif subcategory.subcategory == "Beauty":

                                HairStylistServiceObject = Service(
                                    user            =   RohanSharmaUser,
                                    service_name    =   "Hair Stylist",
                                    category        =   subcategory.category,
                                    subcategory     =   subcategory,
                                    service_pricing =   800,
                                    pricing_timing_unit = "Per Hour",
                                    speciality          =   False,
                                    service_location    =   "Searchmont, ON, Canada",
                                    service_location_lat =  46.7786400000,
                                    service_location_long = -84.0513300000,
                                    locality               = "Searchmont"
                                )
                                HairStylistServiceObject.save()

                                HairStylistScheduleObject = ServiceSchedule(
                                    service             =   HairStylistServiceObject,
                                    day                 =   "Thursday",
                                    checked             =   True,
                                    open_time           =   "09:00:00",
                                    close_time          =   "11:00:00"
                                )
                                HairStylistScheduleObject.save()


                                HairStylistScheduleObject = ServiceSchedule(
                                    service             =   HairStylistServiceObject,
                                    day                 =   "Thursday",
                                    checked             =   True,
                                    open_time           =   "17:00:00",
                                    close_time          =   "18:00:00"
                                )
                                HairStylistScheduleObject.save()


                                HairStylistScheduleObject = ServiceSchedule(
                                    service             =   HairStylistServiceObject,
                                    day                 =   "Friday",
                                    checked             =   True,
                                    open_time           =   "20:00:00",
                                    close_time          =   "22:00:00"
                                )
                                HairStylistScheduleObject.save()


                                HairStylistScheduleObject = ServiceSchedule(
                                    service             =   HairStylistServiceObject,
                                    day                 =   "Friday",
                                    checked             =   True,
                                    open_time           =   "16:00:00",
                                    close_time          =   "17:00:00"
                                )
                                HairStylistScheduleObject.save()


                                HairStylistImagesObject  = ServiceImage(
                                    service         =   HairStylistServiceObject,
                                    service_img_file_1_s3 = "https://meenfee.s3.amazonaws.com/public%2FHair+Stylist1.png",


                                    service_img_file = "https://meenfee.s3.amazonaws.com/public%2FHair+Stylist1.png",

                                )
                                HairStylistImagesObject.save()

                                HairStylistAnswerObject = AnswerByProvider(
                                    service     =   HairStylistServiceObject,
                                    user        =   RohanSharmaUser,
                                    option_Selected = "At service requestor's place",
                                    question        =   PointofServiceQuesObj,
                                    user_name       =   "Rohan Sharma",
                                    service_name    =   "Hair Stylist",
                                    question_string  =  "Where do you prefer to provide Service ?"
                                )
                                HairStylistAnswerObject.save()


                                HairStylistAnswerObject = AnswerByProvider(
                                    service     =   HairStylistServiceObject,
                                    user        =   RohanSharmaUser,
                                    option_Selected = "10 KM away",
                                    question        =   DistanceOfTravelQuesObj,
                                    user_name       =   "Rohan Sharma",
                                    service_name    =   "Hair Stylist",
                                    question_string  =  "How far are you willing to travel to provide the service ?"
                                )
                                HairStylistAnswerObject.save()

                                HairStylistAnswerObject = AnswerByProvider(
                                    service     =   HairStylistServiceObject,
                                    user        =   RohanSharmaUser,
                                    option_Selected = "Phone",
                                    question        =   ModeOfContactQuesObj,
                                    user_name       =   "Rohan Sharma",
                                    service_name    =   "Hair Stylist",
                                    question_string  =  "Where would you like requestor to contact you ?"
                                )
                                HairStylistAnswerObject.save()


                                HairStylistAnswerObject = AnswerByProvider(
                                    service     =   HairStylistServiceObject,
                                    user        =   RohanSharmaUser,
                                    option_Selected = "3-7 Years (Medium)",
                                    question        =   YearsOfExpQuesObj,
                                    user_name       =   "Rohan Sharma",
                                    service_name    =   "Hair Stylist",
                                    question_string  =  "How many years of experience do you have ?"
                                )
                                HairStylistAnswerObject.save()


                                HairStylistAnswerObject = AnswerByProvider(
                                    service     =   HairStylistServiceObject,
                                    user        =   RohanSharmaUser,
                                    option_Selected = "Per Hour",
                                    question        =   PriceRateQuesObj,
                                    user_name       =   "Rohan Sharma",
                                    service_name    =   "Hair Stylist",
                                    question_string  =  "At what price rate do you provide service ?"
                                )
                                HairStylistAnswerObject.save()





        return Response({"msg":"DB Populated Successfully. Do not hit this API again."},status=HTTP_200_OK)            
        
        


# class CapturePaymentGateway(APIView):
    
#     def post(self,request):
        
#         response_dict = {
#             "Response_Amount"                   :   "1000",
#             "Response_ApprovalCode"             :   "",
#             "Response_CardExpiryDate"           :   "2201",
#             "Response_CardHolderName"           :   "Akhilesh T.",
#             "Response_CardNumber"               :   "401200******1112",
#             "Response_CurrencyISOCode"          :   "400",
#             "Response_GatewayName"              :   "EMPPG",
#             "Response_GatewayStatusCode"        :   "",
#             "Response_GatewayStatusDescription" :   "Payment processed successfully.",
#             "Response_MerchantID"               :   "2000000045",
#             "Response_RRN"                      :   "2019090915463980000000000",
#             "Response_SecureHash"               :   "4998246902a7db646cfbe25a5b242e7c8a50f25273e29f43da438b477c4154d0",
#             "Response_StatusCode"               :   "00000",
#             "Response_StatusDescription"        :   "Transaction was processed successfully",
#             "Response_TransactionID"            :   "1568033086040"
#             }
        
        
        
# #         data = request.data
        
#         SECRET_KEY = "N2UwNmQ3NDlmZmY4Yzg1NTA0NzUwMTdm"
        
        


# import hashlib

# class TestClass(APIView):
    
#     def post(self,request):
        

#         SECRET_KEY = "N2UwNmQ3NDlmZmY4Yzg1NTA0NzUwMTdm"
#         response_parameters = request.query_params
#         if len(response_parameters.keys()) == 0:
            
#             response_parameters = request.data
            
        
        
#         response_ordered_string = ""
        
#         response_ordered_string += SECRET_KEY
        
#         for key in response_parameters:
            
#             cleaned_value = ""
            
#             if key == "Response_GatewayStatusDescription":
#                 cleaned_value = response_parameters[key].replace(" ","+")
#             elif key == "Response_StatusDescription":
#                 cleaned_value = response_parameters[key].replace(" ","+")
#             elif key == "Response_SecureHash":
#                 pass
#             else:
#                 cleaned_value = response_parameters[key]
                
#             response_ordered_string += cleaned_value
        
#         received_secure_hash = response_parameters["Response_SecureHash"]
#         generated_hash  = hashlib.sha256(response_ordered_string.encode()).hexdigest()
#         if generated_hash == received_secure_hash:
#             print("<--------------------THey Are equal----------------->")
# #         print("<-------------------Generated hash--------------------->",generated_hash.hexdigest())
#         print("<----------Response ORdered-------- string-------------->",response_ordered_string)
            
# #         print("<=------------------Params in Request---------------->",response_parameters)

        
        
        
class CapturePaymentResponse(APIView):

    def post(self,request):
        data = request.data

        print("<--------Incoming Request Data Capture Payment Response------------->",data)
        if "booking_id" in data:
            booking_id = data["booking_id"]
        else:
            return Response({"msg":"Booking ID missing in request data."},status=HTTP_400_BAD_REQUEST)
        
        if "user_id" in data:
            user_other_id = data["user_id"]
            UserOtherObject = UserOtherInfo.objects.get(id=user_other_id)
            user_id = UserOtherObject.user.id
        else:
            return Response({"msg":"User ID missing in request data."},status=HTTP_400_BAD_REQUEST)
        

        if "gateway_response" in data:
            gateway_response = data["gateway_response"]
        
        else:
            return Response({"msg":"Gateway Response missing in request data."},status=HTTP_400_BAD_REQUEST)

        if "payment_for" in data:
            payment_for = data["payment_for"]
            if payment_for not in ["Completion","Cancellation"]:
                return Response({"msg":"Invalid Payment For Values. Valid values are : 'Completion' and 'Cancellation'."},status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"Payment for parameter missing in request data."},status=HTTP_400_BAD_REQUEST)

        
        if "transaction_status" in data:
            transaction_status = data["transaction_status"]
            if transaction_status not in ["success","in_progress","failed"]:
                return Response({"msg":"Invalid transaction status value.Valid values are : 'success' , 'in_progress' , 'failed' "},status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"Transaction Status missing in request data."},status=HTTP_400_BAD_REQUEST)

        User = request.user

        if User.id != user_id:
            return Response({"msg":"User ID in data payload does not match with the one provided in Authorization header"},status=HTTP_400_BAD_REQUEST)
        
        
        gateway_response_serialized = json.dumps(gateway_response)
        BookingObject = NewBookingModel.objects.get(booking_id__exact=booking_id)

        CardTransactionObject = CardTransactionMaster(
            payment_for = payment_for,
            service_id  = BookingObject.service_ID,
            booking   = BookingObject,
            service_requestor = BookingObject.requestor_id,
            service_provider  = BookingObject.provider_id,
            raw_json_response_string = gateway_response_serialized
        )
        CardTransactionObject.save()

        if transaction_status == "success":

            if payment_for == "Cancellation":
                BookingObject.booking_cancelled = True
                BookingObject.cancelled_by_requestor = True
                BookingObject.cancellation_fee = round((((BookingObject.service_charges + BookingObject.admin_charges) * CANCELLATION_FEE_PERCENTAGE)/100),2)
                BookingObject.booking_closure_time = timezone.now()
                BookingObject.payment_incurred = True
                BookingObject.payment_completed = True            
                BookingObject.save()

                fcm_receiver_token = BookingObject.provider_id.fcm_token
                message_body = "Service requestor has cancelled the booking."
                try:
                    send_to_one(fcm_receiver_token, message_body, "Appointment Cancelled")
                except Exception as e:
                    print("<----------FCM Exception----------------->",e)
                    pass

                InAppBookingNotificationsObject = InAppBookingNotifications(
                    from_user_id = BookingObject.requestor_id,
                    from_user_name = BookingObject.requestor_id.user.get_full_name(),
                    to_user_id = BookingObject.provider_id,
                    to_user_name = BookingObject.provider_id.user.get_full_name(),
                    notification_type = "Booking Cancelled",
                    notification_title = "Your booking request " + "(Booking ID: " + BookingObject.booking_id +")"+" has been declined by the service provider.",
                    service_name      = BookingObject.service_name,
                    notification_time = timezone.now(),
                    notification_date  = timezone.now(),
                    to_user_usertype = PROVIDER_STRING
                    )
                InAppBookingNotificationsObject.save()


                try:
                    LivePaymentObject = LivePayments.objects.get(booking_ID__exact=BookingObject.booking_id)

                    SettledPaymentObject = SettledPayments(
                        payment_card                =   LivePaymentObject.payment_card,
                        payment_method              =   LivePaymentObject.payment_method,
                        payment_request_date        =   LivePaymentObject.payment_request_date,
                        payment_request_time        =   LivePaymentObject.payment_request_time,
                        payment_settle_date         =   timezone.now(),
                        payment_settle_time         =   timezone.now(),
                        service                     =   LivePaymentObject.service,
                        payment_from                =   LivePaymentObject.payment_from,
                        payment_to                  =   LivePaymentObject.payment_to,
                        booking_ID                  =   LivePaymentObject.booking_ID,
                        cash_paid_by_requestor      =   LivePaymentObject.cash_paid_by_requestor,
                        cash_collected_by_provider  =   LivePaymentObject.cash_collected_by_provider,
                        service_charges             =   LivePaymentObject.service_charges,
                        admin_charges               =   LivePaymentObject.admin_charges,
                        total_amount_paid           =   LivePaymentObject.service_charges +  LivePaymentObject.admin_charges,
                        payment_for                 =   "Cancellation"
                        )
                    SettledPaymentObject.save()

                    SettledPaymentsCancelObject = SettledPaymentsCancel(
                        payment_card                =   LivePaymentObject.payment_card,
                        payment_method              =   LivePaymentObject.payment_method,
                        payment_request_date        =   LivePaymentObject.payment_request_date,
                        payment_request_time        =   LivePaymentObject.payment_request_time,
                        payment_settle_date         =   timezone.now(),
                        payment_settle_time         =   timezone.now(),
                        service                     =   LivePaymentObject.service,
                        payment_from                =   LivePaymentObject.payment_from,
                        payment_to                  =   LivePaymentObject.payment_to,
                        booking_ID                  =   LivePaymentObject.booking_ID,
                        cash_paid_by_requestor      =   LivePaymentObject.cash_paid_by_requestor,
                        cash_collected_by_provider  =   LivePaymentObject.cash_collected_by_provider,
                        service_charges             =   LivePaymentObject.service_charges,
                        admin_charges               =   LivePaymentObject.admin_charges,
                        total_amount_paid           =   LivePaymentObject.service_charges +  LivePaymentObject.admin_charges,
                        payment_for                 =   "Cancellation"
                        )
                    SettledPaymentsCancelObject.save()
                    
                    LivePaymentObject.delete()

                except Exception as e:
                    print("<---------------Exception occured in Live Payments Cancellation---------------->",e)
                    pass


            elif payment_for == "Completion":
                
                BookingObject.task_status = 'Completed'
                BookingObject.booking_completed = True
                BookingObject.booking_marked_completed_by_requestor = True
                BookingObject.booking_marked_completed_by_provider = True
                BookingObject.booking_closure_time = timezone.now()
                BookingObject.payment_completed = True
                BookingObject.save()

                fcm_receiver_token = BookingObject.provider_id.fcm_token
                message_body = "Requestor has marked the appointment as complete and has completed the payment."
                try:
                    send_to_one(fcm_receiver_token, message_body, "Appointment Complete")
                except Exception as e:
                    print("<----------FCM Exception----------------->",e)
                    pass

                InAppBookingNotificationsObject  =  InAppBookingNotifications(
                    from_user_id                = BookingObject.requestor_id,
                    from_user_name              = BookingObject.requestor_id.user.get_full_name(),
                    to_user_id                  = BookingObject.provider_id,
                    to_user_name                = BookingObject.provider_id.user.get_full_name(),
                    notification_type           = "Booking Completed",
                    service_name                = BookingObject.service_name,
                    notification_title          = "Your Booking has been marked completed by service requestor and payment is complete.",
                    notification_time           = timezone.now(),
                    notification_date           = timezone.now(),
                    to_user_usertype            = PROVIDER_STRING
                    )
                InAppBookingNotificationsObject.save()

                try:
                    LivePaymentObject = LivePayments.objects.get(booking_ID__exact=BookingObject.booking_id)

                    SettledPaymentObject = SettledPayments(
                        payment_card                =   LivePaymentObject.payment_card,
                        payment_method              =   LivePaymentObject.payment_method,
                        payment_request_date        =   LivePaymentObject.payment_request_date,
                        payment_request_time        =   LivePaymentObject.payment_request_time,
                        payment_settle_date         =   timezone.now(),
                        payment_settle_time         =   timezone.now(),
                        service                     =   LivePaymentObject.service,
                        payment_from                =   LivePaymentObject.payment_from,
                        payment_to                  =   LivePaymentObject.payment_to,
                        booking_ID                  =   LivePaymentObject.booking_ID,
                        cash_paid_by_requestor      =   LivePaymentObject.cash_paid_by_requestor,
                        cash_collected_by_provider  =   LivePaymentObject.cash_collected_by_provider,
                        service_charges             =   LivePaymentObject.service_charges,
                        admin_charges               =   LivePaymentObject.admin_charges,
                        total_amount_paid           =   LivePaymentObject.service_charges +  LivePaymentObject.admin_charges,
                        payment_for                 =   "Completion"
                        )
                    SettledPaymentObject.save()
                    
                    LivePaymentObject.delete()

                except Exception as e:
                    print("<---------------Exception occured in Live Payments Completion---------------->",e)
                    pass

            return Response({"msg":"Payment successful","status":"PAY_SUCCESS"},status=HTTP_200_OK)
        elif transaction_status == "in_progress":
            return Response({"msg":"Payment in progress","status":"PAY_IN_PROGRESS"},status=HTTP_200_OK)
        elif transaction_status == "failed":
            return Response({"msg":"Payment failed","status":"PAY_FAIL"},status=HTTP_200_OK)

# class TestTransaction(APIView):

#     def post(self,request):

#         data = request.data
#         json_data = data

#         json_string = json.dumps(json_data)

#         TempTableObject = TempTable(raw_json_response_string = json_string)

#         TempTableObject.save()

#         print("<---------Json Data----------->",json.loads(TempTableObject.raw_json_response_string))

#         print("<---------Json Data Type==========?",type(json.loads(TempTableObject.raw_json_response_string)))

#         return HttpResponse({"msg":"Saved"},status=HTTP_200_OK)



class FetchAdminCharges(APIView):
    def get(self,request):
        AdminChargeQS = AdminCommision.objects.filter(active=True).order_by('-commision_added')
        AdminCharge = AdminChargeQS[0]
        return Response({"admin_charge":AdminCharge.value},status=HTTP_200_OK)



# class TestTimeView(APIView):
#     def post(self, request):
#         data = request.data
#         print("<---------------Incmoing Data-------------?>",data)
#         TestTimeobject = TestTime(date_time = data["timestamp"])
#         TestTimeobject.save()
#         # return Response()


class FetchUserDetails(APIView):
    def get(self,request):

        user = request.user
        user_data={
            "username" 			: "",
			"first_name" 		: "",
			"last_name" 		: "",
			"email" 			: "",
			"phone" 			: "",
			"user_address" 		: "",
			"user_address_lat" 	: "",
			"user_address_long" : "",
			"profile_image" 	: "",
			"idcard" 			: "",
			"bio" 				: "",
			"usertype"			: "",
            "pending_payment"   : False,
            "booking_list"      : []
			}
        
        if user.is_anonymous:
            return Response({"msg":"You need to login to view this data"},status=HTTP_400_BAD_REQUEST)
        else:
            try:
                user_object = User.objects.get(id=user.id)
            except Exception as e:
                print("<---------------Some exception occurred------------->",e)
                return Response({"msg":"User does not exist."},status=HTTP_400_BAD_REQUEST)

            uoi_object = UserOtherInfo.objects.get(user=user)

            user_data["username"]               =   user_object.username
            user_data["first_name"]             =   user_object.first_name
            user_data["last_name"]              =   user_object.last_name
            user_data["email"]                  =   user_object.email
            user_data["phone"]                  =   uoi_object.phone
            user_data["user_address"]           =   uoi_object.user_address
            user_data["user_address_lat"]       =   uoi_object.user_address_lat
            user_data["user_address_long"]      =   uoi_object.user_address_long
            user_data["profile_image"]          =   uoi_object.profile_image_s3
            user_data["idcard"]                 =   uoi_object.idcard
            user_data["bio"]                    =   uoi_object.bio
            user_data["usertype"]               =   uoi_object.usertype



            if uoi_object.usertype in ["requester","Requester"]:
                BookingQS = NewBookings.objects.filter(
                    requestor_id = uoi_object,
                    booking_marked_completed_by_provider = True,
                    payment_incurred = True,
                    payment_completed = False
                )
                if len(BookingQS) > 0:
                    user_data["pending_payment"] = True
                    for BookingObject in BookingQS:

                        if BookingObject.payment_mode == "" or BookingObject.payment_mode == None:

                            try:
                                LivePaymentObject = LivePayments.objects.get(booking_ID__exact = BookingObject.booking_id)
                                if LivePaymentObject.payment_method == "Card":
                                    Booking_Serialized = PendingActionsSerializer(BookingObject,context={'uoi_object_id':uoi_object.id}).data
                                    user_data["booking_list"].append(Booking_Serialized)
                            except Exception as e:
                                print("<-----------Some Exception occured while fetching Live pyaments------------>",e)
                                Booking_Serialized = PendingActionsSerializer(BookingObject,context={'uoi_object_id':uoi_object.id}).data
                                user_data["booking_list"].append(Booking_Serialized)


                        elif BookingObject.payment_mode == "Card":
                            Booking_Serialized = PendingActionsSerializer(BookingObject,context={'uoi_object_id':uoi_object.id}).data
                            user_data["booking_list"].append(Booking_Serialized)

                    return Response(user_data,status=HTTP_200_OK)
                else:
                    return Response(user_data,status=HTTP_200_OK)
            else:
                return Response(user_data,status=HTTP_200_OK)


class RandomizeArabicStrings(APIView):
    def get(self,request):
        my_list = ['بعض', 'الفئات', 'هي', 'فريدة', 'من', 'نوعها', 'لكيفية', 'تفسير', 'المستخدم', 'في', 'المستعرض','حيث', 'أن', 'وحدة', 'المعالجة', 'المركزية', 'التي', 'تحتوي', 'على', 'تقلبات', 'لا', 'تحتاج', 'بالضرورة', 'إلى', 'أن', 'تكون', 'متصلاً', 'عبر', 'البوابات', 'أو', 'البوابات.', 'الخلط', 'التراكمي', 'للعمليات', 'يعوض', 'الفقد', 'في', 'الكمون', 'بسبب', 'العملية', 'الحرارية']

        length_of_my_list = len(my_list)
    
        last_four_random_nums = []

        All_Options =  OptionsFilledbyAdmin.objects.all()

        for option in All_Options:
            while True:
                random_arabic_string_index = random.randint(0,length_of_my_list-1)

                if random_arabic_string_index not in last_four_random_nums:
                    if len(last_four_random_nums) < 4:
                        last_four_random_nums.append(random_arabic_string_index)
                        break
                    else:
                        del(last_four_random_nums[0])
                        last_four_random_nums.append(random_arabic_string_index)
                        break
            
            option.Option1_in_arabic = my_list[random_arabic_string_index]
            option.save()

        
        return Response({"msg":"Arabic Strings randomized"},status=HTTP_200_OK)



class QuestionStringToArabic(APIView):

    def get(self,request):

        QuestionQS = QuestionFilledByAdmin.objects.all()

        for question in QuestionQS:
            if question.question_for_provider == "Where do you prefer to provide Service ?":
                question.question_for_provider_in_arabic = "أين تفضل تقديم الخدمة؟"
                question.save()
            

            if question.question_for_requestor == "Where do you prefer to avail the Service ?":
                question.question_for_requestor_in_arabic = "أين تفضل الاستفادة من الخدمة؟"
                question.save()

            if question.question_for_provider == "How far are you willing to travel to provide the service ?":
                question.question_for_provider_in_arabic = "إلى أي مدى أنت على استعداد للسفر لتقديم الخدمة؟"
                question.save()


            if question.question_for_requestor == "How far are you willing to travel to seek service ?":
                question.question_for_requestor_in_arabic = "إلى أي مدى أنت على استعداد للسفر لطلب الخدمة؟"
                question.save()


            if question.question_for_provider == "How many years of experience do you have ?":
                question.question_for_provider_in_arabic = "كم سنة من الخبرة لديك؟"
                question.save()
            
            if question.question_for_requestor == "How much experienced provider are you seeking ?":
                question.question_for_requestor_in_arabic = "كم مزود خبرة كنت تسعى؟"
                question.save()


            if question.question_for_provider == "At what price rate do you provide service ?":
                question.question_for_provider_in_arabic = "ما هو سعر السعر الذي تقدمه الخدمة؟"
                question.save()


            if question.question_for_requestor == "At what price rate are you willing to seek service ?":
                question.question_for_requestor_in_arabic = "بأي سعر سعر أنت على استعداد لطلب الخدمة؟"
                question.save()


            if question.question_for_provider == "Where would you like requestor to contact you ?":
                question.question_for_provider_in_arabic = "أين تريد مقدم الطلب الاتصال بك؟"
                question.save()


            if question.question_for_requestor == "How would you like to contact service provider ?":
                question.question_for_requestor_in_arabic = "كيف تريد الاتصال بمزود الخدمة؟"



        return Response({"msg":"Questions Translated"},status=HTTP_200_OK)


class InsertQuestion(APIView):
    def get(self,request):

        subcategory_qs = SubCategory.objects.all()

        for subcategory in subcategory_qs:
            
            QuestionObject = QuestionFilledByAdmin(
                Question_name = "Price Rate",
                SubCategory = subcategory,
                question_for_provider = "At what price rate do you provide service ?",
                question_for_provider_in_arabic = "ما هو سعر السعر الذي تقدمه الخدمة؟",
                question_for_requestor = "At what price rate are you willing to seek service ?",
                question_for_requestor_in_arabic = "بأي سعر سعر أنت على استعداد لطلب الخدمة؟"
            )
            QuestionObject.save()

            Option1 = OptionsFilledbyAdmin(
                question = QuestionObject,
                Option1 = "Per Hour",
                Option1_in_arabic = "في الساعة"
            )
            Option1.save()


            Option2 = OptionsFilledbyAdmin(
                question = QuestionObject,
                Option1 = "Per Project",
                Option1_in_arabic = "لكل مشروع"
            )
            Option2.save()

        return Response({"msg":"Question Inserted"},status=HTTP_200_OK)



# Feedback to MeenFee Service

class MeenFeeFeedbackCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self, request, format=None):
        data = request.data
        serializer = MeenFeeFeedbackCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.validated_data['timestamp'] = datetime.now().time()
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

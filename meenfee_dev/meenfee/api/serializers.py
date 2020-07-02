from meenfee.models import *
import json
import collections
from _operator import itemgetter
# from builtins import True
orderedDict = collections.OrderedDict()
# from .models import File
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_204_NO_CONTENT,HTTP_201_CREATED,HTTP_404_NOT_FOUND
from rest_framework.serializers import (
	ModelSerializer,
	SerializerMethodField,
	HyperlinkedIdentityField,
    SlugRelatedField
	)


from rest_framework.serializers import(
     ModelSerializer,
     EmailField, 
     CharField,
     DecimalField,
     ValidationError,
     SerializerMethodField,
     Serializer,
     )


from services.models import *




INTERNAL_TIME_FORMAT = None
EXTERNAL_TIME_FORMAT = "%I:%M %p"

INTERNAL_DATE_FORMAT = None
EXTERNAL_DATE_FORMAT = "%d/%m/%Y"




class UserListSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = [
            'id',
            'first_name',
            'last_name',
            'email'
        ]

class CategoryListSerializer(ModelSerializer):

	
	class Meta:
		model = Category
		fields = [
            'id',
            'category',
            'bannerimage'
        ]
	


# Arabic clone
class CategoryListArabicSerializer(ModelSerializer):
	
    category = SerializerMethodField()

    def get_category(self,instance):
        return instance.category_in_arabic
    
    class Meta:
        model = Category
        fields = [
            'id',
            'category',
            'bannerimage'
        ]



class CityListSerializer(ModelSerializer):
	class Meta:
		model = City
		fields = [
            'id',
            'city'
        ]

#Arabic clone
class CityListArabicSerializer(ModelSerializer):
	class Meta:
		model = City
		fields = [
            'id',
            'city_in_arabic'
        ]

class SubCategoryListSerializer(ModelSerializer):
	
	
	class Meta:
		model = SubCategory
		fields = [
            'id',
            'category',
            'bannerimage',
            'subcategory'
        ]
	


# Arabic clone
class SubCategoryListArabicSerializer(ModelSerializer):

    category = SerializerMethodField()
    subcategory = SerializerMethodField()

    def get_category(self,instance):
        return instance.category.category_in_arabic

    def get_subcategory(self,instance):
        return instance.subcategory_in_arabic
    
    class Meta:
        model = SubCategory
        fields =[
            'id',
            'category',
            'subcategory',
            'bannerimage'
        ]

class RowBookingListSerializer(ModelSerializer):
	class Meta:
		model = RawBooking
		fields = '__all__'


# class ServiceProviderAvailabilityListSerializer(ModelSerializer):
# 	class Meta:
# 		model = ServiceProviderAvailability
# 		fields = [
# 			'availability_date',
# 			'availability_time_from',
# 			'availability_time_to'
# 		]

class MeenFeeFeedbackCreateSerializer(ModelSerializer):
	class Meta:
		model = MeenFeeFeedback
		fields = [
			'content'
		]


class HelpAndSupportListSerializer(ModelSerializer):
	class Meta:
		model = HelpAndSupport
		fields = [
            'id',
            'contactaddress',
            'contactnumber',
            'email',
            'website'
        ]

#Arabic clone
class HelpAndSupportListArabicSerializer(ModelSerializer):
	class Meta:
		model = HelpAndSupport
		fields = [
            'id',
            'contactaddress_in_arabic',
            'contactnumber',
            'email',
            'website'
        ]



class ServiceScheduleSerializer(ModelSerializer):
    class Meta:
        model = ServiceSchedule
        fields = '__all__'




# class ServiceCreateSerializer(ModelSerializer):

#     class Meta:
#         model = Service
#         fields = [
#             'category',
#             'subcategory',
#             'experience',
#             'levelskill',
#             'city',
#             'distance_limit',
#             'service_pricing',
#             'quote_at_request',
#             'pricing_timing_unit',
#             'provide_tools',
#             'tool_specify',
#             'instant_booking',
#             ]


class ServiceCreateSerializer(ModelSerializer):

#     distance_limit          = CharField(allow_blank=True)
    locality                = CharField(allow_blank=True)
    service_location        = CharField(allow_blank=True)
    # service_location_lat    = (allow_blank=True)
    # service_location_long   = SerializerMethodField(allow_blank=True)



    class Meta:
        model = Service
        fields = [
            'service_place',
            'service_name',
            'category',
            'subcategory',
            'experience',
            'levelskill',
            'city',
#             'distance_limit',
            'service_pricing',
            'pricing_timing_unit',
            'provide_tools',
            'instant_booking',
            'avg_rating',
            # 'service_img',
            # 'service_img_file'
            'speciality',
            'service_location',
            'service_location_lat',
            'service_location_long',
            'locality',
            'experience_description'
        ]




# class FileSerializer(ModelSerializer):
#     class Meta:
#         model = ServiceImage
#         fields = [
#             'service_img_file'
#             ]


# provider : 1,
# subcategory:2,
# experience:I have experience in blah blah blah
# levelskill:Elite-(7+),
# distance_limit:5 Km away,
# service_place:I travel to my customers,
# service_pricing:500,
# pricing_timing_unit:Per Hour,
# provide_tools:True,
# instant_booking:True,
# avg_rating:4.5,
# category:1

class ServiceCreateSerializerCopy(ModelSerializer):


    class Meta:
        model = Service
        fields = [
            'service_place',
            'service_name',
            'category',
            'subcategory',
            'experience',
            'levelskill',
            'city',
            'distance_limit',
            'service_pricing',
            'pricing_timing_unit',
            'provide_tools',
            'instant_booking',
            'avg_rating',
            'available_on_Sunday',
            'available_on_Monday',
            'available_on_Tuesday', 
            'available_on_Wednesday',   
            'available_on_Thursday',   
            'available_on_Friday',     
            'available_on_Saturday',
            # 'service_img'    

        ]

# def create(self, validated_data):
#     schedule = validated_data.pop('schedule')
#     service = Service.objects.create(**validated_data)
#     for schedule_object in schedule:



# class ServiceImageSerializer(ModelSerializer):
#     class Meta:
#         model = File
#         fields = "__all__"


# class UserOtherInfoSerializer(ModelSerializer):
#     name = SerializerMethodField()
#     email = SerializerMethodField()
#     profile_img  = SerializerMethodField()
# 
#     class Meta:
#         model = UserOtherInfo
#         fields = [
#             'id',
#             'phone',
#             'user',
#             'name',
#             'email',
#             'response_within',
#             'avg_rating',
#             'location',
#             'created',
#             'type_of_tasker',
#             'bio',
#             'completed_tasks',
#             'current_language',
#             'idcard',
#             'profile_img',
#             'user_address',
#              'user_address',
#             'user_address_lat',
#             'user_address_long',
# 
#             ]
# 
# 
#     def get_profile_img(self,instance):
#         return instance.profile_image_s3
# 
#     def get_email(self,instance):
#         userObj = User.objects.get(id = instance.user.id)
#         return userObj.email
# 
#     def get_name(self,instance):
#         userObj = User.objects.get(id = instance.user.id)
#         data = FirstNameSerializer(userObj).data
#         return data
#        
#     def get_profile_img(self,instance):
#     	data = UserProfileImageSerializer(instance).data
#     	if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
#     		return data['profile_img']
#     	else:
#     		return data['profile_image_s3']

class UserOtherInfoSerializer(ModelSerializer):
    name = SerializerMethodField()
    email = SerializerMethodField()
    profile_img  = SerializerMethodField()
    speciality_service_name = SerializerMethodField()

    class Meta:
        model = UserOtherInfo
        fields = [
            'id',
            'phone',
            'user',
            'name',
            'email',
            'response_within',
            'avg_rating',
            'location',
            'created',
            'type_of_tasker',
            'bio',
            'completed_tasks',
            'current_language',
            'idcard',
            'profile_img',
            'user_address',
            'user_address_lat',
            'user_address_long',
            'is_id_verified',
            'switched_to_provider',
            'locality',
            'speciality_service_name'
            ]


    def get_profile_img(self,instance):
        data = UserProfileImageSerializer(instance).data
        if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
            return ""
        else:
            return data['profile_image_s3']


    def get_email(self,instance):
        userObj = User.objects.get(id = instance.user.id)
        return userObj.email

    def get_name(self,instance):
        userObj = User.objects.get(id = instance.user.id)
        data = FirstNameSerializer(userObj).data
        return data
    
    def get_speciality_service_name(self,instance):
    	user_object = User.objects.get(id=instance.user.id)
    	try:
    		ServiceObjectQS = Service.objects.filter(user=user_object).filter(speciality=True)
    		Service_object = ServiceObjectQS[0]
    		return Service_object.service_name
    	except:
    		return ""

    	



class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = ServiceFeedback
        fields = '__all__'

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            'rating'
        ]

class SlotListSerializer(ModelSerializer):
    class Meta:
        model = Slots
        fields = '__all__'

class SheduleListSerializer(ModelSerializer):
    class Meta:
        model = days
        fields = '__all__'

# class ServiceSerializer(ModelSerializer):
#     feedback = SerializerMethodField()
#     category = SerializerMethodField()
#     subcategory = SerializerMethodField()
#     avg_rating = SerializerMethodField()
#     # schedule = SerializerMethodField()
#     service_ID = SerializerMethodField()
#     schedule  = SerializerMethodField()
#     service_images = SerializerMethodField()
# 
#     def get_avg_rating(self,instance):
#         service = instance.id
#         qs = Rating.objects.filter(services=service)
#         data = RatingSerializer(qs, many=True).data
#         array = []
#         for j in json.loads(json.dumps(data)):
#             array.append(j['rating'])
#         sum = 0
#         for i in array:
#             sum = sum + i
#         if len(array) is not 0:
#             avg_rating = sum/len(array)
#             return avg_rating
#     def get_feedback(self,instance):
#         service = instance.id
#         qs   = ServiceFeedback.objects.filter(service=service)
#         data = FeedbackSerializer(qs ,many=True).data
#         return data
#     def get_category(self,instance):
#         service = instance.id
#         serviceObj = Service.objects.get(id=service)
#         qs   = Category.objects.get(id=serviceObj.category.id)
#         data = CategoryListSerializer(qs).data
#         return data
#     def get_subcategory(self,instance):
#         service = instance.id
#         serviceObj = Service.objects.get(id=service)
#         qs   = SubCategory.objects.filter(id=serviceObj.subcategory.id)
#         data = SubCategoryListSerializer(qs,many=True).data
#         return data
# 
#     def get_service_ID(self,instance):
#         return instance.id
# 	
# 	
#     def get_schedule(self,instance):
#         service = instance.id
#         ServiceScheduleQS = ServiceSchedule.objects.filter(service = service)
#         schedule = []
#         slots_array = []
#         
#         days_of_the_week = [
#             "Monday",
#             "Tuesday",
#             "Wednesday",
#             "Thursday",
#             "Friday",
#             "Saturday",
#             "Sunday"
#         ]
#         for day in days_of_the_week:
#             slots_array = []
#             TempQS = ServiceScheduleQS.filter(day=day)
#             if len(TempQS) == 0:
#                 schedule_object = {
#                     "Day":day,
#                     "checked":False,
#                     "slots_array":slots_array 
#                 }
#                 schedule.append(schedule_object)
#             else:
#                 for item in TempQS:
#                     slot_object = {
#                         "open_time":item.open_time,
#                         "close_time":item.close_time
#                     }
#                     slots_array.append(slot_object)
# 
#                 schedule_object = {
#                     "Day":day,
#                     "cheked":True,
#                     "slots_array":slots_array
#                 }
#                 schedule.append(schedule_object)
#         return schedule
#     
#     
# 	
# 
#     # def get_schedule(self,instance):
#     #     daysObj = days.objects.get(Service = instance.id)
#     #     daysdata = SheduleListSerializer(daysObj).data
#     #     sunday = daysdata['Sunday']
#     #     monday = daysdata['Monday']
#     #     tuesday = daysdata['Tuesday']
#     #     wednesday = daysdata['Wednesday']
#     #     thursday  = daysdata['Thursday']
#     #     friday    = daysdata['Friday']
#     #     saturday  = daysdata['Saturday']
#     #     sundayqs   = Slots.objects.filter(service = instance.id,day="Sunday")
#     #     sundayslots = SlotListSerializer(sundayqs,many=True).data
#     #     mondayqs   = Slots.objects.filter(service = instance.id,day="Monday")
#     #     mondayslots = SlotListSerializer(mondayqs,many=True).data
#     #     tuesdayqs   = Slots.objects.filter(service = instance.id,day="Tuesday")
#     #     tuesdayslots = SlotListSerializer(tuesdayqs,many=True).data
#     #     wednesdayqs   = Slots.objects.filter(service = instance.id,day="Wednesday")
#     #     wednesdaylots = SlotListSerializer(wednesdayqs,many=True).data
#     #     thursdayqs   = Slots.objects.filter(service = instance.id,day="Thursday")
#     #     thursdayslots = SlotListSerializer(thursdayqs,many=True).data
#     #     fridayqs   = Slots.objects.filter(service = instance.id,day="Friday")
#     #     fridayslots = SlotListSerializer(fridayqs,many=True).data
#     #     saturdayqs   = Slots.objects.filter(service = instance.id,day="Saturday")
#     #     saturdayslots = SlotListSerializer(saturdayqs,many=True).data
#     #     data = [{"sunday":sunday,"slot_Sunday":sundayslots},
#     #             {"monday":monday,"slot_monday":mondayslots},
#     #             {"tuesday":tuesday,"slot_tuesday":tuesdayslots},
#     #             {"wednesday":wednesday,"slot_wednesday":wednesdaylots},
#     #             {"thursday":thursday,"slot_thursday":thursdayslots},
#     #             {"friday":friday,"slot_friday":fridayslots},
#     #             {"saturday":saturday,"slot_saturday":saturdayslots},
#     #             ]
#     #     return data
# 
# 
# 
#     # def get_schedule(self,instance):
#     #     scheduleQS = ServiceSchedule.objects.filter(service=instance.id)
#     #     for schedule in scheduleQS:
#     #         if schedule['checked'] == "Sunday":
# 
# 	
# 	
# 
# 	           
#     class Meta:
#         model = Service
#         fields = [
#             'service_ID',
#             'service_name',
#             'category',
#             'subcategory',
#             'avg_rating',
#             'experience',
#             'levelskill',
#             # 'location',
#             'distance_limit',
#             'quote_at_request',
#             'provide_tools',
#             'feedback',
#             'service_pricing',
#             'pricing_timing_unit',
#             'tool_specify',
#             'instant_booking',
#             'created',
#             'schedule',
#             'service_images'
#             ]




class ServiceSerializer(ModelSerializer):
    feedback = SerializerMethodField()
    category = SerializerMethodField()
    subcategory = SerializerMethodField()
    # avg_rating = SerializerMethodField()
    # schedule = SerializerMethodField()
    service_ID = SerializerMethodField()
    schedule  = SerializerMethodField()
    service_images = SerializerMethodField()
 
    # def get_avg_rating(self,instance):
    #     service = instance.id
    #     qs = Rating.objects.filter(services=service)
    #     data = RatingSerializer(qs, many=True).data
    #     array = []
    #     for j in json.loads(json.dumps(data)):
    #         array.append(j['rating'])
    #     sum = 0
    #     for i in array:
    #         sum = sum + i
    #     if len(array) is not 0:
    #         avg_rating = sum/len(array)
    #         return avg_rating
 
 
    def get_feedback(self,instance):
        service = instance.id
        qs   = ServiceFeedback.objects.filter(service_id=instance)
        data = FeedbackSerializer(qs ,many=True).data
        return data
    def get_category(self,instance):
        service = instance.id
        serviceObj = Service.objects.get(id=service)
        qs   = Category.objects.get(id=serviceObj.category.id)
        data = CategoryListSerializer(qs).data
        return data
    def get_subcategory(self,instance):
        service = instance.id
        serviceObj = Service.objects.get(id=service)
        qs   = SubCategory.objects.filter(id=serviceObj.subcategory.id)
        data = SubCategoryListSerializer(qs,many=True).data
        return data

    def get_service_ID(self,instance):
        return instance.id


    def get_schedule(self,instance):
        service = instance.id
        ServiceScheduleQS = ServiceSchedule.objects.filter(service = service)
        schedule = []
        slots_array = []
        
        days_of_the_week = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]
        for day in days_of_the_week:
            slots_array = []
            TempQS = ServiceScheduleQS.filter(day=day)
            if len(TempQS) == 0:
                schedule_object = {
                    "Day":day,
                    "checked":False,
                    "slots_array":slots_array 
                }
                schedule.append(schedule_object)
            else:
                for item in TempQS:
                    slot_object = {
                        "open_time":item.open_time,
                        "close_time":item.close_time
                    }
                    slots_array.append(slot_object)

                schedule_object = {
                    "Day":day,
                    "cheked":True,
                    "slots_array":slots_array
                }
                schedule.append(schedule_object)
        return schedule
  

    def get_service_images(self,instance):
        image_set = []
        try:
            ServiceImageObject= ServiceImage.objects.get(service = instance.id)


            if "https" in ServiceImageObject.service_img_file_1_s3:
                image_set.append(ServiceImageObject.service_img_file_1_s3)

            if "https" in ServiceImageObject.service_img_file_2_s3:
                image_set.append(ServiceImageObject.service_img_file_2_s3)

            if "https" in ServiceImageObject.service_img_file_3_s3:
                image_set.append(ServiceImageObject.service_img_file_3_s3)


            return image_set
        except:
            return image_set

    class Meta:
        model = Service
        fields = [
            'service_ID',
            'service_name',
            'category',
            'subcategory',
            'avg_rating',
            'experience',
            'levelskill',
            # 'location',
            'distance_limit',
            'quote_at_request',
            'provide_tools',
            'feedback',
            'service_pricing',
            'pricing_timing_unit',
            'tool_specify',
            'instant_booking',
            'created',
            'schedule',
            'service_images',
            'locality',
            'experience_description'
            ]










# class ServiceSerializer(ModelSerializer):
#     feedback = SerializerMethodField()
#     category = SerializerMethodField()
#     subcategory = SerializerMethodField()
#     city = SerializerMethodField()
#     avg_rating = SerializerMethodField()
#     schedule = SerializerMethodField()

#     def get_avg_rating(self,instance):
#         service = instance.id
#         qs = Rating.objects.filter(services=service)
#         data = RatingSerializer(qs, many=True).data
#         array = []
#         for j in json.loads(json.dumps(data)):
#             array.append(j['rating'])
#         sum = 0
#         for i in array:
#             sum = sum + i
#         if len(array) is not 0:
#             avg_rating = sum/len(array)
#             return avg_rating
#     def get_feedback(self,instance):
#         service = instance.id
#         qs   = ServiceFeedback.objects.filter(service=service)
#         data = FeedbackSerializer(qs ,many=True).data
#         return data
#     def get_category(self,instance):
#         service = instance.id
#         serviceObj = Service.objects.get(id=service)
#         qs   = Category.objects.get(id=serviceObj.category.id)
#         data = CategoryListSerializer(qs).data
#         return data
#     def get_subcategory(self,instance):
#         service = instance.id
#         serviceObj = Service.objects.get(id=service)
#         qs   = SubCategory.objects.filter(id=serviceObj.subcategory.id)
#         data = SubCategoryListSerializer(qs,many=True).data
#         return data
#     def get_city(self,instance):
#         service = instance.id
#         serviceObj = Service.objects.get(id=service)
#         qs = City.objects.filter(id=serviceObj.city.id)
#         data = CityListSerializer(qs,many=True).data
#         return data
#     def get_schedule(self,instance):
#         daysObj = days.objects.get(Service = instance.id)
#         daysdata = SheduleListSerializer(daysObj).data
#         sunday = daysdata['sunday']
#         monday = daysdata['monday']
#         tuesday = daysdata['tuesday']
#         wednesday = daysdata['wednesday']
#         thursday  = daysdata['thursday']
#         friday    = daysdata['friday']
#         saturday  = daysdata['saturday']
#         sundayqs   = Slots.objects.filter(service = instance.id,day="sunday")
#         sundayslots = SlotListSerializer(sundayqs,many=True).data
#         mondayqs   = Slots.objects.filter(service = instance.id,day="monday")
#         mondayslots = SlotListSerializer(mondayqs,many=True).data
#         tuesdayqs   = Slots.objects.filter(service = instance.id,day="tuesday")
#         tuesdayslots = SlotListSerializer(tuesdayqs,many=True).data
#         wednesdayqs   = Slots.objects.filter(service = instance.id,day="wednesday")
#         wednesdaylots = SlotListSerializer(wednesdayqs,many=True).data
#         thursdayqs   = Slots.objects.filter(service = instance.id,day="thursday")
#         thursdayslots = SlotListSerializer(thursdayqs,many=True).data
#         fridayqs   = Slots.objects.filter(service = instance.id,day="friday")
#         fridayslots = SlotListSerializer(fridayqs,many=True).data
#         saturdayqs   = Slots.objects.filter(service = instance.id,day="saturday")
#         saturdayslots = SlotListSerializer(saturdayqs,many=True).data
#         data = [{"sunday":sunday,"slot_Sunday":sundayslots},
#                 {"monday":monday,"slot_monday":mondayslots},
#                 {"tuesday":tuesday,"slot_tuesday":tuesdayslots},
#                 {"wednesday":wednesday,"slot_wednesday":wednesdaylots},
#                 {"thursday":thursday,"slot_thursday":thursdayslots},
#                 {"friday":friday,"slot_friday":fridayslots},
#                 {"saturday":saturday,"slot_saturday":saturdayslots},
#                 ]
#         return data

#     class Meta:
#         model = Service
#         fields = [
#             'id',
#             'service_name',
#             'category',
#             'subcategory',
#             'avg_rating',
#             'experience',
#             'levelskill',
#             # 'location',
#             'city',
#             'distance_limit',
#             'quote_at_request',
#             'provide_tools',
#             'feedback',
#             'service_pricing',
#             'pricing_timing_unit',
#             'tool_specify',
#             'instant_booking',
#             'created',
#             'schedule'
#             ]



from accounts.api.serializers import UserDetailSerializer

class providerProfileSeralizer(ModelSerializer):
    user = SerializerMethodField()
    service = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user',
            'service'
            ]

    def get_user(self ,instance):
        obj      =  UserOtherInfo.objects.get(user = instance)
        total_bookings  = len(RawBooking.objects.filter(provider=instance.id))
        canceledBooking = len(CanceledBooking.objects.filter(provider=instance.id))
        data     =  UserOtherInfoSerializer(obj).data 
        name     =  instance.first_name+ ' ' + instance.last_name
        data['name'] = name
        data['total_bookings'] = total_bookings
        data['canceledBooking'] = canceledBooking
        data['profile_img']     = "/media/" + str(obj.profile_img)
        return data

    def get_service(self,instance):
        qs = Service.objects.filter(user = instance)
        total_bookings = RawBooking.objects.filter(provider=instance)
        data = ServiceSerializer(qs,many = True).data
        return data


class UserProfileDataSerializer(ModelSerializer):
    class Meta:
        model = UserOtherInfo
        fields = [
            'avg_rating',
            'location',
            'completed_tasks',
            'profile_views'
        ]
class UserProfileImageSerializer(ModelSerializer):
    class Meta:
        model = UserOtherInfo
        fields = [
            'profile_img',
            'profile_image_s3'
        ]
class FirstNameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name'
        ]


 
class ProviderServiceListSerializer(ModelSerializer):
    # profile_img = SerializerMethodField()
    # cat = SerializerMethodField()
    # providerName = SerializerMethodField()
    # catname = SerializerMethodField()
    # first_name = SerializerMethodField()
    # last_name = SerializerMethodField()


    class Meta:
        model = Service
        fields = [
            'user',
            'category',
            'subcategory',
            'service_pricing',
            'pricing_timing_unit',
            # 'service_img',
            'avg_rating',
            'service_name',
            'experience',
            'service_place',
            'levelskill',
            # 'city',
            'distance_limit',
            'service_pricing',
            'pricing_timing_unit',
            'provide_tools',
            'instant_booking',
            'avg_rating',
            # 'first_name',
            # 'last_name'


            # 'catname'
        ]
    # print("<------------------------User---------------------------->",instance.id)    
    # def get_providerName(self,instance):

    # def get_cat(self,instance):
    #     obj = Category.objects.get()
    # def get_profile_img(self,instance):
    #     userObj = UserOtherInfo.objects.get(user = instance.id)
    #     data = UserProfileImageSerializer(userObj).data
    #     return data['profile_img']
    # def get_catname(self,instance):
    #     data = Service.objects.get(category=instance.id)['category']
    #     return data
    # def get_first_name(self,instance):
    #     first_name = User.objects.values('first_name').get(id=user)
    #     return first_name

    # def get_last_name(self,instance):
    #     last_name = User.objects.values('last_name').get(id=user)







class ProviderServicesSerializer(ModelSerializer):
    services = SerializerMethodField()
    class Meta:
        model = Service
        fields = [
            'services',
            ]

    def get_services(self,instance):
        qs = Service.objects.filter(user = instance)
        data = ProviderServiceListSerializer(qs,many = True,).data
        return data



class AllServicesSerializerTemp(ModelSerializer):
    services = SerializerMethodField()
    # name = SerializerMethodField()
    class Meta:
        model = Service
        fields = [
            'services',
            # 'name'
            ]
        # print("<--------------------------Here--------------------------------->")


    def get_services(self,instance):
        # qs = Service.objects.exclude(user = instance)
        qs = Service.objects.all()
        # print()
        data = ProviderServiceListSerializer(qs,many = True).data
        return data



    # def get_name(self,instance):
    #     userObj = User.objects.get(id = instance.user.id)
    #     data = FirstNameSerializer(userObj).data
    #     return data







# <--------------------------------------------------Temporary--------------------------------->



# class CatnameSerializer(ModelSerializer):
#     class Meta:
#         model = Category
#         fields = [
#             'category'
#         ]




class ProviderServiceListSerializerTemp(ModelSerializer):
    # profile_img = SerializerMethodField()
    # cat = CatnameSerializer(many=True)
    # providerName = SerializerMethodField()
    # catname = SerializerMethodField()
    class Meta:
        model = Service
        fields = [
            'category',
            'subcategory',
            'service_pricing',
            'pricing_timing_unit',
            'service_img',
            'avg_rating',
            'service_img',
            'service_name'
        ]



# <------------------------NOT IN USE---------------------------------->



# class AllServicesSerializerTemp(ModelSerializer):
#     services = SerializerMethodField()

#     class Meta:
#         model = Service
#         fields = [
#             'services',
#             ]
#         # print("<--------------------------Here--------------------------------->")

#     def get_services(self,instance):
#         # qs = Service.objects.exclude(user = instance)
#         qs = ServiceCopy.objects.all()
#         print("<------------------------------------Services QS---------------------->",qs)
#         data = ProviderServiceListSerializerTemp(qs,many = True).data
#         print("<------------------------------------Services Seria;ized data---------------------->",data)
#         print("<------------------------------LEngth---------------------------->",len(data))       
#         # myjson = json.dumps(data)
#         return data
    # print("<--------------------------Here--------------------------------->")






# <------------------------NOT IN USE---------------------------------->





class AllServicesSerializer(ModelSerializer):

    name            = SerializerMethodField()
    profile_img     = SerializerMethodField()
    profile_views   = SerializerMethodField()
    location        = SerializerMethodField()
    completed_tasks = SerializerMethodField()
    avg_rating      = SerializerMethodField()
    bio             = SerializerMethodField()
    response_within = SerializerMethodField()
    type_of_tasker  = SerializerMethodField()
    services_offered = SerializerMethodField()
    # schedule     = SerializerMethodField()
    # provider_name  = SerializerMethodField()    
    user_ID     = SerializerMethodField()   
    user_address = SerializerMethodField()
    user_address_lat = SerializerMethodField()
    user_address_long = SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
                'user',
                'user_ID',
                # 'provider_name',
                'name',
                'profile_img',
                'profile_views',
                'experience',
                'levelskill',
                # 'location',
                'distance_limit',
                'service_pricing',
                'pricing_timing_unit',
                'quote_at_request',
                'provide_tools',
                'service_place',
                'locality',
                'tool_specify',
                'instant_booking',
                'avg_rating',
                'created',
                'service_name',
                'location',
                'completed_tasks',
                'avg_rating',
                'bio',
                'response_within',
                'type_of_tasker',
                'services_offered',
                'user_address',
                'user_address_lat',
                'user_address_long',
                'speciality'

                # 'schedule'
            ]
    
    def get_user_ID(self,instance):
        return instance.user.id

    def get_name(self,instance):
        userObj = User.objects.get(id = instance.user.id)
        data = FirstNameSerializer(userObj).data
        return data

    def get_profile_img(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.user.id)
        data = UserProfileImageSerializer(userObj).data
        if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
        	return ""
        else:
        	return data['profile_image_s3']
        

    def get_profile_views(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.user.id)
        data = UserProfileDataSerializer(userObj).data
        return data['profile_views']

    def get_location(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.user.id)
        data = UserProfileDataSerializer(userObj).data
        return data['location']

    def get_completed_tasks(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.user.id)
        data = UserProfileDataSerializer(userObj).data
        return data['completed_tasks']

    def get_avg_rating(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.user.id)
        data = UserProfileDataSerializer(userObj).data
        return data['avg_rating']

    def get_bio(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.user.id)
        data = UserOtherInfoSerializer(userObj).data
        return data['bio']

    def get_response_within(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.user.id)
        data = UserOtherInfoSerializer(userObj).data
        return data['response_within']

    def get_type_of_tasker(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.user.id)
        data = UserOtherInfoSerializer(userObj).data
        return data['type_of_tasker'] 



    def get_services_offered(self,instance):
        qs = Service.objects.filter(user = instance.user.id)
        # total_bookings = RawBooking.objects.filter(provider=instance.user.id)
        data = ServiceSerializer(qs,many = True).data
        return data  
   
    def get_user_address(self,instance):
    	userObj = UserOtherInfo.objects.get(user = instance.user.id)
    	data  =  UserOtherInfoSerializer(userObj).data
    	return data['user_address']
    def get_user_address_lat(self,instance):
    	userObj = UserOtherInfo.objects.get(user = instance.user.id)
    	data  =  UserOtherInfoSerializer(userObj).data
    	return data['user_address_lat']
    def get_user_address_long(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.user.id)
        data  =  UserOtherInfoSerializer(userObj).data
        return data['user_address_long']

	
       
    # def get_schedule(self,instance):

    #         daysObj = days.objects.get(Service = instance.id)
    #         daysdata = SheduleListSerializer(daysObj).data
    #         sunday = daysdata['Sunday']
    #         monday = daysdata['Monday']
    #         tuesday = daysdata['Tuesday']
    #         wednesday = daysdata['Wednesday']
    #         thursday  = daysdata['Thursday']
    #         friday    = daysdata['Friday']
    #         saturday  = daysdata['Saturday']
    #         sundayqs   = Slots.objects.filter(service = instance.id,day="Sunday")
    #         sundayslots = SlotListSerializer(sundayqs,many=True).data
    #         mondayqs   = Slots.objects.filter(service = instance.id,day="Monday")
    #         mondayslots = SlotListSerializer(mondayqs,many=True).data
    #         tuesdayqs   = Slots.objects.filter(service = instance.id,day="Tuesday")
    #         tuesdayslots = SlotListSerializer(tuesdayqs,many=True).data
    #         wednesdayqs   = Slots.objects.filter(service = instance.id,day="Wednesday")
    #         wednesdaylots = SlotListSerializer(wednesdayqs,many=True).data
    #         thursdayqs   = Slots.objects.filter(service = instance.id,day="Thursday")
    #         thursdayslots = SlotListSerializer(thursdayqs,many=True).data
    #         fridayqs   = Slots.objects.filter(service = instance.id,day="Friday")
    #         fridayslots = SlotListSerializer(fridayqs,many=True).data
    #         saturdayqs   = Slots.objects.filter(service = instance.id,day="Saturday")
    #         saturdayslots = SlotListSerializer(saturdayqs,many=True).data
    #         data = [{"sunday":sunday,"slot_Sunday":sundayslots},
    #                 {"monday":monday,"slot_monday":mondayslots},
    #                 {"tuesday":tuesday,"slot_tuesday":tuesdayslots},
    #                 {"wednesday":wednesday,"slot_wednesday":wednesdaylots},
    #                 {"thursday":thursday,"slot_thursday":thursdayslots},
    #                 {"friday":friday,"slot_friday":fridayslots},
    #                 {"saturday":saturday,"slot_saturday":saturdayslots},
    #                 ]
    #         return data






# <--------------------------------------------------Temporary--------------------------------->








class FeaturedServiceListSerializer(ModelSerializer):
    name            = SerializerMethodField()
    profile_img     = SerializerMethodField()
    profile_views   = SerializerMethodField()
    location        = SerializerMethodField()
    completed_tasks = SerializerMethodField()
    avg_rating      = SerializerMethodField()
    bio             = SerializerMethodField()
    response_within = SerializerMethodField()
    type_of_tasker  = SerializerMethodField()
    services_offered = SerializerMethodField()
    # schedule     = SerializerMethodField()
    # provider_name  = SerializerMethodField()    
    user_ID     = SerializerMethodField()
    # service_id  = SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
                # 'service_id',
                'user',
                'user_ID',
                # 'provider_name',
                'name',
                'profile_img',
                'profile_views',
                'experience',
                'levelskill',
                # 'location',
                'distance_limit',
                'service_pricing',
                'pricing_timing_unit',
                'quote_at_request',
                'provide_tools',
                'tool_specify',
                'instant_booking',
                'avg_rating',
                'created',
                'service_name',
                'location',
                'completed_tasks',
                'avg_rating',
                'bio',
                'response_within',
                'type_of_tasker',
                'services_offered',
                # 'schedule'

            ]

    def get_service_id(self,instance):
        userObj = User.objects.get(id = instance.user.id)
        serviceObj = Service.objects.get(user =userObj)
        return serviceObj.id

    def get_user_ID(self,instance):
        return instance.user.id

    def get_name(self,instance):
        userObj = User.objects.get(id = instance.user.id)
        data = FirstNameSerializer(userObj).data
        return data

    def get_profile_img(self,instance):
        try:
            userObj = UserOtherInfo.objects.get(user = instance.user.id)
            data = UserProfileImageSerializer(userObj).data
            return data['profile_img']
        except UserOtherInfo.DoesNotExist:
            pass

    def get_profile_views(self,instance):
        try:
            userObj = UserOtherInfo.objects.get(user = instance.user.id)
            data = UserProfileDataSerializer(userObj).data
            return data['profile_views']
        except UserOtherInfo.DoesNotExist:
            pass

    def get_location(self,instance):
        try:
            userObj = UserOtherInfo.objects.get(user = instance.user.id)
            data = UserProfileDataSerializer(userObj).data
            return data['location']
        except UserOtherInfo.DoesNotExist:
            pass

    def get_completed_tasks(self,instance):

        try:
            userObj = UserOtherInfo.objects.get(user = instance.user.id)
            data = UserProfileDataSerializer(userObj).data
            return data['completed_tasks']
        except UserOtherInfo.DoesNotExist:
            pass

    def get_avg_rating(self,instance):
        try:
            userObj = UserOtherInfo.objects.get(user = instance.user.id)
            data = UserProfileDataSerializer(userObj).data
            return data['avg_rating']
        except UserOtherInfo.DoesNotExist:
            pass

    def get_bio(self,instance):
        try:
            userObj = UserOtherInfo.objects.get(user = instance.user.id)
            data = UserOtherInfoSerializer(userObj).data
            return data['bio']
        except UserOtherInfo.DoesNotExist:
            pass

    def get_response_within(self,instance):
        try:
            userObj = UserOtherInfo.objects.get(user = instance.user.id)
            data = UserOtherInfoSerializer(userObj).data
            return data['response_within']
        except UserOtherInfo.DoesNotExist:
            pass

    def get_type_of_tasker(self,instance):
        try:
            userObj = UserOtherInfo.objects.get(user = instance.user.id)
            data = UserOtherInfoSerializer(userObj).data
            return data['type_of_tasker']
        except UserOtherInfo.DoesNotExist:
            pass

    def get_services_offered(self,instance):
        qs = Service.objects.filter(user = instance.user.id)
        # total_bookings = RawBooking.objects.filter(provider=instance.user.id)
        data = ServiceSerializer(qs,many = True).data
        return data        



    # def get_schedule(self,instance):

    #         daysObj = days.objects.get(Service = instance.id)
    #         daysdata = SheduleListSerializer(daysObj).data
    #         sunday = daysdata['Sunday']
    #         monday = daysdata['Monday']
    #         tuesday = daysdata['Tuesday']
    #         wednesday = daysdata['Wednesday']
    #         thursday  = daysdata['Thursday']
    #         friday    = daysdata['Friday']
    #         saturday  = daysdata['Saturday']
    #         sundayqs   = Slots.objects.filter(service = instance.id,day="Sunday")
    #         sundayslots = SlotListSerializer(sundayqs,many=True).data
    #         mondayqs   = Slots.objects.filter(service = instance.id,day="Monday")
    #         mondayslots = SlotListSerializer(mondayqs,many=True).data
    #         tuesdayqs   = Slots.objects.filter(service = instance.id,day="Tuesday")
    #         tuesdayslots = SlotListSerializer(tuesdayqs,many=True).data
    #         wednesdayqs   = Slots.objects.filter(service = instance.id,day="Wednesday")
    #         wednesdaylots = SlotListSerializer(wednesdayqs,many=True).data
    #         thursdayqs   = Slots.objects.filter(service = instance.id,day="Thursday")
    #         thursdayslots = SlotListSerializer(thursdayqs,many=True).data
    #         fridayqs   = Slots.objects.filter(service = instance.id,day="Friday")
    #         fridayslots = SlotListSerializer(fridayqs,many=True).data
    #         saturdayqs   = Slots.objects.filter(service = instance.id,day="Saturday")
    #         saturdayslots = SlotListSerializer(saturdayqs,many=True).data
    #         data = [{"sunday":sunday,"slot_Sunday":sundayslots},
    #                 {"monday":monday,"slot_monday":mondayslots},
    #                 {"tuesday":tuesday,"slot_tuesday":tuesdayslots},
    #                 {"wednesday":wednesday,"slot_wednesday":wednesdaylots},
    #                 {"thursday":thursday,"slot_thursday":thursdayslots},
    #                 {"friday":friday,"slot_friday":fridayslots},
    #                 {"saturday":saturday,"slot_saturday":saturdayslots},
    #                 ]
    #         return data

    # def get_provider_name(self,instance):
    #     userObj = User.objects.get(id = instance.user.id)
    #     first_name = userObj.GET.get('first_name')
    #     last_name = userObj.GET.get('last_name')
    #     providerName = str(first_name + " " + last_name)
    #     return providerName



class FeaturedProvidersSerializers(ModelSerializer):
    class Meta:
        model = FeaturedProviders
        fields = '__all__'
    
class TrendingProvidersSerializers(ModelSerializer):
    class Meta:
        model = TrendingProviders
        fields = '__all__'

class MostRecentProvidersSerializers(ModelSerializer):
    class Meta:
        model = MostRecentProviders
        fields = '__all__'

class RawBookingCreateSerializers(ModelSerializer):
    available_service_Chosen = SerializerMethodField()
    class Meta:
        model = RawBooking
        fields = [
            'provider',
            'available_service_Chosen',
            'appointment_city',
            'appointment_venue',
            # 'appointment_gio_location',
            'description',
        ]





class RawBookingCreateSerializersTemp(ModelSerializer):
    # available_service_Chosen = SerializerMethodField()
    class Meta:
        model = RawBooking
        fields = [
            'provider_name',
            'service_name',
            'appointment_city',
            'appointment_venue',
            # 'appointment_gio_location',
            'description',
        ]








# class BookingSerializer(ModelSerializer):

#     # service = SlugRelatedField(
#     #     many=True,
#     #     read_only=True,
#     #     slug_field='service_name'
#     # )

#     service = SerializerMethodField()

#     requester_city = SlugRelatedField(
#         many=True,
#         read_only=True,
#         slug_field='city'
#     )

#     class Meta:
#         model = Bookings
#         fields = [
#             # 'provider',
#             # 'requester',
#             'requester_city',
#             # 'category',
#             # 'sub_category',
#             'service',
#             'task_status',
#             'booking_status',
#             'created',
#             'modified'
#         ]


#     def get_service(self,instance):
#         data = ServiceSerializer(instance)
#         return data

# class RawBookingCreateSerializersTemp(ModelSerializer):
#     class Meta:
#         model = RawBookingTemp
#         fields = '__all__'


class MyBookingListSerializer(ModelSerializer):
    class Meta:
        model = RawBooking
        fields = [
            'available_service_Choosed',
            'appointment_city',
            'appointment_venue',
            'appointment_gio_location',
            'description',
            'isaccepted_by_provider',
            'created',
            'time_taken_accepting',
            'accepted_time',
            'ispaymentadd',
            'paymentaddtime',
            'isbookingcompleted'
        ]

class BookingSummaryListSerializer(ModelSerializer):
    mybookings = SerializerMethodField()
    class Meta:
        model = RawBooking
        fields = [
            'mybookings',
        ]
    
    def get_mybookings(self,instance):
        qs = RawBooking.objects.filter(requester = instance)
        data = MyBookingListSerializer(qs,many = True).data
        return data

class MyCanceledBookingsListSerializer(ModelSerializer):
    class Meta:
        model = CanceledBooking
        fields = [
            'rawbooking_id',
            'canceled_by',
            'cancel_date',
        ]

class RequestorCancelBookingsListSerializer(ModelSerializer):
    mycanceledbookings = SerializerMethodField()
    class Meta:
        model = CanceledBooking
        fields = [
            'mycanceledbookings',
        ]
    
    def get_mycanceledbookings(self,instance):
        qs = CanceledBooking.objects.filter(canceled_by = instance)
        data = MyCanceledBookingsListSerializer(qs,many = True).data
        return data

class RawBookingListSerializer(ModelSerializer):
    rating      = SerializerMethodField()
    userimage   = SerializerMethodField()
    subcategory = SerializerMethodField()
    pricing     = SerializerMethodField()
    service_name = SerializerMethodField()
    unit         = SerializerMethodField()
    name         = SerializerMethodField()
    class Meta:
        model = RawBooking
        fields = [
            'rating',
            'userimage',
            'date',
            'subcategory',
            'pricing',
            'service_name',
            'unit',
            'name'
        ]
    def get_userimage(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.provider)
        image = userObj.profile_img
        return ("/media/" + str(image))
    def get_rating(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.provider)
        rating = userObj.avg_rating
        return rating
    def get_pricing(self,instance):
        instanceid = instance.service.id
        serviceObj = Service.objects.get(id = instanceid)
        pricing = serviceObj.service_pricing
        return pricing
    def get_subcategory(self,instance):
        instanceid = instance.service.id
        serviceObj = Service.objects.get(id = instanceid)
        subcategory = serviceObj.subcategory
        return str(subcategory)
    def get_service_name(self,instance):
        instanceid = instance.service.id
        serviceObj = Service.objects.get(id = instanceid)
        service_name = serviceObj.service_name
        return service_name
    def get_unit(self,instance):
        instanceid = instance.service.id
        serviceObj = Service.objects.get(id = instanceid)
        pricing_timing_unit = serviceObj.pricing_timing_unit
        return pricing_timing_unit
    def get_name(self,instance):
        userObj = User.objects.get(id = instance.provider.id)
        name = str(userObj.first_name) + str(userObj.last_name)
        return name





# <----------------------------------Temp-----------------VVVVVVVVVVVVVVVVV--------------------->


class RawBookingListSerializerTemp(ModelSerializer):
    rating      = SerializerMethodField()
    userimage   = SerializerMethodField()
    # subcategory = SerializerMethodField()
    pricing     = SerializerMethodField()
    # service_name = SerializerMethodField()
    # unit         = SerializerMethodField()
    # name         = SerializerMethodField()
    class Meta:
        model = RawBooking
        fields = [
            'rating',
            'userimage',
            'pricing',
            # 'date',
            # 'subcategory',
            # 'service_name',
            # 'unit',
            # 'name'
        ]
    def get_userimage(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.provider)
        image = userObj.profile_img
        print("<-------------------------INstance Userimage----------------->",instance)
        return ("/media/" + str(image))
    def get_rating(self,instance):
        userObj = UserOtherInfo.objects.get(user = instance.provider)
        rating = userObj.avg_rating
        print("<-------------------------INstance Rating----------------->",instance.service.id)
        return rating
    def get_pricing(self,instance):
        instanceid = instance.service.id
        serviceObj = Service.objects.get(id = instanceid)
        print("<-------------------------Instance Pricing----------------->",instanceid)
        pricing = serviceObj.service_pricing
        return pricing
    # def get_subcategory(self,instance):
    #     serviceObj = Service.objects.get(id = instance.service.id)
    #     subcategory = serviceObj.subcategory
    #     return str(subcategory)
    # def get_service_name(self,instance):
    #     serviceObj = Service.objects.get(id = instance.service.id)
    #     service_name = serviceObj.service_name
    #     return service_name
    # def get_unit(self,isinstance):
    #     serviceObj = Service.objects.get(id = instance.service.id)
    #     pricing_timing_unit = serviceObj.pricing_timing_unit
    #     return pricing_timing_unit
    def get_name(self,instance):
        userObj = User.objects.get(id = instance.provider.id)
        name = str(userObj.first_name) + str(userObj.last_name)
        return name


# <----------------------------------------------TEMP-_------------------^^^^^^^^^^^^^^_--------------->



class DynamicSerializer(ModelSerializer):

    def to_representation(self, obj):
        # get the original representation
        ret = super(DynamicSerializer, self).to_representation(obj)

        # remove 'url' field if mobile request
        # if is_mobile_platform(self.context.get('request', None)):
        #     ret.pop('url')

        # here write the logic to check whether `elements` field is to be removed 
        # pop 'elements' from 'ret' if condition is True
        if(ret['Option3'] == "Default"):
            # print("<----------------data option 3--------------->",ret.dat['Option3'])
            ret.pop('Option3')

        # return the modified representation
        return ret 

class OptionSerializer(DynamicSerializer):
    # Option3 = SerializerMethodField()
    # Option3 = serializers.CharField(source='Option3')
    class Meta:
        model = OptionsFilledbyAdmin
        fields = [
            'id'
            'Option1',
            'Option2',
            'Option3',
            # 'Option4'
        ]
        print("<------------------------Field-------------------->",fields[1])
        # if(fields[2] is None):

    # def get_Option3(self,instance):
    #     if (str(instance.Option3) != 'Default'):
    #         return Option3

    # def to__representation(self,data):
    #     if data is not N

    # def to_representation(self, instance):
    #     """
    #     Object instance -> Dict of primitive datatypes.
    #     """
    #     ret = collections.OrderedDict()
    #     fields = self._readable_fields

    #     for field in fields:
    #         try:
    #             attribute = field.get_attribute(instance)
    #         except SkipField:
    #             continue

    #         # KEY IS HERE:
    #         if attribute in [None, '', 'Default']:
    #             continue

    #         # We skip `to_representation` for `None` values so that fields do
    #         # not have to explicitly deal with that case.
    #         #
    #         # For related fields with `use_pk_only_optimization` we need to
    #         # resolve the pk value.
    #         check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
    #         if check_for_none is None:
    #             ret[field.field_name] = None
    #         else:
    #             ret[field.field_name] = field.to_representation(attribute)

    #     return ret


#Arabic clone
class OptionArabicSerializer(ModelSerializer):
    Option1 = SerializerMethodField()
    Option1_english = SerializerMethodField()


    def get_Option1(self,instance):
        return instance.Option1_in_arabic
    

    def get_Option1_english(self,instance):
        return instance.Option1


    class Meta:
        model = OptionsFilledbyAdmin
        fields = [
            'id',
            'Option1',
            'Option1_english',
            'Option2_in_arabic',
            'Option3_in_arabic',
            # 'Option4_in_arabic'
        ]
class QuestionForRequestorListSerializer(ModelSerializer):
    options = SerializerMethodField()
    class Meta:
        model = QuestionFilledByAdmin
        fields = [
            'id',
            'question_for_requestor',
            'options',
            'Question_name'
        ]

    def get_options(self,instance):
        obj = OptionsFilledbyAdmin.objects.get(question = instance)
        serializer = OptionSerializer(obj).data
        return serializer

# Arabic clone
class QuestionForRequestorListArabicSerializer(ModelSerializer):
    options = SerializerMethodField()
    class Meta:
        model = QuestionFilledByAdmin
        fields = [
            'id',
            'question_for_requestor_in_arabic',
            'options',
            'Question_name_in_arabic'
        ]

    def get_options(self,instance):
        obj = OptionsFilledbyAdmin.objects.get(question = instance)
        serializer = OptionArabicSerializer(obj).data
        return serializer
        
class AnswerbyProviderCreateSerializer(ModelSerializer):
    class Meta:
        model = AnswerByProvider
        fields =[
            'user',
            'service',
            'question',
            'option_Selected',
            'question_string'
        ]
#Arabic clone
class AnswerbyProviderCreateArabicSerializer(ModelSerializer):
    class Meta:
        model = AnswerByProvider
        fields =[
            'user',
            'services',
            'question',
            'option_Selected_in_arabic'
        ]


class QuestionForProviderListSerializer(ModelSerializer):
    options = SerializerMethodField()
    class Meta:
        model = QuestionFilledByAdmin
        fields = [
            'id',
            'question_for_provider',
            'options'
        ]
    def get_options(self,instance):
        try:
            obj = OptionsFilledbyAdmin.objects.get(question = instance)
            serializer = OptionSerializer(obj).data
            return serializer
        except:
            return None



#arabic
class QuestionForProviderListArabicSerializer(ModelSerializer):
    options = SerializerMethodField()
    question_for_provider = SerializerMethodField()


    class Meta:
        model = QuestionFilledByAdmin
        fields = [
            'id',
            'question_for_provider',
            'options'
        ]
    def get_options(self,instance):
        obj = OptionsFilledbyAdmin.objects.get(question = instance)
        serializer = OptionArabicSerializer(obj).data
        return serializer
    
    def get_question_for_provider(self,instance):
        return instance.question_for_provider_in_arabic

class FilterServicesSubcategoryId(ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id'
        ]

class UserOtherInfoUpdate(ModelSerializer):
    name = SerializerMethodField()
    class Meta:
        model = UserOtherInfo
        fields = [
            'name',
            'bio',
            'idcard',
            'user_address',
            'phone'
        ]

    def get_name(self,instance):
        userObj = User.objects.get(id = instance.user.id)
        data = FirstNameSerializer(userObj).data
        return data
    



class UserFCMTokenUpdate(ModelSerializer):
    class Meta:
        model = UserOtherInfo
        fields = [
            'fcm_token'
        ]

class PaymentTokenAddSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'token',
            'bookingid'
        ]
class OngoingBookingCreateSerializer(ModelSerializer):
    class Meta:
        model = OngoingBooking
        fields = [
            'rawbooking_id',
            'requester',
            'provider'
        ]
class CompletedBookingCreateSerializer(ModelSerializer):
    class Meta:
        model = CompletedBooking
        fields = [
            'rawbooking_id'
        ]
class AnswerByProviderListSerializer(ModelSerializer):
    class Meta:
        model = AnswerByProvider
        fields = [
            'services',
            'question',
            'option_Selected'
            'user_name',
            'service_name',
            'question_string'
        ]
class SheduleCreateSerializer(ModelSerializer):
    class Meta:
        model = days
        fields = '__all__'


class SlotCreateSerializer(ModelSerializer):
    class Meta:
        model = Slots
        fields = '__all__'




class NewBookingSerializer(ModelSerializer):
    class Meta:
        model  = NewBookings
        fields = [
            'provider_id',
            'service_name',
            'appointment_city',
            'service_ID',
            'point_of_service',
            'booking_id'
        ]

class PendingActionsSerializer(ModelSerializer):
    profile_img = SerializerMethodField()
    quote_requested = SerializerMethodField()
    payment_mode = SerializerMethodField()
    provider_rating = SerializerMethodField()
#     service_location = SerializerMethodField()
    point_of_service = SerializerMethodField()
    city             = SerializerMethodField()
    service_date     = SerializerMethodField()
    service_time     = SerializerMethodField()
    price_rate		= SerializerMethodField()




    def get_profile_img(self,instance):
        # userObj = UserOtherInfo.objects.get(user = instance.requestor_id)
        print("<--------------Getting Profile Image-------------->")
        print("<---------------Instance-------------------->",instance)
        data = UserProfileImageSerializer(instance.requestor_id).data
        uoi_object_id = self.context.get('uoi_object_id')
        uoi_object = UserOtherInfo.objects.get(id=uoi_object_id)
        
        if uoi_object.usertype == "provider" or uoi_object.usertype == "Provider":
        	requestor_object = instance.requestor_id
        	profile_image = requestor_object.profile_image_s3
        	if profile_image == None or profile_image == "":
        		return ""
        	else:
        		return profile_image
        else:
        	provider_object = instance.provider_id
        	profile_image = provider_object.profile_image_s3
        	if profile_image == None or profile_image == "":
        		return ""
        	else:
        		return profile_image
        	
    
    def get_point_of_service(self,instance):
    	point_of_service = instance.point_of_service

    	return point_of_service
        	
        	
#         print("<-------------------Data fetched---------------------->",data)
#         if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
#             return ""
#         else:
#             return data['profile_image_s3']
    
    def get_quote_requested(self,instance):
    	NewBookingObject = NewBookings.objects.get(id=instance.id)
    	print("<------------New Booking Object Fetched------------------>",NewBookingObject)
    	if NewBookingObject.quote_requested_by_requestor == True:
    		return True
    	else:
    		return False
    	
    
    def get_city(self,instance):
    	point_of_service = instance.point_of_service
    	if point_of_service == "RequestorPlace" or "I travel to my customers":
    		return instance.appointment_city
    	else:
    		return ""
    	
    def get_payment_mode(self,instance):
    	NewBookingObject = NewBookings.objects.get(id=instance.id)
    	booking_id = NewBookingObject.booking_id
    	try:
    		LivePaymentObject = LivePayments.objects.get(booking_ID__exact = booking_id)
    		if LivePaymentObject.payment_method == "Cash":
    			return "Cash"
    		else:
    			return "Card"
    	except:
    		return ""
    
    def get_provider_rating(self,instance):
    	try:
    		provider_object = instance.provider_id
    		return provider_object.avg_rating
    	except:
    		return ""
    	
    	
   
    
    def get_service_date(self,instance):
    	NewBookingObject = NewBookings.objects.get(id=instance.id)
    	return NewBookingObject.service_date.strftime(EXTERNAL_DATE_FORMAT)
    
    def get_service_time(self,instance):
    	NewBookingObject = NewBookings.objects.get(id=instance.id)
    	return NewBookingObject.service_time.strftime(EXTERNAL_TIME_FORMAT)
    
    def get_price_rate(self,instance):
    	if instance.service_charge_rate == "" or instance.service_charge_rate == None:
    		return ""
    	else:
    		return instance.service_charge_rate
    	


			
    

    class Meta:
        model = NewBookings
        fields = [
            'booking_id',
            'requestor',
            'requestor_id',
            'provider',
            'provider_id',
            'profile_img',
            'service_ID',
            'service_name',
            'service_date',
            'service_time',
            'quote_requested',
            'payment_mode',
            'provider_rating',
            'point_of_service',
            'city',
            'service_charges',
            'admin_charges',
            'price_rate',
            'booking_marked_completed_by_requestor',
            'booking_marked_completed_by_provider',
            'auto_cancelled'

        ]


class ViewActiveBookingSerializer(ModelSerializer):
    profile_img = SerializerMethodField()
    payment_mode = SerializerMethodField()
    def get_payment_mode(self,instance):
        NewBookingObject = NewBookings.objects.get(id=instance.id)
        booking_id = NewBookingObject.booking_id
        try:
            LivePaymentObject = LivePayments.objects.get(booking_ID__exact = booking_id)
            if LivePaymentObject.payment_method == "Cash":
                return "Cash"
            else:
                return "Card"
        except:
            return ""   


   

    
    def get_profile_img(self,instance):
        # userObj = UserOtherInfo.objects.get(user = instance.requestor_id)
        print("<--------------Getting Profile Image-------------->")
        print("<---------------Instance-------------------->",instance)
        data = UserProfileImageSerializer(instance.requestor_id).data
        uoi_object_id = self.context.get('uoi_object_id')
        uoi_object = UserOtherInfo.objects.get(id=uoi_object_id)
        if uoi_object.usertype == "provider" or uoi_object.usertype == "Provider":
        	requestor_object = instance.requestor_id
        	profile_image = requestor_object.profile_image_s3
        	if profile_image == None or profile_image == "":
        		return ""
        	else:
        		return profile_image
        else:
        	provider_object = instance.provider_id
        	profile_image = provider_object.profile_image_s3
        	if profile_image == None or profile_image == "":
        		return ""
        	else:
        		return profile_image
# 
#         print("<-------------------Data fetched---------------------->",data)
#         if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
#             return ""
#         else:
#             return data['profile_image_s3']
    
    def get_provider_rating(self,instance):
    	try:
    		provider_object = instance.provider_id
    		return provider_object.avg_rating
    	except:
    		return ""
    
    def get_point_of_service(self,instance):
    	point_of_service = instance.point_of_service
    	return point_of_service
    
    
    def get_city(self,instance):
    	return instance.appointment_city
    
    

    	
    
         
# 	def get_provider_rating(self,instance):
# 		try:
# 			provider_object = instance.provider_id
# 			return provider_object.avg_rating
# 		except:
# 			return ""


    class Meta:
        model = NewBookings
        fields = [
            'booking_id',
            'requestor',
            'requestor_id',
            'provider',
            'provider_id',
            'profile_img',
            'service_ID',
            'service_name',
            'service_date',
            'service_time',
            'payment_mode',
            'provider_rating',
#             'service_place',
            'point_of_service',
            'city',
            'service_charges',
            'admin_charges',
			'booking_marked_completed_by_requestor',
			'booking_marked_completed_by_provider',
            'auto_cancelled'

        ]





class ViewBookingAcceptedSerializer(ModelSerializer):
    class Meta:
        model = NewBookings
        fields = '__all__'


class AcceptBookingSerializer(ModelSerializer):
    class Meta:
        model = NewBookings
        fields = '__all__'



class ViewCompletedTaskSerializer(ModelSerializer):
	profile_img  = SerializerMethodField()
	reviews      = SerializerMethodField()
	provider_rating = SerializerMethodField()
	point_of_service = SerializerMethodField()
	city = SerializerMethodField()
	service_date = SerializerMethodField()
	service_time = SerializerMethodField()
	price_rate = SerializerMethodField()
	booking_cancelled = SerializerMethodField()
	payment_mode	= SerializerMethodField()
	
	
	def get_reviews(self,instance):
		booking_id = instance.id
		print("<---------------------Completed Task Booking ID--------------------->",booking_id)
		try:
			ReviewQS = ServiceFeedback.objects.get(booking_id = booking_id)
			print("<---------------_Completed Task------------------>",ReviewQS)
			serializer = ServiceFeedbackSerializer(ReviewQS).data
			print("<-------------------Completed Task Serialized review------------------>",serializer)
			return serializer
		except:
			return ""
	

	def get_payment_mode(self,instance):
		NewBookingObject = NewBookings.objects.get(id=instance.id)
		booking_id = NewBookingObject.booking_id
		try:
			SettledPaymentObject = SettledPayments.objects.get(booking_ID__exact = booking_id)
			if SettledPaymentObject.payment_method == "Cash":
				return "Cash"
			else:
				return "Card"
		except:
			return ""

	
	
	
	def get_profile_img(self,instance):
		data = UserProfileImageSerializer(instance.requestor_id).data

		uoi_object_id = self.context.get('uoi_object_id')
		uoi_object = UserOtherInfo.objects.get(id=uoi_object_id)
		if uoi_object.usertype == "provider" or uoi_object.usertype == "Provider":
			requestor_object = instance.requestor_id
			profile_image = requestor_object.profile_image_s3
			if profile_image == None or profile_image == "":
				return ""
			else:
				return profile_image
		else:
			provider_object = instance.provider_id
			profile_image = provider_object.profile_image_s3
			if profile_image == None or profile_image == "":
				return ""
			else:
				return profile_image
		
# 		if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
# 			return ""
# 		else:
# 			return data['profile_image_s3']



	
	def get_provider_rating(self,instance):
		try:
			provider_object = instance.provider_id
			return provider_object.avg_rating
		except:
			return ""
	
	def get_point_of_service(self,instance):
		point_of_service = instance.point_of_service
		return point_of_service
	
	
	def get_city(self,instance):
		return instance.appointment_city
	
	
	def get_service_date(self,instance):
		return instance.service_date.strftime(EXTERNAL_DATE_FORMAT)
	
	def get_service_time(self,instance):
		return instance.service_time.strftime(EXTERNAL_TIME_FORMAT)
	
	def get_price_rate(self,instance):
		if instance.service_charge_rate == "" or instance.service_charge_rate == None:
			return ""
		else:
			return instance.service_charge_rate
		
	
	def get_booking_cancelled(self,instance):
		if instance.booking_cancelled == True:
			return True
		else:
			return False
			
	
	
	class Meta:
		model = NewBookings
		fields = [
			
			'booking_id',
			'requestor',
			'requestor_id',
			'provider',
			'provider_id',
			'profile_img',
			'service_ID',
			'service_name',
			'service_date',
			'service_time',
			'reviews',
			'provider_rating',
			'point_of_service',
			'city',
			'service_charges',
			'admin_charges',
			'price_rate',
			'booking_cancelled',
			'payment_mode',
			'booking_marked_completed_by_provider',
			'booking_marked_completed_by_requestor',
            'auto_cancelled'			
			]





class ImageUploadTestSerializer(ModelSerializer):
    class Meta:
        model = ImageUploadTest
        fields = '__all__'


class TempSerializer(ModelSerializer):
    class Meta:
        model = AnswerByProvider
        fields = '__all__'


class MarketingCarouselSerializer(ModelSerializer):
    class Meta:
        #model = MarketingCarousel
        model = BannerImage
        fields = '__all__'



class BookingListSerializer(ModelSerializer):

    class Meta:
        model = NewBookings
        fields = '__all__'


# class TrendingServiceListSerializer(ModelSerializer):
#     name            = SerializerMethodField()
#     profile_img     = SerializerMethodField()
#     profile_views   = SerializerMethodField()
#     location        = SerializerMethodField()
#     completed_tasks = SerializerMethodField()
#     avg_rating      = SerializerMethodField()
#     bio             = SerializerMethodField()
#     response_within = SerializerMethodField()
#     type_of_tasker  = SerializerMethodField()
#     services_offered = SerializerMethodField()
#     # schedule     = SerializerMethodField()
#     # provider_name  = SerializerMethodField()    
#     user_ID     = SerializerMethodField()
#     # service_id  = SerializerMethodField()
    
#     class Meta:
#         model = Service
#         fields = [
#                 # 'service_id',
#                 'user',
#                 'user_ID',
#                 # 'provider_name',
#                 'name',
#                 'profile_img',
#                 'profile_views',
#                 'experience',
#                 'levelskill',
#                 # 'location',
#                 'distance_limit',
#                 'service_pricing',
#                 'pricing_timing_unit',
#                 'quote_at_request',
#                 'provide_tools',
#                 'tool_specify',
#                 'instant_booking',
#                 'avg_rating',
#                 'created',
#                 'service_name',
#                 'location',
#                 'completed_tasks',
#                 'avg_rating',
#                 'bio',
#                 'response_within',
#                 'type_of_tasker',
#                 'services_offered',
#                 # 'schedule'

#             ]

#     def get_service_id(self,instance):
#         userObj = User.objects.get(id = instance.user.id)
#         serviceObj = Service.objects.get(user =userObj)
#         return serviceObj.id

#     def get_user_ID(self,instance):
#         return instance.user.id

#     def get_name(self,instance):
#         userObj = User.objects.get(id = instance.user.id)
#         data = FirstNameSerializer(userObj).data
#         return data

#     def get_profile_img(self,instance):
#         userObj = UserOtherInfo.objects.get(user = instance.user.id)
#         data = UserProfileImageSerializer(userObj).data
#         return data['profile_img']

#     def get_profile_views(self,instance):
#         userObj = UserOtherInfo.objects.get(user = instance.user.id)
#         data = UserProfileDataSerializer(userObj).data
#         return data['profile_views']

#     def get_location(self,instance):
#         userObj = UserOtherInfo.objects.get(user = instance.user.id)
#         data = UserProfileDataSerializer(userObj).data
#         return data['location']

#     def get_completed_tasks(self,instance):
#         userObj = UserOtherInfo.objects.get(user = instance.user.id)
#         data = UserProfileDataSerializer(userObj).data
#         return data['completed_tasks']

#     def get_avg_rating(self,instance):
#         userObj = UserOtherInfo.objects.get(user = instance.user.id)
#         data = UserProfileDataSerializer(userObj).data
#         return data['avg_rating']

#     def get_bio(self,instance):
#         userObj = UserOtherInfo.objects.get(user = instance.user.id)
#         data = UserOtherInfoSerializer(userObj).data
#         return data['bio']

#     def get_response_within(self,instance):
#         userObj = UserOtherInfo.objects.get(user = instance.user.id)
#         data = UserOtherInfoSerializer(userObj).data
#         return data['response_within']

#     def get_type_of_tasker(self,instance):
#         userObj = UserOtherInfo.objects.get(user = instance.user.id)
#         data = UserOtherInfoSerializer(userObj).data
#         return data['type_of_tasker'] 

#     def get_services_offered(self,instance):
#         qs = Service.objects.filter(user = instance.user.id)
#         # total_bookings = RawBooking.objects.filter(provider=instance.user.id)
#         data = ServiceSerializer(qs,many = True).data
#         return data        


class TrendingServiceListSerializer(ModelSerializer):
    services_offered = SerializerMethodField()
    name  = SerializerMethodField()
    instant_services = SerializerMethodField()
    other_services = SerializerMethodField()
    instant_booking = SerializerMethodField()
    user_ID     = SerializerMethodField()
    profile_img =   SerializerMethodField()
    background_image = SerializerMethodField()
    top_reviews = SerializerMethodField()
    

    class Meta:
        model = UserOtherInfo
        fields = [
            'name',
            'user_ID',
            'phone',
            'response_within',
            'avg_rating',
            'location',
            'created',
            'type_of_tasker',
            'bio',
            'completed_tasks',
            'current_language',
            'profile_img',
            'usertype',
            'city',
            'location',
            'services_offered',
            'instant_booking',
            'instant_services',
            'other_services',
            'switched_to_provider',
            'user_address',
            'background_image',
            'locality',
            'user_address_lat',
            'user_address_long',
            'top_reviews'
        ]


    # def get_user_ID(self,instance):
    #     userObj   = User.objects.get(id=instance.user)
    #     return userObj.id

    def get_background_image(self,instance):
        userObj  = User.objects.get(id=instance.user.id)
        print("<---------------User Object------------------>")
        ServiceQS = Service.objects.filter(user=userObj)
        print("<-----------------ServiceQS------------>",ServiceQS)
        if len(ServiceQS) == 0:
            return ""
        else:
            ServiceObject = ServiceQS[0]
#             print("<-----------------Service Object------------->",ServiceObject)
#             print("<---------------Service Image being Sent--------------->",ServiceImageObject.service_img_file_1_s3)
            ServiceImageObject = ServiceImage.objects.get(service=ServiceObject)
            
            return ServiceImageObject.service_img_file_1_s3


    def get_profile_img(self,instance):
        print("<--------------Trending Instance----------------->",instance)
        data = UserProfileImageSerializer(instance).data
        if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
            return ""
        else:
            return data['profile_image_s3']
        # if instance.profile_image_s3 == None or instance.profile_image_s3 == "":
        #     return instance.profile_img
        # else:
        #     return instance.profile_image_s3

    def get_user_ID(self,instance):
        print("<--------------Instance------------->",instance)
        print("<--------------Instance.user---------->",instance.user)
        print("<--------------Instance.user.id------------>",instance.user.id)
        userObj   = User.objects.get(id=instance.user.id)
        return userObj.id


    def get_services_offered(self,instance):
        lang = self.context.get('lang')
        qs = Service.objects.filter(user = instance.user.id).filter(service_langugae=lang)
        # total_bookings = RawBooking.objects.filter(provider=instance.user.id)
        data = ServiceSerializer(qs,many = True).data
        return data    

    def get_name(self,instance):
        userObj = User.objects.get(id = instance.user.id)
        data = FirstNameSerializer(userObj).data
        return data

    def get_instant_services(self,instance):
        instant_services = Service.objects.filter(user=instance.user.id).filter(instant_booking = True)
        data = ServiceSerializer(instant_services,many=True).data
        return data
    
    def get_other_services(self,instance):
        other_services   = Service.objects.filter(user=instance.user.id).filter(instant_booking = False)
        data = ServiceSerializer(other_services,many=True).data
        return data

    def get_instant_booking(self,instance):
        if len(Service.objects.filter(user=instance.user.id).filter(instant_booking = True)) == 0:
            return False
        else:
            return True
    
    def get_top_reviews(self,instance):
    	user_object = instance.user
    	service_qs = Service.objects.filter(user=user_object)
    	if len(service_qs) == 0:
    		return []
    	else:
    		reviews_list = []
    		FinalQS = ServiceFeedback.objects.none()
    		for service in service_qs:
    			reviews = ServiceFeedback.objects.filter(service_id = service)
    			if len(reviews)!=0:
    				serializer = ServiceFeedbackSerializer(reviews,many=True).data
    				for review_object in serializer:
    					reviews_list.append(review_object)
    		
    		raw_reviews = []
    		for review in reviews_list:
    			tuple_object = (review['feedback_id'],review['rating'],review['feedback_date'],review['feedback_time'])
    			raw_reviews.append(tuple_object)
    			
    		
    		sorted_reviews = sorted(raw_reviews,key=itemgetter(1,2,3),reverse=True)[:3]
    		
    		review_id = [x[0] for x in sorted_reviews]
    		final_reviews = []
    		
    		for review_ref in review_id:
    			review_object  = ServiceFeedback.objects.get(id=review_ref)
    			review_serialized = ServiceFeedbackSerializer(review_object).data
    			final_reviews.append(review_serialized)
    		
    		return final_reviews
    
    


class FeaturedSerializerOld(ModelSerializer):
	services_offered	=	SerializerMethodField()
	instant_services	=	SerializerMethodField()
	other_services		=	SerializerMethodField()
	instant_booking		=	SerializerMethodField()
	name				=	SerializerMethodField()
	user_ID				=	SerializerMethodField()
	profile_img			=	SerializerMethodField()
	background_image	=	SerializerMethodField()
	top_reviews			=	SerializerMethodField()
	
	class Meta:
		model = UserOtherInfo
		fields = [
			'name',
			'phone',
			'user_ID',
			'avg_rating',
			'location',
			'created',
			'type_of_tasker',
			'bio',
			'instant_booking',
			'completed_tasks',
			'current_language',
			'profile_img',
			'usertype',
			'city',
			'location',
			'instant_services',
			'other_services',
			'services_offered',
			'switched_to_provider',
			'user_address',
			'background_image',
			'locality',
			'user_address_lat',
			'user_address_long',
			'top_reviews',
			]
		

	def get_services_offered(self,instance):
		qs = Service.objects.filter(user=instance.user.id)

		data = ServiceSerializer(qs,many=True).data
		return data


	def get_instant_services(self,instance):
		instant_services = Service.objects.filter(user=instance.user.id).filter(instant_booking = True)
		data = ServiceSerializer(instant_services,many=True).data
		return data
	
	def get_other_services(self,instance):
		other_services = Service.objects.filter(user=instance.user.id).filter(instant_booking=False)
		data = ServiceSerializer(other_services,many=True).data
		return data
	
	def get_instant_booking(self,instance):
		if len(Service.objects.filter(user=instance.user.id).filter(instant_booking=True))==0:
			return False
		else:
			return True
	
	def get_name(self,instance):
		userObj = User.objects.get(id=instance.user.id)
		data = FirstNameSerializer(userObj).data
		return data
	
	def get_user_ID(self,instance):
		userObj = User.objects.get(id=instance.user.id)
		return userObj.id
	
	def get_profile_img(self,instance):
		data = UserProfileImageSerializer(instance).data
		if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
			return ""
		else:
			return data['profile_image_s3']
	
	def get_background_image(self,instance):
		userObj = User.objects.get(id=instance.user.id)
		ServiceQS = Service.objects.filter(user=userObj)
		if len(ServiceQS) == 0:
			return ""
		else:
			ServiceObject = ServiceQS[0]
			# print("<------------------Background Image---------------->",ServiceImageObject.service_image_1_s3)
			ServiceImageObject =  ServiceImage.objects.get(service=ServiceObject)
			return ServiceImageObject.service_img_file_1_s3
	
	def get_top_reviews(self,instance):
		user_object = instance.user
		service_qs = Service.objects.filter(user=user_object)
# 		print("<---------------Service QS retreived------------------->",service_qs)
		if len(service_qs)==0:
			return []
		else:
			reviews_list = []
			FinalQS = ServiceFeedback.objects.none()
			for service in service_qs:
				reviews = ServiceFeedback.objects.filter(service_id=service)
# 				print("<---------------reviews--------------------->",type(reviews))
				if len(reviews)!=0:
					serializer = ServiceFeedbackSerializer(reviews,many=True).data
# 					print("<==============Serializer--------------------?",serializer)
					for review_object in serializer:
						reviews_list.append(review_object)
						
			
			raw_reviews = []
			for review in reviews_list:
				tuple_object = (review['feedback_id'],review['rating'],review['feedback_date'],review['feedback_time'])
				raw_reviews.append(tuple_object)
				
# 			print("<--------------Raw Reviews Tuple---------------->",raw_reviews)
			sorted_reviews = sorted(raw_reviews,key=itemgetter(1,2,3),reverse=True)[:3]
# 			print("<--------------Sorted Tuple------------------->",sorted_reviews)
			
			
			review_id = [x[0] for x in sorted_reviews]
	#		 for review in sorted_reviews:
	#			 review_id.append(review[0][0])
# 			print("<------------Review IDS---------------->",review_id)
			final_reviews = []
	
			
			
			
			for review_ref in review_id:
				review_object = ServiceFeedback.objects.get(id=review_ref)
# 				print("<----------------review object--------->",review_object)
				review_serialized = ServiceFeedbackSerializer(review_object).data
# 				print("<-----------------Review Serialized------------->",review_serialized)
				final_reviews.append(review_serialized)
				
# 			print("<============================>",final_reviews)
			return final_reviews
					
			
class MostRecentSerializer(ModelSerializer):
    services_offered = SerializerMethodField()
    instant_services = SerializerMethodField()
    other_services = SerializerMethodField()
    instant_booking = SerializerMethodField()
    name  = SerializerMethodField()
    user_ID = SerializerMethodField()
    profile_img =   SerializerMethodField()
    background_image = SerializerMethodField()
    top_reviews			=	SerializerMethodField()

    class Meta:
        model = UserOtherInfo
        fields = [
            'user_ID',
            'name',
            'phone',
            'response_within',
            'avg_rating',
            'location',
            'created',
            'type_of_tasker',
            'bio',
            'instant_booking',
            'completed_tasks',
            'current_language',
            'profile_img',
            'usertype',
            'city',
            'location',
            'instant_services',
            'other_services',
            'services_offered',
            'switched_to_provider',
            'user_address',
            'background_image',
            'locality',
            'user_address_lat',
            'user_address_long',
			'top_reviews'

        ]


    def get_background_image(self,instance):
        userObj  = User.objects.get(id=instance.user.id)
#         print("<---------------User Object------------------>")
        ServiceQS = Service.objects.filter(user=userObj)
#         print("<-----------------ServiceQS------------>",ServiceQS)
        if len(ServiceQS) == 0:
            return ""
        else:
            try:
                ServiceObject = ServiceQS[0]
                print("<-----------------Service Object------------->",ServiceObject)
                ServiceImageObject = ServiceImage.objects.get(service = ServiceObject)
                print("<---------------Service Image being Sent--------------->",ServiceImageObject.service_img_file_1_s3)
    # 			print("<------------------Background Image---------------->",ServiceObject.service_image_1_s3)
                return ServiceImageObject.service_img_file_1_s3
            except:
                return ""


    def get_profile_img(self,instance):
#         print("<--------------Trending Instance----------------->",instance)
        data = UserProfileImageSerializer(instance).data
        if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
            return ""
        else:
            return data['profile_image_s3']


    def get_name(self,instance):
        userObj = User.objects.get(id = instance.user.id)
        data = FirstNameSerializer(userObj).data
        return data
    
    def get_user_ID(self,instance):
#         print("<--------------Instance------------->",instance)
#         print("<--------------Instance.user---------->",instance.user)
#         print("<--------------Instance.user.id------------>",instance.user.id)
        userObj   = User.objects.get(id=instance.user.id)
        return userObj.id

    # def get_name(self,instance):
    #     print("<---------Instance------------->",instance)
    #     userObj = UserOtherInfo.objects.get(user = instance.user.id)
    #     print("<---------UserObj in serializer------------->",userObj)
    #     data = FirstNameSerializer(userObj).data
    #     return data
 

    # def get_services_offered(self,instance):
    #     instant_booking = False

    #     qs = Service.objects.filter(user = instance.user.id)
    #     instant_services = Service.objects.filter(user=instance.user.id).filter(instant_booking = True)
    #     other_services   = Service.objects.filter(user=instance.user.id).filter(instant_booking = False)
    #     if len(instant_services) != 0:
    #         instant_booking  = True
    #         instant_data = ServiceSerializer(instant_services,many=True).data

    #         if instant_data.is_valid():
    #             instant_data.validated_data['instant_booking'] = True
            
    #     # total_bookings = RawBooking.objects.filter(provider=instance.user.id)
    #     else:
    #         data =
    #     data = ServiceSerializer(qs,many = True).data
    #     return data          
    # 

    def get_instant_services(self,instance):
        instant_services = Service.objects.filter(user=instance.user.id).filter(instant_booking = True)
        data = ServiceSerializer(instant_services,many=True).data
        return data
    
    def get_other_services(self,instance):
        other_services   = Service.objects.filter(user=instance.user.id).filter(instant_booking = False)
        data = ServiceSerializer(other_services,many=True).data
        return data

    def get_instant_booking(self,instance):
        if len(Service.objects.filter(user=instance.user.id).filter(instant_booking = True)) == 0:
            return False
        else:
            return True           


    def get_services_offered(self,instance):
        lang = self.context.get('lang')
        print("<----------Language----------->",lang)
        qs = Service.objects.filter(user = instance.user.id).filter(service_langugae=lang)
        # total_bookings = RawBooking.objects.filter(provider=instance.user.id)
        data = ServiceSerializer(qs,many = True).data
        return data
       
    def get_top_reviews(self,instance):
    	user_object = instance.user
    	service_qs = Service.objects.filter(user=user_object)
#     	print("<------------------Service QS retreived----------------->",service_qs)
    	if len(service_qs) == 0:
    		return []
    	else:
    		
    		reviews_list = []
    		for service in service_qs:
    			reviews = ServiceFeedback.objects.filter(service_id=service)
#     			print("<----------------Reviews------------------->",type(reviews))
    			if len(reviews)!=0:
    				serializer = ServiceFeedbackSerializer(reviews,many=True).data
    				
    				for review_object in serializer:
    					reviews_list.append(review_object)
    		
    		
    		raw_reviews = []
    		for review in reviews_list:
    			tuple_object = (review['feedback_id'],review['rating'],review['feedback_date'],review['feedback_time'])
    			raw_reviews.append(tuple_object)
    			
    		
    		sorted_reviews = sorted(raw_reviews,key=itemgetter(1,2,3),reverse=True)[:3]
    		
    		review_id = [x[0] for x in sorted_reviews]
    		final_reviews = []
    		
    		for review_ref in review_id:
    			review_object = ServiceFeedback.objects.get(id=review_ref)
    			review_serialized = ServiceFeedbackSerializer(review_object).data
    			final_reviews.append(review_serialized)
    		
    		return final_reviews
    		
    		
#     		reviews_list = []
#     		for service in service_qs:
#     			reviews = ServiceFeedback.objects.filter
#     		
    		
    		
#     		FinalQS = ServiceFeedback.objects.none()
#     		for service in service_qs:
#     			reviews = ServiceFeedback.objects.filter(service_id=service)
#     			FinalQS.union(reviews)
#     		print("<-------------------Service Feedback QS-------------------->",FinalQS)
#     		SortedQS = FinalQS.order_by('-rating','-feedback_date','-feedback_time')[:3]
#     		print("<-------------------Sorted QS------------------------------->",SortedQS)
#     		data = ServiceFeedbackSerializer(SortedQS,many=True).data
#     		print("<-------------------Data being returned--------------------->",data)
#     		return data
    
#     def get_top_reviews(self,instance):
# 		user_object = instance.user
# 		service_qs = Service.objects.filter(user=user_object)
# 		print("<---------------Service QS retreived------------------->",service_qs)
# 		if len(service_qs)==0:
# 			return ""
# 		else:
# 			FinalQS = ServiceFeedback.objects.none()
# 			for service in service_qs:
# 				reviews = ServiceFeedback.objects.filter(service_id=service)
# 				FinalQS.union(reviews)
# 			print("<-------------Service Feedback QS------------------>",FinalQS)
# 			SortedQS = FinalQS.order_by('-rating','-feedback_date','-feedback_time')[:3]
# 			print("<--------------Sorted QS----------------------------->",SortedQS)
# 			data = ServiceFeedbackSerializer(SortedQS,many=True).data
# 			print("<----------------Data being returned------------------>",data)
# 			return data


# class MostRecentSerializer(ModelSerializer):
#     services_offered = SerializerMethodField()
#     instant_services = SerializerMethodField()
#     other_services = SerializerMethodField()
#     instant_booking = SerializerMethodField()
#     name  = SerializerMethodField()
#     user_ID = SerializerMethodField()
#     profile_img =   SerializerMethodField()
# 
#     class Meta:
#         model = UserOtherInfo
#         fields = [
#             'user_ID',
#             'name',
#             'phone',
#             'response_within',
#             'avg_rating',
#             'location',
#             'created',
#             'type_of_tasker',
#             'bio',
#             'instant_booking',
#             'completed_tasks',
#             'current_language',
#             'profile_img',
#             'usertype',
#             'city',
#             'location',
#             'instant_services',
#             'other_services',
#             'services_offered',
#             'switched_to_provider'
#         ]
# 
# 
#     def get_profile_img(self,instance):
#         print("<--------------Trending Instance----------------->",instance)
#         data = UserProfileImageSerializer(instance).data
#         if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
#             return data['profile_img']
#         else:
#             return data['profile_image_s3']
# 
# 
#     def get_name(self,instance):
#         userObj = User.objects.get(id = instance.user.id)
#         data = FirstNameSerializer(userObj).data
#         return data
#     
#     def get_user_ID(self,instance):
#         print("<--------------Instance------------->",instance)
#         print("<--------------Instance.user---------->",instance.user)
#         print("<--------------Instance.user.id------------>",instance.user.id)
#         userObj   = User.objects.get(id=instance.user.id)
#         return userObj.id
# 
#     # def get_name(self,instance):
#     #     print("<---------Instance------------->",instance)
#     #     userObj = UserOtherInfo.objects.get(user = instance.user.id)
#     #     print("<---------UserObj in serializer------------->",userObj)
#     #     data = FirstNameSerializer(userObj).data
#     #     return data
#  
# 
#     # def get_services_offered(self,instance):
#     #     instant_booking = False
# 
#     #     qs = Service.objects.filter(user = instance.user.id)
#     #     instant_services = Service.objects.filter(user=instance.user.id).filter(instant_booking = True)
#     #     other_services   = Service.objects.filter(user=instance.user.id).filter(instant_booking = False)
#     #     if len(instant_services) != 0:
#     #         instant_booking  = True
#     #         instant_data = ServiceSerializer(instant_services,many=True).data
# 
#     #         if instant_data.is_valid():
#     #             instant_data.validated_data['instant_booking'] = True
#             
#     #     # total_bookings = RawBooking.objects.filter(provider=instance.user.id)
#     #     else:
#     #         data =
#     #     data = ServiceSerializer(qs,many = True).data
#     #     return data          
#     # 
# 
#     def get_instant_services(self,instance):
#         instant_services = Service.objects.filter(user=instance.user.id).filter(instant_booking = True)
#         data = ServiceSerializer(instant_services,many=True).data
#         return data
#     
#     def get_other_services(self,instance):
#         other_services   = Service.objects.filter(user=instance.user.id).filter(instant_booking = False)
#         data = ServiceSerializer(other_services,many=True).data
#         return data
# 
#     def get_instant_booking(self,instance):
#         if len(Service.objects.filter(user=instance.user.id).filter(instant_booking = True)) == 0:
#             return False
#         else:
#             return True           
# 
# 
#     def get_services_offered(self,instance):
#         qs = Service.objects.filter(user = instance.user.id)
#         # total_bookings = RawBooking.objects.filter(provider=instance.user.id)
#         data = ServiceSerializer(qs,many = True).data
#         return data  




class SearchResultSerializer(ModelSerializer):	
    services_offered = SerializerMethodField()
    instant_services = SerializerMethodField()
    other_services = SerializerMethodField()
    instant_booking = SerializerMethodField()
    name  = SerializerMethodField()
    profile_img = SerializerMethodField()
    user_ID =SerializerMethodField()

    class Meta:
        model = UserOtherInfo
        fields = [
			'user_ID',
            'name',
            'phone',
            'response_within',
            'avg_rating',
            'location',
            'created',
            'type_of_tasker',
            'bio',
            'instant_booking',
            'completed_tasks',
            'current_language',
            'profile_img',
            'usertype',
            'city',
            'location',
            'instant_services',
            'other_services',
            'services_offered',
            'switched_to_provider',
            'locality',
            'user_address',
            'user_address_lat',
            'user_address_long'
        ]



    def get_profile_img(self,instance):
        print("<--------------Trending Instance----------------->",instance)
        data = UserProfileImageSerializer(instance).data
        if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
            return ""
        else:
            return data['profile_image_s3']


    def get_name(self,instance):
        userObj = User.objects.get(id = instance.user.id)
        data = FirstNameSerializer(userObj).data
        return data
       
    def get_user_ID(self,instance):
        print("<--------------Instance------------->",instance)
        print("<--------------Instance.user---------->",instance.user)
        print("<--------------Instance.user.id------------>",instance.user.id)
        userObj   = User.objects.get(id=instance.user.id)
        return userObj.id
    

    # def get_name(self,instance):
    #     print("<---------Instance------------->",instance)
    #     userObj = UserOtherInfo.objects.get(user = instance.user.id)
    #     print("<---------UserObj in serializer------------->",userObj)
    #     data = FirstNameSerializer(userObj).data
    #     return data
 

    # def get_services_offered(self,instance):
    #     instant_booking = False

    #     qs = Service.objects.filter(user = instance.user.id)
    #     instant_services = Service.objects.filter(user=instance.user.id).filter(instant_booking = True)
    #     other_services   = Service.objects.filter(user=instance.user.id).filter(instant_booking = False)
    #     if len(instant_services) != 0:
    #         instant_booking  = True
    #         instant_data = ServiceSerializer(instant_services,many=True).data

    #         if instant_data.is_valid():
    #             instant_data.validated_data['instant_booking'] = True
            
    #     # total_bookings = RawBooking.objects.filter(provider=instance.user.id)
    #     else:
    #         data =
    #     data = ServiceSerializer(qs,many = True).data
    #     return data          
    # 

    def get_instant_services(self,instance):
        instant_services = Service.objects.filter(user=instance.user.id).filter(instant_booking = True)
        data = ServiceSerializer(instant_services,many=True).data
        return data
    
    def get_other_services(self,instance):
        other_services   = Service.objects.filter(user=instance.user.id).filter(instant_booking = False)
        data = ServiceSerializer(other_services,many=True).data
        return data

    def get_instant_booking(self,instance):
        if len(Service.objects.filter(user=instance.user.id).filter(instant_booking = True)) == 0:
            return False
        else:
            return True           


    def get_services_offered(self,instance):
        lang = self.context.get('lang')
        qs = Service.objects.filter(user = instance.user.id).filter(service_langugae=lang)
        # total_bookings = RawBooking.objects.filter(provider=instance.user.id)
        data = ServiceSerializer(qs,many = True).data
        return data  



class SelfServiceSerializer(ModelSerializer):
    services_offered = SerializerMethodField()
    top_reviews = SerializerMethodField()
	
    class Meta:
        model = UserOtherInfo
        fields = [
            'services_offered',
            'top_reviews'
        ]

    def get_services_offered(self,instance):
        qs = Service.objects.filter(user = instance.user.id).order_by('-created')
        # total_bookings = RawBooking.objects.filter(provider=instance.user.id)
        data = ServiceSerializer(qs,many = True).data
        return data
    
    
    def get_top_reviews(self,instance):
    	
    	user_object = instance.user
    	service_qs = Service.objects.filter(user=user_object)
    	if len(service_qs) == 0:
    		return []
    	else:
    		reviews_list =[]
    		FinalQS = ServiceFeedback.objects.none()
    		for service in service_qs:
    			reviews = ServiceFeedback.objects.filter(service_id =  service)
    			if len(reviews)!=0:
    				serializer = ServiceFeedbackSerializer(reviews,many=True).data
    				for review_object in serializer:
    					reviews_list.append(review_object)
    		
    		raw_reviews = []
    		for review in reviews_list:
    			tuple_object = (review['feedback_id'],review['rating'],review['feedback_date'],review['feedback_time'])
    			raw_reviews.append(tuple_object)
    			
    		
    		sorted_reviews = sorted(raw_reviews,key=itemgetter(1,2,3),reverse=True)[:3]
    		
    		review_id = [x[0] for x in sorted_reviews]
    		final_reviews  = []
    		
    		for review_ref in review_id:
    			review_object = ServiceFeedback.objects.get(id=review_ref)
    			review_serialized = ServiceFeedbackSerializer(review_object).data
    			final_reviews.append(review_serialized)
    		
    		return final_reviews
    		
    	
#     	return []
       
       
       #     def get_top_reviews(self,instance):
# 		user_object = instance.user
# 		service_qs = Service.objects.filter(user=user_object)
# 		if len(service_qs) == 0:
# 			return []
# 		else:
# 			reviews_list = []
# 			FinalQS = ServiceFeedback.objects.none()
# 			for service in service_qs:
# 				reviews = ServiceFeedback.objects.filter(service_id = service)
# 				if len(reviews)!=0:
# 					serializer = ServiceFeedbackSerializer(reviews,many=True).data
# 					for review_object in serializer:
# 						reviews_list.append(review_object)
# 			
# 			raw_reviews = []
# 			for review in reviews_list:
# 				tuple_object = (review['feedback_id'],review['rating'],review['feedback_date'],review['feedback_time'])
# 				raw_reviews.append(tuple_object)
# 				
# 			
# 			sorted_reviews = sorted(raw_reviews,key=itemgetter(1,2,3),reverse=True)[:3]
# 			
# 			review_id = [x[0] for x in sorted_reviews]
# 			final_reviews = []
# 			
# 			for review_ref in review_id:
# 				review_object  = ServiceFeedback.objects.get(id=review_ref)
# 				review_serialized = ServiceFeedbackSerializer(review_object).data
# 				final_reviews.append(review_serialized)
# 			
# 			return final_reviews




class ServiceNameSerializer(ModelSerializer):


    class Meta:
        model = Service
        fields = [
            'service_name'
        ]






    
class SearchSerializer(ModelSerializer):
    name = SerializerMethodField()
    services_offered = SerializerMethodField()

    class Meta:   
        model = UserOtherInfo
        fields = [
            'name',
            'services_offered'
        ]

    def get_name(self, instance):
        userObj = User.objects.get(id = instance.user.id)
        return userObj.get_full_name()

    def get_services_offered(self,instance):
        qs  = Service.objects.filter(user = instance.user.id)
        data = ServiceNameSerializer(qs,many=True).data
        return data




class NotificationSerializer(ModelSerializer):
    profile_img = SerializerMethodField()
    notification_date = SerializerMethodField()
    notification_time = SerializerMethodField()
    


    def get_profile_img(self,instance):
        # userObj = UserOtherInfo.objects.get(user = instance.requestor_id)
        data = UserProfileImageSerializer(instance.from_user_id).data
        print("<-------------------Data fetched---------------------->",data)
        if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
            return ""
        else:
            return data['profile_image_s3']
    
    def get_notification_date(self,instance):
    	return instance.notification_date.strftime(EXTERNAL_DATE_FORMAT)
    
    def get_notification_time(self,instance):
    	return instance.notification_time.strftime(EXTERNAL_TIME_FORMAT)
    	



    class Meta:
        model = InAppBookingNotifications
        fields = [
			'id',
            'from_user_id',
            'from_user_name',
            'to_user_name',
            'notification_type',
            'service_name',
            'notification_title',
            'service_slot_start',
            'service_slot_end',
            'requested_service_time',
            'requested_service_date',
            'notification_time',
            'notification_date',
            'service_pricing',
            'service_place',
            'notification_read',
            'profile_img'
        ]
        


class SavedCardSerializer(ModelSerializer):
	class Meta:
		model = BankingInfo
		fields = [
			'id',
			'card_holder_name',
			'credit_card_masked',
			'credit_card_number',
			'valid_upto',
			]
 
 
 
 
 
class ServiceFeedbackSerializer(ModelSerializer):
 	
 	feedback_id  = SerializerMethodField()
 	feedback_user_image = SerializerMethodField()
 	feedback_user_name = SerializerMethodField()
 	
 	def get_feedback_id(self,instance):
 		return instance.id
 	
 	
 	def get_feedback_user_image(self,instance):
 		try:
 			booking_id = instance.booking_id
 			BookingObject = NewBookings.objects.get(booking_id__exact = booking_id)
 			RequestorObject = BookingObject.requestor_id
 			
 			if RequestorObject.profile_image_s3 == "" or None:
 				return ""
 			else:
  				return RequestorObject.profile_image_s3
 		except:
 			return ""
 	
 	def get_feedback_user_name(self,instance):
 		try:
 			feedback_uoi = instance.feedback_user
 			feedback_user_object = feedback_uoi.user
 			return feedback_user_object.get_full_name()
 		except:
 			return ""
 			
 		
 	
 	

 
 	
 	class Meta:
 		model = ServiceFeedback
 		fields = [
			'feedback_id',
			'booking_id',
			'service_id',
			'rating',
			'compliment',
			'review',
			'feedback_date',
			'feedback_time',
# 			'marked_for_moderation',
			'feedback_user_image',
			'feedback_user_name'
			]
 		
 			
  
class LegalTextSerializer(ModelSerializer):
  	
	class Meta:
		model = ContentMaster
		fields = [
			'title',
			'legal_text',
            'content',
            'content_in_arabic'
			]
  		
  		
  		
 
class OptionSerializer(ModelSerializer):
	option_id = SerializerMethodField()
	
	
	class Meta:
		 model = OptionsFilledbyAdmin
		 fields = [
			'option_id',
			'Option1'
			]
		 
	def get_option_id(self,instance):
		return instance.id
 
  		
  
 
 
# class question_for_provider_serialzer(ModelSerializer):
#     question_id = SerializerMethodField()
#     options = SerializerMethodField()
#     class Meta:
# 		model = QuestionFilledByAdmin
# 		fields = [
# 			'question_id',
# 			'service',
# 			'category',
# 			'SubCategory',
# 			'question_for_provider',
# 			'options',
# 			'question_tag',
# 			'Question_name'
			
# 			]

#     def get_question_id(self,instance):
#         return instance.id

# 	def get_options(self,instance):
		
# 		OptionQS = OptionsFilledbyAdmin.objects.filter(question=instance.id)
# 		OptionSerialized = OptionSerializer(OptionQS,many=True).data
# 		return OptionSerialized
	



class question_for_provider_serialzer(ModelSerializer):

    question_id = SerializerMethodField()
    options = SerializerMethodField()
    class Meta:
        model = QuestionFilledByAdmin
        fields = [
            'question_id',
            'service',
            'category',
            'SubCategory',
            'question_for_provider',
            'options',
            'question_tag',
            'Question_name'
        ]

    def get_question_id(self,instance):
        return instance.id

    def get_options(self,instance):

        OptionQS = OptionsFilledbyAdmin.objects.filter(question=instance.id)
        OptionSerialized = OptionSerializer(OptionQS,many=True).data
        return OptionSerialized



class question_for_provider_serializer_arabic(ModelSerializer):

    options = SerializerMethodField()
    question_id = SerializerMethodField()
    question_for_provider = SerializerMethodField()
    Question_name = SerializerMethodField()

    class Meta:
        model = QuestionFilledByAdmin
        fields = [
            'question_id',
            'service',
            'category',
            'SubCategory',
            'question_for_provider',
            'options',
            'question_tag',
            'Question_name'
        ]
    
    def get_options(self,instance):

        OptionQS = OptionsFilledbyAdmin.objects.filter(question=instance.id)
        OptionSerialized = OptionArabicSerializer(OptionQS,many=True).data
        return OptionSerialized


    def get_question_id(self,instance):
        return instance.id
    

    def get_question_for_provider(self,instance):
        return instance.question_for_provider_in_arabic
    
    def get_Question_name(self,instance):
        return instance.Question_name_in_arabic




class question_for_requestor_serialzer(ModelSerializer):

    question_id = SerializerMethodField()
    options = SerializerMethodField()
    question_for_requestor = SerializerMethodField()


    class Meta:
        model = QuestionFilledByAdmin
        fields = [
            'question_id',
            'service',
            'category',
            'SubCategory',
            'question_for_requestor',
            'options',
            'question_tag',
            'Question_name'
        ]

    def get_question_id(self,instance):
        return instance.id

    def get_options(self,instance):

        OptionQS = OptionsFilledbyAdmin.objects.filter(question=instance.id)
        OptionSerialized = OptionSerializer(OptionQS,many=True).data
        return OptionSerialized
    
    def get_question_for_requestor(self,instance):
        return instance.question_for_requestor




class question_for_requestor_serializer_arabic(ModelSerializer):

    options = SerializerMethodField()
    question_id = SerializerMethodField()
    question_for_requestor = SerializerMethodField()
    Question_name = SerializerMethodField()

    class Meta:
        model = QuestionFilledByAdmin
        fields = [
            'question_id',
            'service',
            'category',
            'SubCategory',
            'question_for_requestor',
            'options',
            'question_tag',
            'Question_name'
        ]
    
    def get_options(self,instance):

        OptionQS = OptionsFilledbyAdmin.objects.filter(question=instance.id)
        OptionSerialized = OptionArabicSerializer(OptionQS,many=True).data
        return OptionSerialized


    def get_question_id(self,instance):
        return instance.id
    
    def get_question_for_requestor(self,instance):
        return instance.question_for_requestor_in_arabic


    def get_Question_name(self,instance):
        return instance.Question_name_in_arabic






# class question_for_provider_serialzer_arabic(ModelSerializer):
	
# 	options = SerializerMethodField()
#     question_id = SerializerMethodField()
# 	question_for_provider = SerializerMethodField()

	
# 	class Meta:
# 		model = QuestionFilledByAdmin
# 		fields = [
# 			'question_id',
# 			'service',
# 			'category',
# 			'SubCategory',
# 			'question_for_provider',
# 			'options',
# 			'question_tag',
# 			'Question_name'
			
# 			]
		
# 	def get_options(self,instance):
		
# 		OptionQS = OptionsFilledbyAdmin.objects.filter(question=instance.id)
# 		OptionSerialized = OptionArabicSerializer(OptionQS,many=True).data
# 		return OptionSerialized
	
# 	def get_question_for_provider(self,instance):
# 		return instance.question_for_provider_in_arabic



	

# class question_for_requestor_serialzer(ModelSerializer):
	
# 	options = SerializerMethodField()

# 	class Meta:
# 		model = QuestionFilledByAdmin
# 		fields = [
# 			'question_id',
# 			'service',
# 			'category',
# 			'SubCategory',
# 			'question_for_requestor',
# 			'options',
# 			'question_tag',
# 			'Question_name'
			
# 			]
		
# 	def get_options(self,instance):
		
# 		OptionQS = OptionsFilledbyAdmin.objects.filter(question=instance.id)
# 		OptionSerialized = OptionSerializer(OptionQS,many=True).data
# 		return OptionSerialized
	



# class question_for_requestor_serializer_arabic(ModelSerializer):

#     options = SerializerMethodField()
#     question_for_requestor = SerializerMethodField()

#     def get_question_for_requestor(self,instance):
#         return instance.question_for_requestor_in_arabic


#     def get_options(self,instance):
#         OptionQS = OptionsFilledbyAdmin.objects.filter(question=instance.id)
#         OptionSerialized = OptionArabicSerializer(OptionQS,many=True).data
#         return OptionSerialized


#     class Meta:
#         model = QuestionFilledByAdmin
#         fields = [
#             'question_id',
#             'service',
#             'category',
#             'SubCategory',
#             'question_for_requestor',
#             'options',
#             'question_tag',
#             'Question_name'

#         ]



class FilteredProviderSerializerOld(ModelSerializer):
	services_offered	=	SerializerMethodField()
	instant_services	=	SerializerMethodField()
	other_services		=	SerializerMethodField()
	instant_booking		=	SerializerMethodField()
	name				=	SerializerMethodField()
	user_ID				=	SerializerMethodField()
	profile_img			=	SerializerMethodField()
	background_image	=	SerializerMethodField()
	top_reviews			=	SerializerMethodField()

	
	class Meta:
		model = UserOtherInfo
		fields = [
			'name',
			'phone',
			'user_ID',
			'avg_rating',
			'location',
			'created',
			'type_of_tasker',
			'bio',
			'instant_booking',
			'completed_tasks',
			'current_language',
			'profile_img',
			'usertype',
			'city',
			'location',
			'instant_services',
			'other_services',
			'services_offered',
			'switched_to_provider',
			'user_address',
			'background_image',
			'locality',
			'user_address_lat',
			'user_address_long',
			'top_reviews',

			]
		
	def get_services_offered(self,instance):
		qs = Service.objects.filter(user=instance.user.id)
		data = ServiceSerializer(qs,many=True).data
		return data
	
	def get_instant_services(self,instance):
		instant_services = Service.objects.filter(user=instance.user.id).filter(instant_booking = True)
		data = ServiceSerializer(instant_services,many=True).data
		return data
	
	def get_other_services(self,instance):
		other_services = Service.objects.filter(user=instance.user.id).filter(instant_booking=False)
		data = ServiceSerializer(other_services,many=True).data
		return data
	
	def get_instant_booking(self,instance):
		if len(Service.objects.filter(user=instance.user.id).filter(instant_booking=True))==0:
			return False
		else:
			return True
	
	def get_name(self,instance):
		userObj = User.objects.get(id=instance.user.id)
		data = FirstNameSerializer(userObj).data
		return data
	
	def get_user_ID(self,instance):
		userObj = User.objects.get(id=instance.user.id)
		return userObj.id
	
	def get_profile_img(self,instance):
		data = UserProfileImageSerializer(instance).data
		if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
			return ""
		else:
			return data['profile_image_s3']
	
	def get_background_image(self,instance):
		userObj = User.objects.get(id=instance.user.id)
		ServiceQS = Service.objects.filter(user=userObj)
		if len(ServiceQS) == 0:
			return ""
		else:
			ServiceObject = ServiceQS[0]
			return ServiceObject.service_image_1_s3
	
	def get_top_reviews(self,instance):
		user_object = instance.user
		service_qs = Service.objects.filter(user=user_object)
		print("<---------------Service QS retreived------------------->",service_qs)
		if len(service_qs)==0:
			return []
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
	#		 for review in sorted_reviews:
	#			 review_id.append(review[0][0])
			print("<------------Review IDS---------------->",review_id)
			final_reviews = []
	
			
			
			
			for review_ref in review_id:
				review_object = ServiceFeedback.objects.get(id=review_ref)
				print("<----------------review object--------->",review_object)
				review_serialized = ServiceFeedbackSerializer(review_object).data
				print("<-----------------Review Serialized------------->",review_serialized)
				final_reviews.append(review_serialized)
				
			print("<============================>",final_reviews)
			return final_reviews




class FeaturedSerializer(ModelSerializer):
	services_offered	=	SerializerMethodField()
	instant_services	=	SerializerMethodField()
	other_services		=	SerializerMethodField()
	instant_booking		=	SerializerMethodField()
	name				=	SerializerMethodField()
	user_ID				=	SerializerMethodField()
	profile_img			=	SerializerMethodField()
	background_image	=	SerializerMethodField()
	top_reviews			=	SerializerMethodField()

	class Meta:
		model = UserOtherInfo
		fields = [
			'name',
			'phone',
			'user_ID',
			'avg_rating',
			'location',
			'created',
			'type_of_tasker',
			'bio',
			'instant_booking',
			'completed_tasks',
			'current_language',
			'profile_img',
			'usertype',
			'city',
			'location',
			'instant_services',
			'other_services',
			'services_offered',
			'switched_to_provider',
			'user_address',
			'background_image','locality',
			'user_address_lat',
			'user_address_long',
			'top_reviews',
			]
	def get_services_offered(self,instance):
		lang = self.context.get('lang')
		qs = Service.objects.filter(user=instance.user.id).filter(service_langugae=lang)
		data = ServiceSerializer(qs,many=True).data
		return data

	def get_instant_services(self,instance):
		instant_services = Service.objects.filter(user=instance.user.id).filter(instant_booking = True)
		data = ServiceSerializer(instant_services,many=True).data
		return data
	def get_other_services(self,instance):
		other_services = Service.objects.filter(user=instance.user.id).filter(instant_booking=False)
		data = ServiceSerializer(other_services,many=True).data
		return data
	def get_instant_booking(self,instance):
		if len(Service.objects.filter(user=instance.user.id).filter(instant_booking=True))==0:
			return False
		else:
			return True
	def get_name(self,instance):
		userObj = User.objects.get(id=instance.user.id)
		data = FirstNameSerializer(userObj).data
		return data
	def get_user_ID(self,instance):
		userObj = User.objects.get(id=instance.user.id)
		return userObj.id
	def get_profile_img(self,instance):
		data = UserProfileImageSerializer(instance).data
		if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
			return ""
		else:
			return data['profile_image_s3']
	def get_background_image(self,instance):
		userObj = User.objects.get(id=instance.user.id)
		ServiceQS = Service.objects.filter(user=userObj)
		if len(ServiceQS) == 0:
			return ""
		else:
			ServiceObject = ServiceQS[0]
			# print("<------------------Background Image---------------->",ServiceImageObject.service_image_1_s3)
			ServiceImageObject =  ServiceImage.objects.get(service=ServiceObject)
			return ServiceImageObject.service_img_file_1_s3
	def get_top_reviews(self,instance):
		user_object = instance.user
		service_qs = Service.objects.filter(user=user_object)
		print("<---------------Service QS retreived------------------->",service_qs)
		if len(service_qs)==0:
			return []
		else:
			reviews_list = []
			FinalQS = ServiceFeedback.objects.none()
			for service in service_qs:
				reviews = ServiceFeedback.objects.filter(service_id=service)
				#print("<---------------reviews--------------------->",type(reviews))
				if len(reviews)!=0:
					serializer = ServiceFeedbackSerializer(reviews,many=True).data
					#print("<==============Serializer--------------------?",serializer)
					for review_object in serializer:
						reviews_list.append(review_object)
			raw_reviews = []
			for review in reviews_list:
			    tuple_object = (review['feedback_id'],review['rating'],review['feedback_date'],review['feedback_time'])
			    raw_reviews.append(tuple_object)
			#print("<--------------Raw Reviews Tuple---------------->",raw_reviews)
			sorted_reviews = sorted(raw_reviews,key=itemgetter(1,2,3),reverse=True)[:3]
			#print("<--------------Sorted Tuple------------------->",sorted_reviews)
			review_id = [x[0] for x in sorted_reviews]
			final_reviews = []
			for review_ref in review_id:
				review_object = ServiceFeedback.objects.get(id=review_ref)
				review_serialized = ServiceFeedbackSerializer(review_object).data
				final_reviews.append(review_serialized)
			return final_reviews


class FilteredProviderSerializer(ModelSerializer):
	services_offered	=	SerializerMethodField()
	instant_services	=	SerializerMethodField()
	other_services		=	SerializerMethodField()
	instant_booking		=	SerializerMethodField()
	name				=	SerializerMethodField()
	user_ID				=	SerializerMethodField()
	profile_img			=	SerializerMethodField()
	background_image	=	SerializerMethodField()
	top_reviews			=	SerializerMethodField()
	
	class Meta:
		model = UserOtherInfo
		fields = [
			'name',
			'phone',
			'user_ID',
			'avg_rating',
			'location',
			'created',
			'type_of_tasker',
			'bio',
			'instant_booking',
			'completed_tasks',
			'current_language',
			'profile_img',
			'usertype',
			'city',
			'location',
			'instant_services',
			'other_services',
			'services_offered',
			'switched_to_provider',
			'user_address',
			'background_image',
			'locality',
			'user_address_lat',
			'user_address_long',
			'top_reviews',
			]
	def get_services_offered(self,instance):
		lang = self.context.get('lang')
		qs = Service.objects.filter(user=instance.user.id).filter(service_langugae=lang)
		data = ServiceSerializer(qs,many=True).data
		return data
	def get_instant_services(self,instance):
		instant_services = Service.objects.filter(user=instance.user.id).filter(instant_booking = True)
		data = ServiceSerializer(instant_services,many=True).data
		return data
	def get_other_services(self,instance):
		other_services = Service.objects.filter(user=instance.user.id).filter(instant_booking=False)
		data = ServiceSerializer(other_services,many=True).data
		return data
	def get_instant_booking(self,instance):
		if len(Service.objects.filter(user=instance.user.id).filter(instant_booking=True))==0:
			return False
		else:
			return True
	def get_name(self,instance):
		userObj = User.objects.get(id=instance.user.id)
		data = FirstNameSerializer(userObj).data
		return data
	def get_user_ID(self,instance):
		userObj = User.objects.get(id=instance.user.id)
		return userObj.id
	def get_profile_img(self,instance):
		data = UserProfileImageSerializer(instance).data
		if data['profile_image_s3'] == None or data['profile_image_s3'] == "":
			return ""
		else:
			return data['profile_image_s3']
	def get_background_image(self,instance):
		userObj = User.objects.get(id=instance.user.id)
		ServiceQS = Service.objects.filter(user=userObj)
		if len(ServiceQS) == 0:
			return ""
		else:
			ServiceObject = ServiceQS[0]
			return ServiceObject.service_image_1_s3
	def get_top_reviews(self,instance):
		user_object = instance.user
		service_qs = Service.objects.filter(user=user_object)
		print("<---------------Service QS retreived------------------->",service_qs)
		if len(service_qs)==0:
			return []
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
			print("<------------Review IDS---------------->",review_id)
			final_reviews = []
			for review_ref in review_id:
				review_object = ServiceFeedback.objects.get(id=review_ref)
				print("<----------------review object--------->",review_object)
				review_serialized = ServiceFeedbackSerializer(review_object).data
				print("<-----------------Review Serialized------------->",review_serialized)
				final_reviews.append(review_serialized)
			print("<============================>",final_reviews)
			return final_reviews
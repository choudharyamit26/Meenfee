from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime,timedelta
from django.utils import timezone
from datetime import datetime
from django.contrib.sites.models import Site
from asn1crypto._ffi import null
# from .models import File
# from django.contrib.gis.db import models as gis_models
# from mapwidgets.widgets import GooglePointFieldWidget

from django.db.models.signals import post_save
from django.dispatch import receiver


CITYNAME    = (('Amman', 'Amman'), ('Irbid', 'Irbid'),('Aqaba','Aqaba'),('Noida','Noida'))
LEVELSKILLS = (('Beginner-(0-3)','Beginner-(0-3)'),('Medium-(3-7)','Medium-(3-7)'),('Elite-(7+)','Elite-(7+)'))
LOCATION    = (('I travel to my customers','I travel to my customers'),('Customers travel to me','Customers travel to me'),('Remotely','Remotely'))
DISTANCE    = (('5 Km away','5 Km away'),('20 Km away','20 Km away'),('30 Km away','30 Km away'))
UNITS       = (('1 hour','1 hour'),('2 hour','2 hour'),('3 hour','3 hour'))
TYPEOFTASKER = (('Elite','Elite'),('Average','Average'))
LANGS = (('Arabic','Arabic'),('English','English'))

class City(models.Model):
    city    = models.CharField(default="ftgyhiujk",max_length=40,unique=True,null=False)
    city_in_arabic = models.CharField(default="ftgyhiujk",max_length=40,null=False)
   
    def __str__(self):
        return self.city
    class Meta:    
        verbose_name_plural = "Cities"

class Category(models.Model):    
    code = models.CharField(default='AR', max_length=100,null=True)
    code_in_arabic = models.CharField(default="الفئة",max_length=100,null= True)    
    category = models.CharField(max_length=40 ,unique=True,null=True)
    category_in_arabic = models.CharField(default="الفئة",max_length=40,null=True)
    description= models.CharField(default='Test',max_length=500,null= True)
    description_in_arabic= models.CharField(default="الفئة",max_length=500,null= True)
    bannerimage = models.ImageField(upload_to ='service/img',default = 'service/img/default.jpg')
    
    def __str__(self):
        return self.category
    class Meta:
        verbose_name_plural = "Catagories"

class SubCategory(models.Model):
    category    = models.ForeignKey(Category,on_delete=models.CASCADE)
    bannerimage = models.ImageField(upload_to ='service/img',default = 'service/img/default.jpg')
    
    subcategory = models.CharField(max_length=40,null=True,unique=True)
    subcategory_in_arabic = models.CharField(default="هذه لغة عربية بسيطة",max_length=40,null=True)
    description= models.CharField(default='Test',max_length=500,null= True)
    description_in_arabic= models.CharField(default="الفئة",max_length=500,null= True)
    
    def __str__(self):
        return str(self.subcategory) +' - '+str(self.id)
    class Meta:
        verbose_name_plural = "SubCatagories"




class ServiceList(models.Model):
    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE,blank=True,null=True)
    service_name_english = models.CharField(max_length=200,blank=True,null=True)
    service_name_arabic = models.CharField(max_length=200,blank=True,null=True)
    
    
    def __str__(self):
        return str(self.id) + " - " +str(self.service_name_english)
    
    class Meta:
        verbose_name_plural = "Service List"


PRICINGUNIT   = (('Per Project', 'Per Project'), ('Per Hour', 'Per Hour'))

# class Service(models.Model):
#     '''
#     model for service add by provider
#     '''
#     user                    = models.ForeignKey(User, on_delete=models.CASCADE)
#     service_name            = models.CharField(max_length=200,null=True,default="sample service")
#     # category                = models.ForeignKey(Category, to_field="category",db_column="category", on_delete=models.CASCADE)
#     # subcategory             = models.ForeignKey(SubCategory, to_field="subcategory",db_column="subcategory",on_delete=models.CASCADE)
#     category                = models.ForeignKey(Category, on_delete=models.CASCADE)
#     subcategory             = models.ForeignKey(SubCategory,on_delete=models.CASCADE)

#     experience              = models.TextField(blank=True,null=True)
#     levelskill              = models.CharField(max_length=120, choices=LEVELSKILLS)
#     service_place           = models.CharField(max_length=120, choices=LOCATION)
#  #   location                = gis_models.PointField(u'longitude/latitude',geography=True, blank=True, null=True,)
#     city                    = models.ForeignKey(City,blank=True,null=True,on_delete=models.DO_NOTHING,choices=CITYNAME)
#     # city                    = models.ForeignKey(City,to_field="city",db_column="city",blank=True,null=False,on_delete=models.DO_NOTHING)
#     distance_limit          = models.CharField(max_length=100, choices=DISTANCE)
#     service_pricing         = models.PositiveIntegerField(help_text='in Jordanian dinar')
#     pricing_timing_unit     = models.CharField(max_length=30,choices=PRICINGUNIT)
#     quote_at_request        = models.BooleanField(default=False, help_text='This will create popup when they accept a requester request')
#     provide_tools           = models.BooleanField(default=True)
#     tool_specify            = models.TextField(blank =True, null=True)
#     instant_booking         = models.BooleanField(default =True)
#     avg_rating              = models.FloatField(default=0.0)
#     created                 = models.DateTimeField(auto_now_add=True)
#     service_img             = models.ImageField(upload_to='provider_service/service_images',default='provider_service/service_images/default.jpg')
#     service_img_file        = models.FileField(blank=False,null=False,upload_to='provider_service/service_images',default='provider_service/service_images/default.jpg')
    
#     def __str__(self):
#         return self.service_name

#     class Meta:
#         verbose_name_plural = "Services"



class Service(models.Model):
    '''
    model for service add by provider
    '''
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    service_name            = models.CharField(max_length=200,null=True,default="sample service")
    service_name_in_arabic  = models.CharField(max_length=200,null=True,default="الفئة")
    
    
    # category                = models.ForeignKey(Category, to_field="category",db_column="category", on_delete=models.CASCADE)
    category                = models.ForeignKey(Category,on_delete=models.CASCADE)    
    # subcategory             = models.ForeignKey(SubCategory, to_field="subcategory",db_column="subcategory",on_delete=models.CASCADE)
    subcategory             = models.ForeignKey(SubCategory,on_delete=models.CASCADE,blank=True,null=True)
    experience              = models.TextField(blank=True,null=True)
    levelskill              = models.CharField(max_length=120,blank=True,null=True)
    service_place           = models.CharField(max_length=120, blank=True,null=True)
 #   location                = gis_models.PointField(u'longitude/latitude',geography=True, blank=True, null=True,)
    # city                    = models.ForeignKey(City,default="City Name",to_field="city",db_column="city",blank=True,null=False,on_delete=models.DO_NOTHING)
    # city                    = models.ForeignKey(City,blank=True,null=False,on_delete=models.DO_NOTHING,default="City")   
    city                    = models.CharField(max_length=150,blank=True,null=True) 
    distance_limit          = models.CharField(max_length=100,blank=True,null=True)
    service_pricing         = models.DecimalField(help_text='in Jordanian dinar',blank=True,null=True,default=0.0,decimal_places=2,max_digits=10)
    pricing_timing_unit     = models.CharField(max_length=50,blank=True,null=True,default="Per Hour")
    quote_at_request        = models.BooleanField(default=False, help_text='This will create popup when they accept a requester request')
    provide_tools           = models.BooleanField(default=True)
    tool_specify            = models.TextField(blank =True, null=True)
    instant_booking         = models.BooleanField(default =True)
    avg_rating              = models.DecimalField(default=0.0,max_digits=7,decimal_places=5)
    count_of_rating         = models.IntegerField(default=0)
    available_on_Sunday     = models.BooleanField(default=False)
    available_on_Monday     = models.BooleanField(default=False)
    available_on_Tuesday    = models.BooleanField(default=False)
    available_on_Wednesday   = models.BooleanField(default=False)
    available_on_Thursday     = models.BooleanField(default=False)
    available_on_Friday     = models.BooleanField(default=False)
    available_on_Saturday     = models.BooleanField(default=False)
    created                 = models.DateTimeField(default=timezone.now)
    service_provider_rating = models.DecimalField(max_digits=3,decimal_places=2,default=0.0)
    # profile_img             =   models.ForeignKey(Image)
    # service_img             = models.ImageField(upload_to='provider_service/service_images',default='provider_service/service_images/default.jpg')
    service_image_1_s3      = models.CharField(max_length=300,blank=True,null=True)
    service_image_2_s3      = models.CharField(max_length=300,blank=True,null=True)
    service_image_3_s3      = models.CharField(max_length=300,blank=True,null=True)
    speciality              = models.BooleanField(default=False)
    service_location        = models.CharField(max_length=250,blank=True,null=True,default="Service Location")
    service_location_lat    = models.DecimalField(max_digits=20,decimal_places=10,default=0.0,blank=True,null=True)
    service_location_long   = models.DecimalField(max_digits=20,decimal_places=10,default=0.0,blank=True,null=True)
    locality                = models.CharField(max_length=50,blank=True,null=True)
    
    price_type              = models.TextField(blank=True,null=True)
    description              = models.CharField(max_length=200,null=True,default="sample description")
    description_in_arabic  = models.CharField(max_length=200,null=True,default="الفئة")
    service_pricing_precise  = models.DecimalField(help_text='in Jordanian dinar',blank=True,null=True,default=0.0,decimal_places=2,max_digits=10)
    experience_description  =   models.TextField(blank=True,null=True,default="")    
    service_langugae        =   models.CharField(blank=True,null=True,default="en",max_length=300)
    
    def __str__(self):
        return str(str(self.id) + " - " + str(self.service_name))

    class Meta:
        verbose_name_plural = "Services"


TASK_STATUS      =   (('Upcoming','Upcoming'),('Completed','Completed'),('In Progress','In Progress'))
BOOKING_STATUS   =   (('Awaiting Acceptance','Awaiting Acceptance'),('Accepted','Accepted'),('Rejected','Rejected'))   


class ProvidersRating(models.Model):    
    service_id = models.IntegerField(default=0)
    rating1              = models.PositiveIntegerField( validators=[MaxValueValidator(5), MinValueValidator(1)])
    created1             = models.DateTimeField(default=datetime.now())
    content1             = models.TextField(null=True)
    rating_by = models.IntegerField(default=1)   
    compliment_review              = models.IntegerField( default=5)
    user_id=models.IntegerField(default=1)
    modified_date             = models.DateTimeField(default=datetime.now())    
    test_fd= models.IntegerField(default=1)
    provider_id=models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.service_id) +' - '+str(self.user_id)+' - '+str(self.rating1)
    class Meta:
        verbose_name_plural = "MeenFee Providers Rating"
    



# class Bookings(models.Model):
#     provider        =   models.ForeignKey(User,on_delete=models.CASCADE,related_name="provider")
#     requester       =   models.ForeignKey(User,on_delete=models.CASCADE,related_name="requester")
#     requester_city  =   models.ForeignKey(City,on_delete=models.CASCADE,related_name="city")
#     category        =   models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category")
#     sub_category    =   models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name="sub_category")
#     service         =   models.ForeignKey(Service,on_delete=models.CASCADE,related_name="service")
#     task_status     =   models.CharField(max_length=30,blank=True,choices=TASK_STATUS)
#     booking_status  =   models.CharField(max_length=30,blank=True,choices=BOOKING_STATUS)


# class Bookings(models.Model):
#     provider        =   models.ForeignKey(User,on_delete=models.CASCADE,default="Provider",related_name="service_provider")
#     requester       =   models.ForeignKey(User,on_delete=models.CASCADE,default=0,related_name="service_requester")
#     requester_city  =   models.ForeignKey(City,on_delete=models.CASCADE)
#     category        =   models.ForeignKey(Category,on_delete=models.CASCADE)
#     sub_category    =   models.ForeignKey(SubCategory,on_delete=models.CASCADE)
#     service         =   models.ForeignKey(Service,on_delete=models.CASCADE)
#     task_status     =   models.CharField(max_length=30,blank=True,choices=TASK_STATUS)
#     booking_status  =   models.CharField(max_length=30,blank=True,choices=BOOKING_STATUS)
#     created         =   models.DateTimeField(auto_now_add=True)
#     modified        =   models.DateTimeField(auto_now=True)



# class Bookings(models.Model):
#     # provider        =   models.CharField(max_length=100,blank=True,default="Provider")
#     # requester       =   models.CharField(max_length=100,blank=True,default="Requester")
#     requester_city  =   models.CharField(City,max_length=100)
#     # category        =   models.CharField(Category,max_length=100)
#     # sub_category    =   models.CharField(SubCategory,max_length=100)
#     service         =   models.ForeignKey(Service,max_length=100,on_delete=models.CASCADE)
#     task_status     =   models.CharField(max_length=30,blank=True,choices=TASK_STATUS)
#     booking_status  =   models.CharField(max_length=30,blank=True,choices=BOOKING_STATUS)
#     created         =   models.DateTimeField(auto_now_add=True)
#     modified        =   models.DateTimeField(auto_now=True)






class ServiceImage(models.Model):
    service_img_file = models.FileField(blank=False, null=False,upload_to='service_images_new/service_images',default='service_images_new/service_images/default.jpg')
    
    service_img_file1 = models.FileField(blank=False, null=False,upload_to='service_images_new/service_images',default='service_images_new/service_images/default.jpg')
    service_img_file2 = models.FileField(blank=False, null=False,upload_to='service_images_new/service_images',default='service_images_new/service_images/default.jpg')
    
    is_arabic = models.BooleanField(default=False)
    service= models.ForeignKey(Service,on_delete=models.CASCADE,default=0)
    
    service_img_file_1_s3 = models.CharField(blank=True,null=True,max_length=250,default="S3 Bucket URL of service image 1")
    service_img_file_2_s3 = models.CharField(blank=True,null=True,max_length=250,default="S3 Bucket URL of service image 2")
    service_img_file_3_s3 = models.CharField(blank=True,null=True,max_length=250,default="S3 Bucket URL of service image 3")  
    
    def __str__(self):
        return str(self.service_img_file)




class Something(models.Model):
    name = models.CharField(max_length=100,blank=True,default="Provider")
    last_name = models.CharField(max_length=100,blank=True,default="last name")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Something Table"

        

class days(models.Model):
    Service = models.OneToOneField(Service,on_delete=models.CASCADE)
    Sunday = models.BooleanField(default=False)
    Monday = models.BooleanField(default=False)
    Tuesday = models.BooleanField(default=False)
    Wednesday = models.BooleanField(default=False)
    Thursday = models.BooleanField(default=False)
    Friday = models.BooleanField(default=False)
    Saturday = models.BooleanField(default=False)

    def __str__(self):
        return str(self.Service.user.first_name) + " " + str(self.Service.user.last_name)


    class Meta:
        verbose_name_plural = "Days"


DAYS = (
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    )
class Slots(models.Model):

    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    note =  models.CharField(max_length=50,default="My time slots for each day")
    day = models.TextField(choices=DAYS,default='Sunday')
    start_time = models.TimeField(default=datetime.now().strftime('%H:%M:%S'))
    end_time = models.TimeField(default=datetime.now().strftime('%H:%M:%S'))


    def __str__(self):
        return str(self.service) + "-" + str(self.day)



    class Meta:
        verbose_name_plural = "Slots"
    # def save(self, *args, **kwargs):
    #         queryset = Slots.objects.filter(service = self.service,day=self.day)
    #         l = len(queryset)
    #         matched = 0
    #         if len(queryset) > 0:
    #             for i in queryset:        
    #                 if (self.start_time >= i.start_time and self.start_time <= i.end_time) and (self.end_time >= i.start_time and self.end_time <= i.end_time):
    #                     matched +=1
    #             if int(matched)== 0:
    #                 return super(Slots, self).save(*args, **kwargs)
    #         else:
    #             return super(Slots, self).save(*args, **kwargs)


class FeaturedProviders(models.Model):
    '''
    Service provider can select different-different availability
    time for different date. This model will also be used in Calender feature
    '''
    service   = models.ForeignKey(Service, on_delete=models.CASCADE)
   
    def __str__(self):
        return str(self.service.user.first_name)

    class Meta:
        verbose_name_plural = "Featured Provider OLD"


class DayAndSlots(models.Model):
    service             =   models.ForeignKey(Service,on_delete=models.CASCADE)
    day                 =   models.CharField(unique=True,max_length=10,default="Day",choices=DAYS)
    slot_1_start_time   =   models.TimeField(default=datetime.now().strftime('%H:%M:%S'))
    slot_1_end_time     =   models.TimeField(default=datetime.now().strftime('%H:%M:%S'))    
    
    slot_2_start_time   =   models.TimeField(default=datetime.now().strftime('%H:%M:%S'))
    slot_2_end_time     =   models.TimeField(default=datetime.now().strftime('%H:%M:%S'))
    
    slot_3_start_time   =   models.TimeField(default=datetime.now().strftime('%H:%M:%S'))
    slot_3_end_time     =   models.TimeField(default=datetime.now().strftime('%H:%M:%S'))
    
    def __str__(self):
        return self.day

    class Meta:
        verbose_name_plural="Availibility Days and Time Slots"



class FeaturedServiceProviders(models.Model):
    provider         = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + "-" + str(self.provider)

    class Meta:
        verbose_name_plural = "Featured Service Provider"



class TrendingProviders(models.Model):
    '''
    Service provider can select different-different availability
    time for different date. This model will also be used in Calender feature
    '''
    service   = models.ForeignKey(Service, on_delete=models.CASCADE)
   
    def __int__(self):
        return self.service

    class Meta:
        verbose_name_plural = "Trending Providers"

class MostRecentProviders(models.Model):
    '''
    Service provider can select different-different availability
    time for different date. This model will also be used in Calender feature
    '''
    service   = models.ForeignKey(Service, on_delete=models.CASCADE)
    def __int__(self):
        return self.service

    class Meta:
        verbose_name_plural = "Most Recent Providers"

class ServiceRating(models.Model):
    '''
    Requester can give Rating  to service provider after service completion
    After rating by requester, provider avg_rating in service model should be
    change and it would be avg of all rating provided by all requester

    '''

    service             = models.ForeignKey(Service, on_delete=models.CASCADE)
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    rating              = models.PositiveIntegerField( validators=[MaxValueValidator(5), MinValueValidator(1)])
    created             = models.DateTimeField(auto_now_add=True)
    content             = models.TextField(null=True)
    uyt=  models.TextField(null=True)
    
    
    def __str__(self):
        return str(self.service) +' - '+str(self.user)+' - '+str(self.rating)
    class Meta:
        verbose_name_plural = "MeenFee Service Rating"
        
        
        

# class ServiceFeedback(models.Model):
#     '''
#     Requester can give Feedback  to service provider after service completion
#     here --user-- is feedback given user
# 
#     '''
#     	
#     service             = models.ForeignKey(Service, on_delete=models.CASCADE)
#     user                = models.ForeignKey(User, on_delete=models.CASCADE)
#     content             = models.TextField(null=True)
#     timestamp           = models.DateTimeField(auto_now_add=True)
# 
#     def __str__(self):
#         return str(self.service) +' - '+str(self.user)

class MeenFeeFeedback(models.Model):
    '''
    Requester and Providers both Can give Feedback to MeenFee administration
    '''
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    content             = models.TextField(null=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    content1             = models.TextField(null=True)
    
    def __str__(self):
        return str(self.content)
    class Meta:
        verbose_name_plural = "MeenFee Feedback"

class HelpAndSupport(models.Model):
    '''
    Meenfee admin can add these field from admin panel it will shown on the help and support section of MeenFee App
    '''
#     site = models.OneToOneField(Site,on_delete=models.CASCADE)
    contactaddress = models.CharField(max_length=400,null=True)
    contactaddress_in_arabic = models.CharField(max_length=400,default="هذه لغة عربية بسيطة",null=True)
    contactnumber = models.CharField(max_length = 15)
    email = models.EmailField(max_length=70,blank=True)
    website = models.CharField(max_length=70,blank=True)
    def __str__(self):
        return str(self.contactaddress) +' - '+str(self.contactnumber) + ' - ' +str(self.email)
    class Meta:
        verbose_name_plural = "Help And Support"



BOOKINGLOCATION  = (('Come to my place','Requester place'),('Service provider place','Provider place'),('Remotely','Remotely'))


class RawBooking(models.Model):
    '''
    To save row booking request given by requester

    '''
    provider                    = models.ForeignKey(User,on_delete=models.CASCADE,related_name="provider",blank=True,null=True)
    requester                   = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    # appointment_city            = models.ForeignKey(City,blank=True,on_delete=models.CASCADE,null=True)
    appointment_city            = models.CharField(max_length=100,choices=CITYNAME,blank=True,null=True)
    service                     = models.ForeignKey(Service,default ='2',on_delete=models.CASCADE,blank=True,null=True)
    start_time                  = models.TimeField(auto_now=True)
    end_time                    = models.TimeField(auto_now=True)
    date                        = models.DateField(auto_now=True)
    appointment_venue           = models.CharField(max_length=120, blank=True,null=True,choices=BOOKINGLOCATION)
    appointment_gio_location    = models.CharField(max_length=30,blank=True,null=True)
    description                 = models.TextField(blank=True,null=True)
    isaccepted_by_provider      = models.BooleanField(default=False)
    created                     = models.DateTimeField(blank=True,null=True)
    time_taken_accepting        = models.PositiveIntegerField(blank=True,null=True,help_text='in minutes')
    accepted_time               = models.DateTimeField(editable = False,blank=True,null=True)
    ispaymentadd                = models.BooleanField(default=False)
    paymentaddtime              = models.DateTimeField(blank=True,null=True)
    isbookingcompleted          = models.BooleanField(default=False)
    service_name                = models.CharField(max_length=200,blank=True,null=True)
    provider_name               = models.CharField(max_length=200,blank=True,null=True)


    

    def __str__(self):
        return str(self.id)
        
    def save(self, *args, **kwargs):
            self.created = datetime.now()    
            return super(RawBooking, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = "Raw Bookings"






# <--------------------------------------------------TEMP------------------VVVVVVVVVVVVV---------------------------->


# class RawBookingTemp(models.Model):
#     '''
#     To save row booking request given by requester

#     '''
#     provider                    = models.ForeignKey(User,on_delete=models.CASCADE,related_name="provider",blank=True,null=True)
#     requester                   = models.ForeignKey(User , on_delete=models.CASCADE,related_name="requester",blank=True,null=True)
#     appointment_city            = models.ForeignKey(City,blank=True,on_delete=models.DO_NOTHING,null=True)
#     service                     = models.ForeignKey(Service,default ='2',on_delete=models.CASCADE,blank=True,null=True)
#     appointment_venue           = models.CharField(max_length=120, blank=True,null=True,choices=BOOKINGLOCATION)
#     description                 = models.TextField(blank=True,null=True)
#     isaccepted_by_provider      = models.BooleanField(default=False)
#     time_taken_accepting        = models.PositiveIntegerField(blank=True,null=True,help_text='in minutes')
#     ispaymentadd                = models.BooleanField(default=False)
#     isbookingcompleted          = models.BooleanField(default=False)

#     def __str__(self):
#         return str(self.id)
        
#     def save(self, *args, **kwargs):
#             self.created = datetime.now()
#             return super(RawBooking, self).save(*args, **kwargs)
#     class Meta:
#         verbose_name = 'Booking'
#         verbose_name_plural = "Raw Bookings"


# <----------------------------------------------TEMP---------------------------^^^^^^^^^^^^^^^^^----------------------------->



# class Bookings(models.Model):

#     requestor           =   models.ForeignKey(User,on_delete=models.CASCADE)
#     provider            =   models.ForeignKey(User,on_delete=models.CASCADE)
#     requestor_city      =   models.CharField(max_length=200,choices=CITYNAME)
#     point_of_service    =   models.ForeignKey(LOCATIO)



class OngoingBooking(models.Model):
    '''
    when requester add payment method then booking  will come in this section
    '''
    rawbooking_id               = models.OneToOneField(RawBooking ,on_delete=models.DO_NOTHING)
    requester                   = models.ForeignKey(User ,related_name='requestor', on_delete=models.DO_NOTHING)
    provider                    = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    confirmed_by_provider       = models.BooleanField(default=False)
    confirmed_by_requester      = models.BooleanField(default=False)
    '''
    status code 

    1   = card added (live)
    2   = ReScheduled Appointments (in process)
    3   = on cancelling appointment delete model from here
    4   = completed

    '''
    booking_status     = models.CharField(max_length=2, blank=True,null=True)

class ReScheduledAppointment(models.Model):
    
    rawbooking_id           = models.ForeignKey(RawBooking ,on_delete=models.DO_NOTHING)
    re_scheduled_by         = models.ForeignKey(User,on_delete=models.CASCADE)
    re_scheduled_date       = models.DateField()
    re_sheduled_start_time  = models.TimeField()
    re_scheduled_end_time   = models.TimeField()
    isconfirmed_by_opp      = models.BooleanField(default=False)# is confirmed by otherside
    confirmed_by_opp_date   = models.DateTimeField(blank=True,null=True)

    # which things is re-schedule 

    def __int__(self):
        return self.rowbooking_id

    class Meta:
        verbose_name_plural = "Re-Scheduled Appointments"


class Notification(models.Model):
    notification_from       = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='notification_from')
    notification_to         = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='notification_to')
    isseen_by_opposite      = models.BooleanField(default=False)
    created                 = models.DateTimeField(auto_now_add=True)
    delieverd               = models.DateTimeField(blank=True,null=True)
    isseen_opposite         = models.BooleanField(default=False)
    seen_time               = models.DateTimeField(blank=True,null=True)

    # notification text and redirect from notification to action place is remaining

    def __int__(self):
        return self.notification_from

    class Meta:
        verbose_name_plural = "Notification"


class CanceledBooking(models.Model):
    '''
    cancelled booking will come here
    '''
    provider           = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='Provider')
    rawbooking_id      = models.OneToOneField(RawBooking ,on_delete=models.DO_NOTHING)
    canceled_by        = models.ForeignKey(User ,on_delete=models.DO_NOTHING)
    cancel_date        = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.rowbooking_id

    class Meta:
        verbose_name_plural = "Canceled Booking"


class CompletedBooking(models.Model):
    '''
    Completed Booking will come here
    '''
    provider                  = models.ForeignKey(User,on_delete=models.CASCADE,default="2")
    rawbooking_id             = models.OneToOneField(RawBooking ,on_delete=models.DO_NOTHING)
    timestamp                 = models.DateTimeField(auto_now_add=True)
    
    
    # TO DO model for when provider say service completed and requester say not completed

    def __int__(self):
        return self.rowbooking_id

    class Meta:
        verbose_name_plural = "Completed Booking"


class PaymentMethod(models.Model):
    '''
    payment method add by requester for perticular rowbooking

    '''
    user            = models.ForeignKey(User ,on_delete=models.DO_NOTHING)
    token           = models.CharField(max_length=500)
    bookingid       = models.ForeignKey(RawBooking,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = "Payment Methods"

# USERTYPE = (('provider','Provider'),('requester','Requester'))


class UserOtherInfo(models.Model):

    '''
    To extend basic user model (for users extra informations)
    '''
    user                    =   models.OneToOneField(User,on_delete=models.CASCADE)
    phone                   =   models.CharField('Phone Number', max_length=15,null=True,blank=True)
    idcard                  =   models.CharField('ID Card Number', max_length=50,null=True,blank=True)
    isphvarified            =   models.BooleanField('Is Phone Varified ?',default=False)
    isemvarified            =   models.BooleanField('Is Email Verified ?',default=False)
    # isIDVerfified           =   models.BooleanField('Is ID Verified ?',default=False)
    # isProviderVerified      =   models.BooleanField('Is Profile Verified ?',default=False)
#     usertype                =   models.CharField(max_length=20,blank=True,null=True, choices = USERTYPE)
    usertype                =   models.CharField(max_length=20,blank=True,null=True)
    avg_rating              =   models.DecimalField(default=0,max_digits=6,decimal_places=5)
    count_of_rating         =   models.IntegerField(default=0)
    response_within         =   models.PositiveIntegerField(blank=True,null=True,help_text='in minutes',default=0)
    response_within_count   =   models.IntegerField(default=0,blank=True,null=True)
    location                =   models.CharField(max_length=20,blank=True,null=True,choices=CITYNAME)
    created                 =   models.DateTimeField(blank=True,null= True,default=timezone.now())
    type_of_tasker          =   models.CharField(max_length=20,blank=True,null=True, choices = TYPEOFTASKER)
    bio                     =   models.CharField(max_length=250,blank=True,null=True)
    completed_tasks         =   models.PositiveIntegerField(default=0)
    fcm_token               =   models.CharField('fcm token', max_length=500,null=True,blank=True)
    profile_views           =   models.PositiveIntegerField(default=0)
    profile_img             =   models.ImageField(upload_to ='service/img',default = 'service/img/default.jpg')
    current_language        =   models.CharField('Current Language',max_length=20,choices=LANGS)
    # city                  =   models.ForeignKey(City,blank=True,null=True,on_delete=models.DO_NOTHING,default="City")
    city                    =   models.CharField(max_length=150,blank=True,null=True) 
    switched_to_provider    =   models.BooleanField(default=False)
    user_address            =   models.CharField(default="Address",max_length=250)
    user_address_lat        =   models.DecimalField(max_digits=20,decimal_places=10,default=0.0)
    user_address_long       =   models.DecimalField(max_digits=20,decimal_places=10,default=0.0)
    
    fb_id                   =   models.CharField('Unique Facebook ID',max_length=100,blank=True,null=True)
    google_id               =   models.CharField('Unique Google ID',max_length=100,blank=True,null=True)
    is_phone_verified       =   models.BooleanField('Is Phone Verified',default=False)
    is_email_verified       =   models.BooleanField('Is Email Verified',default=False)
    is_id_verified          =   models.BooleanField('Is ID Verified',default=False)    
    is_account_fully_verified     =   models.BooleanField('Is account fully verified',default=False)
    profile_image_s3        =   models.CharField(max_length=300,blank=True,null=True)
    locality                =   models.CharField(max_length=50,blank=True, null =True, default="User Locality")
    total_services_count    =   models.IntegerField(default=0)
    avg_rating_rounded      =   models.DecimalField(default=0,max_digits=3,decimal_places=1)





    def __str__(self):
        return str(str(self.id) + " - " + str(self.user.first_name))
        
#     def save(self, *args, **kwargs):
#         self.created = datetime.now()    
#         return super(UserOtherInfo, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.created = datetime.now()    
            return super(UserOtherInfo, self).save(*args, **kwargs)
        else:
            return super(UserOtherInfo, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = "User Other Info"
        verbose_name_plural = "User Other Info"




class UserOtherInfoTemp(models.Model):

    '''
    To extend basic user model (for users extra informations)
    '''
    user             = models.OneToOneField(User,on_delete=models.CASCADE)
    phone            = models.CharField('Phone Number', max_length=15,null=True,blank=True)
    idcard           = models.CharField('ID Card Number', max_length=50,null=True,blank=True)
    isphvarified     = models.BooleanField('Is Phone Varified',default=False)
    isemvarified     = models.BooleanField('Is Email Verified',default=False)
    usertype         = models.CharField(max_length=20,blank=True,null=True)
    avg_rating       = models.FloatField(default=0.0)
    response_within  = models.PositiveIntegerField(blank=True,null=True,help_text='in minutes')
    location         = models.CharField(max_length=20,blank=True,null=True,choices=CITYNAME)
    created          = models.DateTimeField(blank=True,null= True)
    type_of_tasker   = models.CharField(max_length=20,blank=True,null=True, choices = TYPEOFTASKER)
    bio              = models.CharField(max_length=250,blank=True,null=True)
    completed_tasks  = models.PositiveIntegerField(default=0)
    fcm_token        = models.CharField('fcm token', max_length=500,null=True,blank=True)
    profile_views    = models.PositiveIntegerField(default=0)
    profile_img      = models.ImageField(upload_to ='service/img',default = 'service/img/default.jpg')
    current_language = models.CharField('Current Language',max_length=20,choices=LANGS)
    def __str__(self):
        return self.user.first_name
        
    # def save(self, *args, **kwargs):
    #     self.created = datetime.now()    
    #     return super(UserOtherInfo, self).save(*args, **kwargs)
    class Meta:
        verbose_name = "User Other Info"
        verbose_name_plural = "User Other Info"





class QuestionFilledByAdmin(models.Model):
    Question_name             = models.CharField(max_length=50,default ="Level",null=True)
    Question_name_in_arabic   = models.CharField(max_length = 50,default = "هذه لغة عربية",null=True)
    SubCategory               =   models.ForeignKey(SubCategory,on_delete = models.CASCADE,blank=True,null=True)
    question_for_provider     =   models.CharField(max_length = 100,null=True)
    question_for_provider_in_arabic = models.CharField(max_length = 100,default="هذه لغة عربية بسيطة",null=True)
    question_for_requestor    =   models.CharField(max_length = 100,null=True)
    question_for_requestor_in_arabic = models.CharField(max_length = 100,default= "هذه لغة عربية بسيطة",null=True)    
#     status            = models.BooleanField(default=True)
#     service_ids       = models.CharField(max_length=250,default ="0",null=True)
#     service_id_temp       = models.CharField(max_length=250,default ="0",null=True)
    status1            = models.BooleanField(default=True)
    related_service_ids       = models.CharField(max_length=250,null=True)
    category                    = models.ForeignKey(Category,on_delete = models.CASCADE,blank=True,null=True)
    service                     = models.ForeignKey(ServiceList,on_delete = models.CASCADE,blank=True,null=True)
    question_tag            =   models.CharField(max_length=100,blank=True,null=True,default="QUESTION_TAG")


# <-----------------------Added BY JOEL----------------------------------->
    def __str__(self):
        return str(self.id) + " - " + str(self.Question_name) + " - " + str(self.service)
# <-----------------------Added BY JOEL----------------------------------->


    class Meta:
        verbose_name_plural = "Question Filled By Admin"

class OptionsFilledbyAdmin(models.Model):
    question  = models.ForeignKey(QuestionFilledByAdmin,on_delete=models.CASCADE)

    Option1   = models.CharField(max_length = 50,null=True,default="Default")
    Option1_in_arabic = models.CharField(max_length=50,blank=True,default="هذه لغة عربية بسيطة")

    Option2   = models.CharField(max_length = 50,null=True,default="Default")
    Option2_in_arabic = models.CharField(max_length=50,blank=True,default="هذه لغة عربية بسيطة")

    Option3   = models.CharField(max_length = 50,blank=True,default="Default")
    Option3_in_arabic = models.CharField(max_length=50,blank=True,default="هذه لغة عربية بسيطة")


    # Option4   = models.CharField(max_length = 50,null=True,blank=True)
    # Option4_in_arabic = models.CharField(max_length=50,blank=True,default="هذه لغة عربية بسيطة",null=True)


# <-----------------------Added BY JOEL----------vvvvvvvvvvvvvvvvvvv---------------------->
    def __str__(self):
        return str(self.question)


# <-----------------------Added BY JOEL-----------^^^^^^^^^^^^^^^^^^^^^^^------------------------>

    class Meta:
        verbose_name_plural = "Options Filled by Admin"

class AnswerByProvider(models.Model):

    service         = models.ForeignKey(Service,on_delete=models.CASCADE)
    user             = models.ForeignKey(User,on_delete=models.CASCADE)
    question         = models.ForeignKey(QuestionFilledByAdmin,on_delete = models.CASCADE)
    option_Selected  = models.CharField(max_length = 100,null=True,blank=True)
    # option_Selected  = models.ForeignKey(OptionsFilledbyAdmin,null=True,on_delete = models.CASCADE)
    option_Selected_in_arabic = models.CharField(max_length=100,default="هذه لغة عربية بسيطة",null=True,blank=True)
    # userobj     = User.objects.get(user=user)
    user_name        = models.CharField(max_length=40,blank=True)
    service_name     = models.CharField(max_length=70,blank=True)
    question_string  = models.CharField(max_length=100,blank=True)
    option_selected_id = models.ForeignKey(OptionsFilledbyAdmin,on_delete=models.CASCADE,blank=True,null=True)
    question_string_arabic = models.CharField(max_length=100,blank=True,null=True)

    class Meta:
        verbose_name_plural = "Answer by Provider"





# class AnswerByProviderNew(models.Model):
#     category        =   models.ForeignKey(Category,on_delete=models.CASCADE)
#     subcategory     =   models.ForeignKey(SubCategory,on_delete=models.CASCADE)
#     tools           =   models.CharField(max_length=50,null=False)



class Rating(models.Model):
    services = models.ForeignKey(Service,on_delete=models.CASCADE)
    user     = models.ForeignKey(User,on_delete=models.CASCADE)
    rating   = models.FloatField(validators=[MinValueValidator(0.1), MaxValueValidator(5)],)

class Otp(models.Model):
    email = models.EmailField()
    otp = models.PositiveIntegerField()

class Token(models.Model):
    token =  models.CharField(max_length = 92,null=True)
    email =  models.EmailField()



# <-----------------------Added BY JOEL----------------------------------->

# class CreateProviderProfile(models.Model):
#     pass
    




class NewService(models.Model):
    user    = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    service_name = models.CharField(max_length = 200,default = "Service Name",blank=False,null=False)
    category   = models.ForeignKey(Category,on_delete=models.CASCADE,default = 1)   
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,default=1)
    skilllevel  = models.CharField(max_length=200,choices = LEVELSKILLS)
    location   = models.CharField(max_length=200,default="Location of Service")


    def __str__(self):
        return self.service_name

    class Meta:
        verbose_name_plural = "New Services"

POINT_OF_SERVICE = (('RequestorPlace','I travel to my customers'),('ProviderPlace','Customers travel to me'),('Remote','Remotely'))



# class NewBookingOLD(models.Model):
#     booking_id          = models.CharField(max_length=200,blank=False,null=False,default="MNF00000000000000")
#     created             = models.DateTimeField(auto_now=True)
#     requestor           = models.CharField(max_length=200,blank=False,null=False,default="Requestor")
#     provider            = models.CharField(max_length=200,blank=False,null=False,default="Provider")
#     provider_id         = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
#     service_id          = models.ForeignKey(Service,on_delete=models.CASCADE,default=1)
#     service_name        = models.CharField(max_length=200,blank=False,null=False,default="Service Name")
#     appointment_city    = models.CharField(max_length=200,blank=False,null=False,default="Appointment City")
#     point_of_service    = models.CharField(max_length=100,blank=False,null=False,default="Remote",choices = POINT_OF_SERVICE)
#     accepted            = models.BooleanField(default=False)
#     service_date        = models.DateField(auto_now_add=True)
#     service_time        = models.TimeField(auto_now_add=True)
#     # service_slot      = models.CharField(max_length=200,blank=False,null=False,default="Service Slot")
#     # booking_status    = models.CharField(max_length=200,default="Pending for Acceptance",null=False,blank=False)





DAYS_OF_THE_WEEK      =  [ ('Monday','Monday'),
                           ('Tuesday','Tuesday'),
                           ('Wednesday','Wednesday'),
                           ('Thursday','Thursday'),
                           ('Friday','Friday'),
                           ('Saturday','Saturday'),
                           ('Sunday','Sunday') ]


class ServiceSchedule(models.Model):
    service         =   models.ForeignKey(Service,on_delete=models.CASCADE)
    day             =   models.CharField(default="Day of the Week",choices=DAYS_OF_THE_WEEK,max_length=250)
    checked         =   models.BooleanField(default=False)
    open_time       =   models.TimeField(default=timezone.now(),blank=True)
    close_time      =   models.TimeField(default=timezone.now(),blank=True)
    service_capacity = models.PositiveIntegerField(default=1,blank=True,null=True)

    def __str__(self):
        return str(self.service.service_name) + "-" + str(self.day) + "-" + str(self.id)

    class Meta:
        verbose_name_plural = "Service Schedules"






class NewBookings(models.Model):
    booking_id          = models.CharField(max_length=200,blank=False,null=False,default="MNF00000000000000")
    created             = models.DateTimeField(auto_now_add=True)
    requestor           = models.CharField(max_length=200,blank=False,null=False,default="Requestor")
    requestor_id        = models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,default=1,related_name="booking_requestor")
    provider            = models.CharField(max_length=200,blank=False,null=False,default="Provider")
    provider_id         = models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,default=1)
    service_ID          = models.ForeignKey(Service,on_delete=models.CASCADE,default=1)
    service_name        = models.CharField(max_length=200,blank=False,null=False,default="Service Name")
    appointment_city    = models.CharField(max_length=200,blank=False,null=False,default="Appointment City")
    point_of_service    = models.CharField(max_length=100,blank=False,null=False,default="Remote")
    accepted            = models.BooleanField(default=False)
    service_date        = models.DateField(default=timezone.now())
    service_time        = models.TimeField(default=timezone.now())
    # service_slot      = models.CharField(max_length=200,blank=False,null=False,default="Service Slot")
    # booking_status    = models.CharField(max_length=200,default="Pending for Acceptance",null=False,blank=False)
    task_status         = models.CharField(max_length=100,blank=False,null=False,default="Upcoming",choices=TASK_STATUS)
    accepted_by_requester = models.BooleanField(default=False)
    accepted_by_provider        = models.BooleanField(default=False)
    rescheduled_service_date    = models.DateField(default=timezone.now())
    rescheduled_service_time    = models.TimeField(default=timezone.now())
    reschedule_request_date     = models.DateField(default=timezone.now)
    reschedule_request_time     = models.TimeField(default=timezone.now)
    booking_cancelled           = models.BooleanField(default=False)
#     providers_review_id         =models.IntegerField(default=0)
    providers_review_id         =models.IntegerField(default=0,blank=True,null=True)
    booking_completed           = models.BooleanField(default=False)
    booking_marked_completed_by_requestor = models.BooleanField(default=False)
    booking_marked_completed_by_provider  = models.BooleanField(default=False)
    cancellation_fee            = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    cancelled_by_provider       = models.BooleanField(default=False)
    cancelled_by_requestor      = models.BooleanField(default=False)
    cancellation_date           = models.DateField(default=timezone.now())
    cancellation_time           = models.TimeField(default=timezone.now())
    cancellation_fee_applicable = models.BooleanField(default=False)
    quote_requested_by_requestor =   models.BooleanField(default=False)
    quote_requested_by_provider  = models.BooleanField(default=False)
    admin_charges                =  models.DecimalField(default=0,decimal_places=2,max_digits=12)
    service_charges              =  models.DecimalField(default=0,decimal_places=2,max_digits=12)
    service_charge_rate        = models.CharField(default="",blank=True,null=True,max_length=150)
    service_end_time            =   models.TimeField(default=timezone.now)
    service_slot_id                =   models.ForeignKey(ServiceSchedule,on_delete=models.CASCADE,null=True,blank=True)
    payment_incurred            =   models.BooleanField(default=False)
    payment_completed           =   models.BooleanField(default=False)
    updated_time                = models.DateTimeField(auto_now=True,editable=True)
    booking_closure_time     =   models.DateTimeField(default=timezone.now)
    auto_cancellation_time   =   models.DateTimeField(default=timezone.now)
    auto_cancelled          =  models.BooleanField(default=False)
    payment_mode            =   models.CharField(default="",blank=True,max_length=5,null=True)

    def __str__(self):
        return str("Booking " + str(self.id) + " - " + str(self.booking_id))

    class Meta:
        verbose_name_plural = "New Bookings"
    
    # def save(self, *args, **kwargs):
    #     self.updated_time = timezone.now()
    #     return super(NewBookings, self).save(*args, **kwargs)







class ImageUploadTest(models.Model):
    title = models.CharField(max_length = 100,blank=True)
    description = models.CharField(max_length=200,blank=True)
    image = models.ImageField(upload_to='testimages/',default='testimages/default.jpg')





# <-----------------------Added BY JOEL----------------------------------->



class MarketingCarousel(models.Model):
    campaign_name = models.CharField(default="Marketing Campaign",blank=False,max_length=250)
    image = models.ImageField(upload_to = 'marketing/img',default = 'marketing/img/default.jpg',max_length=250)

    def __str__(self):
        return self.campaign_name
    class Meta:
        verbose_name_plural = "Marketing Campaing Images"



class Monday(models.Model):
    service         = models.ForeignKey(Service,on_delete=models.CASCADE,default=1)

    slot1_start     = models.TimeField(default=timezone.now(),blank=True)
    slot1_end       = models.TimeField(default=timezone.now(),blank=True)

    slot2_start     = models.TimeField(default=timezone.now(),blank=True)
    slot2_end       = models.TimeField(default=timezone.now(),blank=True)
    
    slot3_start     = models.TimeField(default=timezone.now(),blank=True)
    slot3_end       = models.TimeField(default=timezone.now(),blank=True)


class Tuesday(models.Model):
    service         = models.ForeignKey(Service,on_delete=models.CASCADE,default=1)
    
    slot1_start     = models.TimeField(default=timezone.now(),blank=True)
    slot1_end       = models.TimeField(default=timezone.now(),blank=True)

    slot2_start     = models.TimeField(default=timezone.now(),blank=True)
    slot2_end       = models.TimeField(default=timezone.now(),blank=True)
    
    slot3_start     = models.TimeField(default=timezone.now(),blank=True)
    slot3_end       = models.TimeField(default=timezone.now(),blank=True)


class Wednesday(models.Model):
    service         = models.ForeignKey(Service,on_delete=models.CASCADE,default=1)
    
    slot1_start     = models.TimeField(default=timezone.now(),blank=True)
    slot1_end       = models.TimeField(default=timezone.now(),blank=True)

    slot2_start     = models.TimeField(default=timezone.now(),blank=True)
    slot2_end       = models.TimeField(default=timezone.now(),blank=True)
    
    slot3_start     = models.TimeField(default=timezone.now(),blank=True)
    slot3_end       = models.TimeField(default=timezone.now(),blank=True)


class Thursday(models.Model):
    service         = models.ForeignKey(Service,on_delete=models.CASCADE,default=1)
    
    slot1_start     = models.TimeField(default=timezone.now(),blank=True)
    slot1_end       = models.TimeField(default=timezone.now(),blank=True)

    slot2_start     = models.TimeField(default=timezone.now(),blank=True)
    slot2_end       = models.TimeField(default=timezone.now(),blank=True)
    
    slot3_start     = models.TimeField(default=timezone.now(),blank=True)
    slot3_end       = models.TimeField(default=timezone.now(),blank=True)


class Friday(models.Model):
    service         = models.ForeignKey(Service,on_delete=models.CASCADE,default=1)
    
    slot1_start     = models.TimeField(default=timezone.now(),blank=True)
    slot1_end       = models.TimeField(default=timezone.now(),blank=True)

    slot2_start     = models.TimeField(default=timezone.now(),blank=True)
    slot2_end       = models.TimeField(default=timezone.now(),blank=True)
    
    slot3_start     = models.TimeField(default=timezone.now(),blank=True)
    slot3_end       = models.TimeField(default=timezone.now(),blank=True)


class Saturday(models.Model):
    service         = models.ForeignKey(Service,on_delete=models.CASCADE,default=1)
    
    slot1_start     = models.TimeField(default=timezone.now(),blank=True)
    slot1_end       = models.TimeField(default=timezone.now(),blank=True)

    slot2_start     = models.TimeField(default=timezone.now(),blank=True)
    slot2_end       = models.TimeField(default=timezone.now(),blank=True)
    
    slot3_start     = models.TimeField(default=timezone.now(),blank=True)
    slot3_end       = models.TimeField(default=timezone.now(),blank=True)


class Sunday(models.Model):
    service         = models.ForeignKey(Service,on_delete=models.CASCADE,default=1)
    
    slot1_start     = models.TimeField(default=timezone.now(),blank=True)
    slot1_end       = models.TimeField(default=timezone.now(),blank=True)

    slot2_start     = models.TimeField(default=timezone.now(),blank=True)
    slot2_end       = models.TimeField(default=timezone.now(),blank=True)
    
    slot3_start     = models.TimeField(default=timezone.now(),blank=True)
    slot3_end       = models.TimeField(default=timezone.now(),blank=True)


class InAppBookingNotifications(models.Model):
    from_user_id           =    models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,default=1)
    from_user_name      =    models.CharField(default="From User Name",max_length=250)
    to_user_id             =    models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,default=1,related_name="to_user")
    to_user_name        =    models.CharField(default="To User Name",max_length=250)
    notification_type   =    models.CharField(default="Notification Type",max_length=250)
    notification_title  =    models.CharField(default="Notification Title",max_length=250)
    service_name             =    models.CharField(default="Notification Body",max_length=250)
    service_slot_start  =    models.TimeField(default=timezone.now(),blank=True)
    service_slot_end    =    models.TimeField(default=timezone.now(),blank=True)
    requested_service_time = models.TimeField(default=timezone.now(),blank=True)
    requested_service_date = models.DateField(default=timezone.now(),blank=True)
    notification_time   =    models.TimeField(default=timezone.now(),blank=True)
    notification_date    =   models.DateField(default=timezone.now(),blank=True)
    service_pricing     =    models.CharField(default="0.0",max_length=250)
    service_place       =    models.CharField(default="Service Place",max_length=250)
    notification_read   =    models.BooleanField(default=False)
    rescheduled_date    =   models.DateField(default=timezone.now(),blank=True)
    rescheduled_time    =   models.TimeField(default=timezone.now(),blank=True)
    notification_body   =   models.TextField(blank=True)
#     to_user_usertype    =   models.CharField(blank=True,choices = USERTYPE,max_length=20)
    to_user_usertype    =   models.CharField(blank=True,max_length=20)
    notification_created = models.DateTimeField(default=timezone.now)
    


class TestTable(models.Model):
    sample_text         =   models.CharField(default="Some Text",max_length=250)



        
class Favourites(models.Model):
    user      = models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE)
    provider  = models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,related_name="provider")

    def __str__(self):
        return str(self.user) + " - " + str(self.provider)

    class Meta:
        verbose_name_plural = "Favourites"


class BannerImage(models.Model):
    banner_img_file = models.FileField(blank=False, null=False,upload_to='marketing/img',default='marketing/img/default.jpg')
    
    banner_name            = models.CharField(max_length=200,null=True,default="sample title")
    banner_name_in_arabic  = models.CharField(max_length=200,null=True,default="الفئة")
    
    description            = models.CharField(max_length=200,null=True,default="sample info")
    description_in_arabic  = models.CharField(max_length=200,null=True,default="الفئة")
    
    def __str__(self):
        return str(self.banner_img_file)


    


class BankingInfo(models.Model):
    card_holder         =   models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,related_name="BankingInfo")
    card_holder_name    =   models.CharField(max_length=40,null=True,blank=True)
    credit_card_number  =   models.CharField(max_length=40,null=True,blank=True)
    credit_card_masked  =   models.CharField(max_length=40,null=True,blank=True)
    valid_upto          =   models.CharField(max_length=40,null=True,blank=True)
    holder_usertype     =   models.CharField(max_length=10,null=True,blank=True)
#     available_balance   =   models.DecimalField(default=0.0,

    def __str__(self):
        if self.card_holder_name == "" or None:
            return str(self.credit_card_masked)
        else:
            return str(self.card_holder_name) + "-" + str(self.credit_card_masked)


PAYMENT_CHOICES = (
    ('Card','Card'),
    ('Cash','Cash')
)

class LivePayments(models.Model):
    payment_card                =   models.ForeignKey(BankingInfo,on_delete=models.CASCADE,blank=True,null=True)
    payment_method              =   models.CharField(max_length=30,choices=PAYMENT_CHOICES)
    payment_request_date        =   models.DateField(default=timezone.now)
    payment_request_time        =   models.TimeField(default=timezone.now)
    payment_settle_date         =   models.DateField(default=timezone.now)
    payment_settle_time         =   models.TimeField(default=timezone.now)
    service                     =   models.ForeignKey(Service,blank=True,null=True,on_delete=models.CASCADE)
    payment_settled             =   models.BooleanField(default=False)
    payment_from                =   models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,related_name="Live_Payments_From")
    payment_to                  =   models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,related_name="Live_Payments_To")
#     transaction_id              =   models.CharField(default="MPAY0000000000000",blank=True,null=True)
#     booking_ref                 =   models.ForeignKey(NewBookings,on_delete=models.CASCADE)
    booking_ID                  =   models.CharField(max_length=70,blank=True,null=True)
    cash_paid_by_requestor      =   models.BooleanField(default=False)
    cash_collected_by_provider       =   models.BooleanField(default=False)
    admin_charges              =   models.DecimalField(default=0,decimal_places=2,max_digits=12)
    service_charges             = models.DecimalField(default=0,decimal_places=2,max_digits=12)



class CardTransactionMaster(models.Model):

    response_amount                     =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_approval_code              =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_card_expiry                =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_card_holder_name           =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_card_number                =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_currency_iso               =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_gateway_name               =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_gateway_status             =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_gateway_status_description =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_merchant_id                =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_rrn                        =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_secure_hash                =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_status_code                =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_status_description         =   models.CharField(default="",blank=True,null=True,max_length=80)
    response_transaction_id             =   models.CharField(default="",blank=True,null=True,max_length=80)

    raw_json_response_string            =   models.CharField(default="",blank=True,null=True,max_length=5000)

    payment_for                        =   models.CharField(default="",blank=True,null=True,max_length=80)
    service_id                          =   models.ForeignKey(Service,on_delete=models.CASCADE,blank=True,null=True,related_name="transaction_master_service")
    booking                             =   models.ForeignKey(NewBookings,on_delete=models.CASCADE,blank=True,null=True,related_name="transaction_master_booking_id")
    # booking_id                          =   models.CharField(default="",blank=True,null=True,max_length=80)
    service_requestor                   =   models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,blank=True,null=True,related_name="transaction_master_requestor")
    service_provider                    =   models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,blank=True,null=True,related_name="transaction_master_provider")







class SettledPayments(models.Model):
    payment_card                =   models.ForeignKey(BankingInfo,on_delete=models.CASCADE,blank=True,null=True,related_name="Settled_Payments")
    payment_method              =   models.CharField(max_length=30,choices=PAYMENT_CHOICES)
    payment_request_date        =   models.DateField(default=timezone.now)
    payment_request_time        =   models.TimeField(default=timezone.now)
    payment_settle_date         =   models.DateField(default=timezone.now)
    payment_settle_time         =   models.TimeField(default=timezone.now)
    service                     =   models.ForeignKey(Service,blank=True,null=True,on_delete=models.CASCADE,related_name="Settled_Payments")
    payment_from                =   models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,related_name="Settled_Payments_From")
    payment_to                  =   models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,related_name="Settled_Payments_To")
    booking_ID                  =   models.CharField(max_length=70,blank=True,null=True)
    cash_paid_by_requestor      =   models.BooleanField(default=False)
    cash_collected_by_provider  =   models.BooleanField(default=False)
    admin_charges               =   models.DecimalField(default=0,decimal_places=2,max_digits=12)
    service_charges             =   models.DecimalField(default=0,decimal_places=2,max_digits=12)
    total_amount_paid           =   models.DecimalField(default=0,decimal_places=2,max_digits=14)
    transaction_type            =   models.CharField(default="",blank=True,null=True,max_length=70)
    gateway_merchant_id         =   models.CharField(default="",blank=True,null=True,max_length=70)
    gateway_transaction_id      =   models.CharField(default="",blank=True,null=True,max_length=70)                 
    transaction                 =   models.ForeignKey(CardTransactionMaster,on_delete=models.CASCADE,blank=True,null=True,related_name="settled_payments_transaction")         
    active                      =   models.BooleanField(default=True)
    payment_for                 =   models.CharField(default="",max_length=20,blank=True,null=True)

class SettledPaymentsCancel(models.Model):
    payment_card                =   models.ForeignKey(BankingInfo,on_delete=models.CASCADE,blank=True,null=True,related_name="Settled_PaymentsCancel")
    payment_method              =   models.CharField(max_length=30,choices=PAYMENT_CHOICES)
    payment_request_date        =   models.DateField(default=timezone.now)
    payment_request_time        =   models.TimeField(default=timezone.now)
    payment_settle_date         =   models.DateField(default=timezone.now)
    payment_settle_time         =   models.TimeField(default=timezone.now)
    service                     =   models.ForeignKey(Service,blank=True,null=True,on_delete=models.CASCADE,related_name="Settled_PaymentsCancel")
    payment_from                =   models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,related_name="Settled_Payments_Cancel_From")
    payment_to                  =   models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,related_name="Settled_Payments_Cancel_To")
    booking_ID                  =   models.CharField(max_length=70,blank=True,null=True)
    cash_paid_by_requestor      =   models.BooleanField(default=False)
    cash_collected_by_provider  =   models.BooleanField(default=False)
    admin_charges               =   models.DecimalField(default=0,decimal_places=2,max_digits=12)
    service_charges             =   models.DecimalField(default=0,decimal_places=2,max_digits=12)
    total_amount_paid           =   models.DecimalField(default=0,decimal_places=2,max_digits=14)
    transaction_type            =   models.CharField(default="",blank=True,null=True,max_length=80)
    gateway_merchant_id         =   models.CharField(default="",blank=True,null=True,max_length=80)
    gateway_transaction_id      =   models.CharField(default="",blank=True,null=True,max_length=80)                 
    transaction                 =   models.ForeignKey(CardTransactionMaster,on_delete=models.CASCADE,blank=True,null=True,related_name="Settled_Payments_Cancel_transaction")     
    payment_for                 =   models.CharField(default="",max_length=20,blank=True,null=True)   

class SettledPaymentsRefund(models.Model):
    payment_card                =   models.ForeignKey(BankingInfo,on_delete=models.CASCADE,blank=True,null=True,related_name="Settled_Payments_Refund_Refund")
    payment_method              =   models.CharField(max_length=30,choices=PAYMENT_CHOICES)
    payment_request_date        =   models.DateField(default=timezone.now)
    payment_request_time        =   models.TimeField(default=timezone.now)
    payment_settle_date         =   models.DateField(default=timezone.now)
    payment_settle_time         =   models.TimeField(default=timezone.now)
    service                     =   models.ForeignKey(Service,blank=True,null=True,on_delete=models.CASCADE,related_name="Settled_Payments_Refund_Service")
    payment_from                =   models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,related_name="Settled_Payments_Refund_From")
    payment_to                  =   models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,related_name="Settled_Payments_Refund_To")
    booking_ID                  =   models.CharField(max_length=70,blank=True,null=True)
    cash_paid_by_requestor      =   models.BooleanField(default=False)
    cash_collected_by_provider  =   models.BooleanField(default=False)
    admin_charges               =   models.DecimalField(default=0,decimal_places=2,max_digits=12)
    service_charges             =   models.DecimalField(default=0,decimal_places=2,max_digits=12)
    total_amount_paid           =   models.DecimalField(default=0,decimal_places=2,max_digits=14)
    transaction_type            =   models.CharField(default="",blank=True,null=True,max_length=80)
    gateway_merchant_id         =   models.CharField(default="",blank=True,null=True,max_length=80)
    gateway_transaction_id      =   models.CharField(default="",blank=True,null=True,max_length=80)
    transaction                 =   models.ForeignKey(CardTransactionMaster,on_delete=models.CASCADE,blank=True,null=True,related_name="Settled_Payments_Refund_Transaction")                 







class TempTable(models.Model):

    raw_json_response_string            =   models.CharField(default="",blank=True,null=True,max_length=100)


class ServiceFeedback(models.Model):
    booking_id  = models.ForeignKey(NewBookings,on_delete=models.CASCADE,blank=True,null=True)
    service_id  = models.ForeignKey(Service,on_delete=models.CASCADE, blank=True,null=True)
    feedback_user = models.ForeignKey(UserOtherInfo,on_delete=models.CASCADE,blank=True,null=True)
    rating        = models.PositiveIntegerField(default=1,blank=True,null=True)
    compliment    =  models.IntegerField(default=0)
    review        = models.TextField(max_length=500,blank=True,null=True)
    feedback_date = models.DateField(default=timezone.now())
    feedback_time = models.TimeField(default=timezone.now())
    marked_for_moderation = models.BooleanField(default=False)




    


class ServiceSpecificQuestions(models.Model):
    
    
    question_id  = models.CharField(max_length=20,blank=True,null=True)
    service =  models.ForeignKey(ServiceList,on_delete=models.CASCADE,blank=True,null=True)
    question_for_provider_english =  models.CharField(max_length=200,blank=True,null=True)
    question_for_provider_arabic  =  models.CharField(max_length=200,blank=True,null=True)
    
    question_for_requestor_english = models.CharField(max_length=200,blank=True,null=True)
    question_for_requestor_arabic = models.CharField(max_length=200,blank=True,null=True)
    
    

# @receiver(post_save, sender=ServiceSpecificQuestions, dispatch_uid="create_service_question_id")
# def create_question_id(sender, instance, **kwargs):
#     print("<-------------------Instance ID------------>",instance.id)
#     print("<-------------------Instance-------------->",instance)
#     print("<-------------------Instance Type----------->",type(instance))
#     instance.question_id = str('S' + str(instance.id))
#     instance.ServiceSpecificQuestions.save()
    
    
    
    
class ServiceSpecificOptions(models.Model):
    service = models.ForeignKey(ServiceList,on_delete=models.CASCADE,blank=True,null=True)
    question = models.ForeignKey(ServiceSpecificQuestions,on_delete=models.CASCADE,blank=True,null=True)
    option_english = models.CharField(max_length=200,blank=True,null=True)
    option_arabic  = models.CharField(max_length=200,blank=True,null=True)
    
    


class ServiceSpecificAnswersFilledByProvider(models.Model):
    service = models.ForeignKey(ServiceList,on_delete=models.CASCADE,blank=True,null=True)
    question = models.ForeignKey(ServiceSpecificQuestions,on_delete=models.CASCADE,blank=True,null=True)
    option_english = models.CharField(max_length=200,blank=True,null=True)
    option_arabic  =  models.CharField(max_length=200,blank=True,null=True)
    
    

    


class CommonQuestions(models.Model):
    
    question_id  = models.CharField(max_length=20,blank=True,null=True)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,blank=True,null=True)
    question_for_provider_english =  models.CharField(max_length=200,blank=True,null=True)
    question_for_provider_arabic  =  models.CharField(max_length=200,blank=True,null=True)
    
    question_for_requestor_english = models.CharField(max_length=200,blank=True,null=True)
    question_for_requestor_arabic = models.CharField(max_length=200,blank=True,null=True)
    


class CommonOptions(models.Model):
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,blank=True,null=True)
    question  = models.ForeignKey(CommonQuestions,on_delete = models.CASCADE,blank=True,null=True)
    option_english = models.CharField(max_length=200,blank=True,null=True)
    option_arabic = models.CharField(max_length=200,blank=True,null=True)
    
    
    
class CommonAnswersByProviders(models.Model):
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,blank=True,null=True)
    question = models.ForeignKey(CommonQuestions,on_delete=models.CASCADE,blank=True,null=True)
    option_english = models.CharField(max_length=200,blank=True,null=True)
    option_arabic  =  models.CharField(max_length=200,blank=True,null=True)    


class AdminCommision(models.Model):
    value = models.DecimalField(default=0,max_digits = 5, decimal_places = 2)
    active = models.BooleanField(default=True)
    commision_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name_plural = "Admin Charges"




class TestTime(models.Model):
    date_time = models.DateTimeField(default=timezone.now)

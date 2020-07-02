from django.contrib import admin

# Register your models here.
from .models import *
from services.models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class UserOtherInfoInline(admin.StackedInline):
    model = UserOtherInfo
    can_delete = False
    verbose_name_plural = 'UserOtherInfos'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserOtherInfoInline,)
    read_only_fields = ('id',)
    list_display = BaseUserAdmin.list_display + ('last_login',)


class ServiceAdmin(admin.ModelAdmin):
	search_fields = ('service_name',)
	



admin.site.unregister(User)
admin.site.register(Service,ServiceAdmin)

admin.site.register(User, UserAdmin)



admin.site.register([ProvidersRating,BannerImage,TestTable,FeaturedServiceProviders,Category,ImageUploadTest,NewService,NewBookings,SubCategory,City,Otp,Token,Slots,days,ServiceImage,DayAndSlots,Something,
	RawBooking,CanceledBooking,Rating,QuestionFilledByAdmin,AnswerByProvider,OptionsFilledbyAdmin,
    ReScheduledAppointment,OngoingBooking,CompletedBooking,ServiceFeedback,MeenFeeFeedback,
    PaymentMethod,HelpAndSupport,UserOtherInfo,FeaturedProviders,
    TrendingProviders,MostRecentProviders,MarketingCarousel,InAppBookingNotifications,ServiceSchedule,
    BankingInfo,LivePayments,SettledPayments,ContentMaster,ServiceList,ServiceSpecificQuestions,ServiceSpecificOptions,
    ServiceSpecificAnswersFilledByProvider,CommonQuestions,CommonOptions,CommonAnswersByProviders,Favourites,AdminCommision,TempTable,
    CardTransactionMaster,SettledPaymentsCancel,SettledPaymentsRefund,TestTime])

admin.site.site_header = 'Meenfee Administration'
admin.site.site_title = 'Meenfee'
admin.site.index_title = 'Meenfee Database'


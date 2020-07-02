from django.contrib import admin
from django.conf.urls import url,include
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from django.views.generic import TemplateView


urlpatterns = [

	# <---------------------Tested APIs------------------------->
	#this is simple City List API
	# path('cities/',views.CityListAPIView.as_view(),name="cities"),
	#this is simply category list API view
    path('categories/',views.CategoryListAPIView.as_view(),name="categories"),
	#for to get subcategories of particular category we have to pass category id as input
    # path('subcategories/',views.SubCategoryListAPIView.as_view(),name="subcategories"),
	# <---------------------have test them once---------------------->
	#Once requestor will add his card detail the booking will came into ongoing booking
    # path('ongoingbookings', views.OngoingBookingsListAPIView.as_view(),name="OngoingBookings"),
	#Requestor can cancel the appointment 
   	# path('cancelbooking', views.CancelAppointmentAPIView.as_view(),name="CancelAppointment"),
	#requestor can re-schedule the appointments
   	# path('re-schedule-appointment', views.ReScheduleAppointmentAPIView.as_view(),name="ReScheduleAppointment"),
	# path('re-schedule-confirm',views.ReScheduleAppointmentConfirmAPIView.as_view(),name="ReScheduleConfirmAppointment"),

	#     <-----------------------Tested APIs------------------------>
	#Provider can create his own services associated with profile
   	path('createservice', views.CreateServiceAPIView.as_view(),name="CreateService"),
	# path('createservicecopy', views.CreateServiceAPIViewCopy.as_view(),name="CreateService"),
	# a general user can give direct feedback meenfee services
	path('feedback/create',views.MeenFeeFeedbackCreateAPIView.as_view(),name="meenfeeFeedback"),
	#admin can add meenfee support detail from admin panel 
	path('meenfeesupport',views.HelpAndSupportListAPIView.as_view(),name="helpAndSupport"),
	#provider can see his profile along with services
	# path('provider/profile', views.ProviderProfileAPIView.as_view(),name="ProviderProfileAPIView"),
	#admin can add promoted providers through admin panel
	# path('provider/profile',views.ProviderProfileAPIView.as_view(),name="Provide Profile"),
	# path('featured/providers', views.FeaturedProvidersListAPIView.as_view(),name="FeaturedProfileView"),
	# currently this is under doubt section
	# path('trending/providers', views.TrendingProvidersListAPIView.as_view(),name="FeaturedProfileView"),
	# currently this is under doubt section
	# path('mostrecent/providers', views.FeaturedProvidersListAPIView.as_view(),name="FeaturedProfileView"),
	#provider can see the services he has created 
	# path('provider/services', views.ProviderServicesAPIView.as_view(),name="ProviderServices"),
	
	# path('allservices', views.AllServicesAPIView.as_view(),name="All Services"),

	# path('allservicestemp',views.AllServicesAPIViewTemp.as_view(),name="All Services Temp"),
	#provider can see his availabilities in calender tab
	# path('available/services', views.ProviderServicesAvailablityListAPIView.as_view(),name="ProviderServicesAvailablity"),
	#create a booking by requestor then provider will be notified
	# path('rawbooking/create', views.RawBookingCreateAPIView.as_view(),name="RawBookingCreate"),
	#accept and reject the booking request by requestor
	# path('booking/accepted', views.BookingAceptedUpdateAPIView.as_view(),name="BookingAccepted"),
	#redirect if doesnt have idcardnumber
	# path('update/idcardnumber', views.IdcardNumberUpdateAPIView.as_view(),name="UpdateIdcardnumber"),
	#Request can add their card detail
	# path('add/payment',views.PaymentTokenUpdateAPIView().as_view(),name ="addCard"),
	#requestor can see his bookings summary
	# path('booking/summary',views.BookingSummaryListAPIView().as_view(),name ="booking summary"),
	#requestor can see his cancel bookings
	# path('canceled/bookings',views.MyCanceledBookingsListAPIView().as_view(),name ="Canceled Bookings"),
	#Confirm bookings as provider or requestor
	# path('confirm/booking',views.BookingConfirmAPI.as_view(),name = "Confirm Booking"),
	#questions with options for requestor 
	path('questions/answers/requestor/list',views.QuestionAnswerForRequestorList.as_view(),name = "Question with options for Requestor"),
	#questions with options for provider
	path('questions/answers/provider/list',views.QuestionAnswerForProviderList.as_view(),name = "Question with options for provider"),
	#answers for provider
	path('questions/answers/provider/create',views.AnswerbyProviderCreateAPIView.as_view(),name = "Question Answer for Provider"),
	#filtered services on the basis of question answers
	# path('filtered/services',views.FilteredServicesList.as_view(),name = "filtered Services on the basis of answers filled by requestor"),
	#update user Other Information
	path('update/userInfo',views.UserProfileUpdateAPIView.as_view(),name = "Update user info"),

	#get fcm token of the user
	path('sendfcmtoken/',views.FcmTokenUpdateAPIView.as_view(),name = "update fcm token"), 
	# path('update/fcmtoken',views.FcmTokenUpdateAPIView.as_view(),name = "update fcm token"),
	#give rating to a user
	# path('rating/create',views.RatingCreateAPIView.as_view(),name = "create rating"),
	#Search Results
	# path('search/results',views.SearchResult.as_view(),name = "search result"),
	#Email verify link generate
	# path('email/link-generate',views.GenerateEmailVerificationLinkAPIView.as_view(),name ="Email verification link generation"),
	#Email verify by clicking on the link
	# url(r'^email/link-verify/(?P<id>[\w\.-]+)/', views.EmailVerifyAPIView),
	#Email Otp generate 
	# path('email/otp-generate',views.EmailOtpGenerateView.as_view(),name='Password reset through Otp on email'),
	#Email Otp verify
	# path('email/otp-verify',views.EmailOtpVerifyView.as_view(),name='Password reset through Otp on email'),
	#Shedule creation
	# path('shedule/create',views.CreateSheduleView.as_view(),name = "Shedule create"),
	#Update Shedule 
	# path('shedule/update',views.UpdateSheduleView.as_view(),name="Update shedule"),
	path('admin/users',views.UserdetailListAPIView.as_view(),name="users"),

	path('provideranswers/',views.AnswerByProv.as_view(),name="Provider Answer"),


	# path('serviceimageupload/',views.ServiceImageUploadAPIVIew.as_view(),name="Service Image Upload"),


	path('newbooking/',views.NewBooking.as_view(),name="New Booking"),
	path('viewActiveBookingRequestor/',views.ViewActiveBookingsRequestor.as_view(),name="View Active Booking Requestor"),
	path('viewActiveBookingProvider/',views.ViewActiveBookingsProvider.as_view(),name="View Active Booking Provider"),
	path('acceptBooking/',views.AcceptBooking.as_view(),name="Accept Booking"),
	# path('markBookingAccepted/',views.ViewBookingAccepted.as_view(),name="Booking Accepted"),
	path('viewCompletedTasks/',views.ViewCompletedTask.as_view(),name="View Completed Task"),
	path('rescheduleBooking/',views.RescheduleBooking.as_view(),name="Reschedule Booking"),
	path('markCompleted/',views.MarkTaskCompleted.as_view(),name="Mark as Completed"),
	# path('imageuploadtest/',views.ImageUploadTestAPIView.as_view(),name="Image Upload Test API View"),
	path('ansByProvider/',views.AnswerByProvider,name="Answer By Provider"),
	path('marketing/campaign/',views.MarketingCarouselAPIView.as_view(),name="Marketing Campaign"),
	path('viewpendingactionsonproviderend/',views.ViewPendingActionsOnProviderEnd.as_view(),name="View Pending Action Provider End"),
	path('viewpendingrequesterend/',views.ViewPendingActionsOnRequesterEnd.as_view(),name="View Requester Action"),
	path('providers/trending/',views.TrendingProvidersAPIVIew.as_view(),name="Trending Providers"),
	# path('sendnotif/',views.SendNotification.as_view(),name="SendNotification"),
	path('providers/featured/',views.FeaturedProviders.as_view(),name="Featured Providers"),
	path('providers/recent/',views.MostRecentProviders.as_view(),name="Recent Provider"),
	path('providers/search/',views.SearchProvider.as_view(),name="Search Provider"),


	# path('testdata/',views.TestWrite.as_view(),name="Test Write"),
	# path('fetchtest/',views.FetchTestWrite.as_view(),name="Fetch Test Write"),

	path('self/service/',views.SelfServices.as_view(),name="Self Service"),
	path('self/profile/',views.MyProfile.as_view(),name="Self Profile"),

	path('services/sort/price/',views.SortByPricing.as_view(),name="Sort By Pricing"),
	path('services/sort/rating/',views.SortByRating.as_view(),name="Sort By Rating"),
	path('services/sort/distance/',views.SortByDistance.as_view(),name="Sort By Distance"),
	path('services/sort/response/',views.SortByResponseTime.as_view(),name="Sort By Response"),
	

	path('viewnotifcations/',views.ViewAllNotifications.as_view(),name="View All Notification"),
	path('mark_notification_as_read/',views.MarkNotificationAsRead.as_view(),name="Mark Notification as view"),
	path('clear_all_notifications/',views.ClearAllNotification.as_view(),name="Clear All Notifications"),

	path('mark_as_favourite/',views.MarkProviderAsFavourite.as_view(),name="Mark As Favourite"),


	path('test/featured/',views.TestFeatured.as_view(),name="Test Featured"),
		# path('cancelBooking/',views.CancelBookingAPIView.as_view(),name="Cancel Booking")
	
	#Added Joelcode for APi 27June	
	path('services/filtered/',views.FilterServicesList.as_view(),name="Filtered Services"),
	path('check/time_slots',views.CheckTimeSlots.as_view(),name="Check Time Slots"),
	
	path('booking/cancel/',views.CancelAppointment.as_view(),name="Cancel Appointment"),
	#path('submit/feedback',views.SubmitFeedback.as_view(),name="SubmitFeedback"),
	
	path('profile/edit',views.EditProfile.as_view(),name="Edit Profile"),

	path('service/edit/',views.EditService.as_view(),name="EditService"),

	path('calender/days',views.BookingCalender.as_view(),name="Booking Calender"),

	# path('populateDB',views.PopulateDB.as_view(),name="PopulateDB"),
	
	path('validateAndSaveCard/',views.ValidateAndSaveCard.as_view(),name="ValidateAndSaveCard"),
	
	path('fetch/savedCards',views.FetchSavedCards.as_view(),name="FetchSavedCards"),
	
	path('record/payment',views.RecordPayment.as_view(),name="RecordPayment"),

	path('submit/feedback',views.SubmitFeedback.as_view(),name="SubmitFeedback"),
	
	path('review/moderation',views.MarkReviewForModeration.as_view(),name="Mark Review for moderation"),
	
	path('fetch/legal_text',views.FetchLegalText.as_view(),name="Fetch Terms and Conditions"),
	
	path('session/test',views.TestServices.as_view(),name="Session_Test"),
	
	path('session/fetch',views.FetchSession.as_view(),name="Session_Fetch"),
	
	path('cash_collected_by_provider',views.MarkCashCollectedByProvider.as_view(),name="CashCollectedByProvider"),
	
	path('cash_paid_by_requestor',views.MarkCashPaidByRequestor.as_view(),name="CashPaidByProvider"),
	
	path('fetch/questions/provider',views.FetchQuestionsForProvider.as_view(),name="FetchQuestionsForProvider"),
	path('fetch/questions/requestor',views.FetchQuestionsForRequestor.as_view(),name="FetchQuestionsForRequestor"),
	
	# path('test/union',views.TestUninon.as_view(),name="Test Union"),
	path('managebooking/prodetails',views.ManageBookingProDetails.as_view(),name="ManageBookingProDetails"),
	
	path('fetch/monthavailability',views.FetchMonthAvailability.as_view(),name="FetchMonthAvailability"),

	path('populateDBV2',views.PopulateDBNew.as_view(),name="Populate DB V2"),
	
	path('notifications/read_all',views.ReadAllNotifications.as_view(),name="Read All Notifications"),
	
	# path('monthnew/',views.FetchMonthAvail.as_view(),name="FetchMonthNew"),
	
	# path('test/payment',views.TestClass.as_view(),name="TestPayment"),

	# path('test/transaction',views.TestTransaction.as_view(),name="TestTransaction"),

	path('payment/capture/',views.CapturePaymentResponse.as_view(),name="PaymentCapture"),

	path('fetch/admincharges',views.FetchAdminCharges.as_view(),name="FetchAdminCharges"),

	# path('test/time',views.TestTimeView.as_view(),name="TestTime"),

	path('fetch/user-data',views.FetchUserDetails.as_view(),name="FetchUserDetails"),

	path('randomize/arabic',views.RandomizeArabicStrings.as_view(),name="RandomizeArabic"),

	path('translate/questions/',views.QuestionStringToArabic.as_view(),name="TranslateQuestions"),

	path('insert/questions',views.InsertQuestion.as_view(),name="InsertQuestions")
# 	path('fetch/monthavailability/new',views.FetchMonthAvailabilityNew.as_view(),name="FetchMonthAvailabilityNew"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT

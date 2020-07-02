from django.urls import path

from . import views

urlpatterns = [
    path('', views.service_main, name='service_main'),
    path('add-service', views.add_service, name='add_service'),
    path('add-category', views.add_category, name='add_category'),
    path('add-subcategory', views.add_subcategory, name='add_subcategory'),    
    path('category-list', views.catgory_list, name='catgory_list'),
    path('subcate-list', views.subcategory_list, name='subcategory_list'),    
    path('catedelete/<int:id>/', views.delete_category, name='delete_category'),
    path('scatedelete/<int:id>/', views.delete_subcategory, name='delete_subcategory'),    
    path('get_table_values', views.get_table_values, name='get_table_values'),
    path('services-list', views.services_list, name='services_list'),    
    path('servicedelete/<int:id>/', views.delete_service, name='delete_service'), 
    path('add-content', views.add_content, name='add_content'), 
    path('content-list', views.content_list, name='content_list'),
    path('contentdelete/<int:id>/', views.delete_content, name='delete_content'),     
    path('banner-list', views.banner_list, name='banner_list'),    
    path('bannerdelete/<int:id>/', views.delete_banner, name='delete_banner'), 
    path('add-banner', views.add_banner, name='add_banner'),  
    path('userrating-list', views.userrating_list, name='userrating_list'),
    path('add-rating', views.add_rating, name='add_rating'),
    path('edit-service/<int:id>/', views.edit_service, name='edit_service'),
    
    path('edit-images/<int:id>/', views.edit_image, name='edit_image'),    
    path('payment', views.payment_process, name='payment_process'),
    
    path('add-rating', views.add_rating, name='add_rating'),
    path('deleterating', views.delete_rating, name='delete_rating'),
    path('list-rating', views.list_rating, name='list_rating'),
   
    path('list-pservices/<int:id>/', views.list_pservices, name='list_pservices'),
    path('list-pservices-reviews/<int:id>/', views.list_pservices_reviews, name='list_pservices_reviews'),
    path('mod-review/<int:id>/', views.mod_review, name='mod_review'),
    
    
    path('payment-list', views.payment_list, name='payment_list '),
    path('pay-refund-list', views.pay_refund_list, name='pay_refund_list'),
    path('pay-complete-list', views.pay_complete_list, name='pay_complete_list'),   
    
    path('list-questions', views.list_questions, name='list_questions '), 
    path('list-answers/<int:id>/', views.list_answers, name='list_answers'),
    
    path('deletequestion/<int:id>/', views.delete_question, name='delete_question'),
    path('deleteanswer/<int:id>/', views.delete_answer, name='delete_answer'),
    
    path('edit-category/<int:id>/', views.edit_category, name='edit_category'),
    
    path('related-subcategory/<int:id>/', views.related_subcategory, name='related_subcategory'),
    path('edit-subcategory/<int:id>/', views.edit_subcategory, name='edit_subcategory'),
    path('edit-banner/<int:id>/', views.edit_banner, name='edit_banner'),
    
    path('add-questions/<int:id>/', views.add_questions, name='add_questions'),
    path('type-questions/', views.type_questions, name='type_questions'),
    path('get_services_values', views.get_services_values, name='get_services_values'), 
    
    path('service_based_questions/<int:id>/', views.service_based_questions, name='service_based_questions'),

    path('deactivate-payment/<int:id>/',views.deactivate_payments,name='deactivate_payments')
           
]
#ClixAdm?!6611

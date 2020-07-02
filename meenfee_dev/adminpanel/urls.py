from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('userlist/', views.user_list, name='user_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('adduser/', views.add_user, name='add_user'),
    path('userdelete/<int:id>/', views.user_delete, name='user_delete'),
    path('logout/', views.logout_site, name='logout'),
    path('login/', views.login_user, name='login_user'),
    path('changepw/', views.change_password, name='change_password'),    
    path('switch_link/', views.switch_to_English_link, name='switch_to_English_link'),     
    path('reset_password/', views.ResetPasswordRequestView.as_view(), name="reset_password"),    
    path('success_mail_send/', views.success_mail_send, name='success_mail_send'),    
    path('reset_password_confirm/(?P<id>[0-9A-Za-z]+)-(?P<token>.+)/', views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('^export/csv/$', views.export_users_csv, name='export_users_csv'),
    
    path('user-detail/<int:id>/', views.user_details, name='user_details'),
    path('bDelete/', views.bulk_delete, name='bulk_delete'),
   
    path('mark_featured/',views.mark_provider_as_featured,name='mark_provider_as_featured'),
    path('unmark_as_featured/',views.unmark_provider_as_featured,name="unmark_provider_as_featured"),    
    path('mark_id_as_verified/',views.mark_id_verified,name="mark_id_verified"),    
    path('deactivate/account/',views.deactivate_account,name="deactivate_account"),

    path('manage_commission/',views.manage_commission,name="manage_commission"),

    path('add-commission/',views.add_commission,name="add_commission"),
    path('list-commission/',views.list_commission,name="list_commission"),
    
]
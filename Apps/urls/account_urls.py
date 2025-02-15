from django.urls import path
from ..views.account_views import Account_view

urlpatterns=[
    path('account',Account_view.get_Account,name='get_Account'),
    path('accountid',Account_view.get_Accountid,name='get_Accountid'),
    path('account/create',Account_view.create_Account,name='create_Account'),
    path('account/login',Account_view.login,name='login'),
   
]
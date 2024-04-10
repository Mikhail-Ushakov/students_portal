from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.AccountLoginView.as_view(), name='login'),
    path('logout/', views.AccountLogoutView.as_view(), name='logout'),
    path('pass-change/', views.AccountPassChangeView.as_view(), name='pass-change'),
    path('pass-change/done', views.AccountPassChangeDoneView.as_view(), name='pass-change-done'),
    path('pass-reset/', views.AccPassResetView.as_view(), name='pass-reset'),
    path('pass-reset/done/', views.AccPassResetDoneView.as_view(), name='pass-reset-done'),
    path('pass-reset/confirm/<uidb64>/<token>/', views.AccPassResetConfirmView.as_view(), name='pass-reset-confirm'),
    path('pass-reset/complete/', views.AccPassResetCompleteView.as_view(), name='pass-reset-complete'),
    path('registration/', views.registr, name='registration'),
    path('edit/', views.edit_profile, name='edit-profile'),
    path('users/<user_name>/', views.user_detail, name='user-detail'),
    path('subscribe/<int:user_id>/<action>/', views.subscribe, name='subscribe'),
    path('users/', views.users_list, name='users-list'),
    path('', views.dashboard, name='dashboard'),
]
from django.urls import path
from .views import *


app_name = "core"

urlpatterns = [
    # auth routes
    path('', index, name='index'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('password/<str:token>/set', set_password, name='set_password'),
    path('password/forgot', forgot_password, name='forgot_password'),
    path('authentication', authentication, name='authentication'),

    # user routes
    path('profile', get_profiles, name='get_profiles'),
    path('profile/create', create_profile, name='create_profile'),
    path('profile/<int:profile_id>/update-profile-permissions', update_profile_permissions, name='update_profile_permissions'),
    path('profile/create/ao', create_ao, name='create_ao'),

    # user department routes
    path('user-department', get_user_departments, name='get_user_departments'),
    path('user-department/create', create_user_department, name='create_user_department'),
    path('user-department/<int:user_department_id>/head', get_user_department_head, name='get_user_department_head'),
    path('user-department/<int:user_department_id>/head/create', create_user_department_head, name='create_user_department_head'),
    path('user-department/<int:user_department_id>/head/update', update_user_department_head, name='update_user_department_head'),
    path('user-department/<int:user_department_id>/head/delete', delete_user_department_head, name='delete_user_department_head'),

    # timing routes
    path('timing', get_timing, name='get_timing'),
    path('timing/update', update_timing, name='update_timing'),

    # pdu routes
    path('pdu', get_pdu, name='get_pdu'),
    path('pdu/head/create', create_pdu_head, name='create_pdu_head'),
    path('pdu/head/update', update_pdu_head, name='update_pdu_head'),
    path('pdu/head/delete', delete_pdu_head, name='delete_pdu_head'),

    # buget routes
    path('budget', get_budgets, name='get_budgets'),
    path('budget/<int:user_department_id>/update', update_user_department_budget, name='update_user_department_budget'),

    # programme routes
    path('programme', get_programmes, name='get_programmes'),

    # expense routes
    path('expense', get_expenses, name='get_expenses'),

]

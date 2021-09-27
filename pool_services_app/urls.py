from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index),

    path('register',views.register),
    #line 25 in html
    path('login',views.login),
    #line 55 in html
    #login page
    path('login_page', views.login_page),

    path('logout', views.logout),

    #new page called dashboard
    path('dashboard',views.dashboard),

    #servive form
    path('services_form',views.services_form),

    # create service 
    path('services',views.services ),

    # service and quote display!
    path('services_quotes', views.services_quotes),

    #review your order Page!
    path('review_order/<int:id>',views.review_order),

        # Process review your order Page!
    path('process_order',views.process_order),

    #cancel
    path('cancel/<int:id>', views.cancel),
]
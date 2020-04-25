from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list', views.OpportunityList.as_view(), name='list'),
    #path('api/ref/', views.API_Reference.as_view(), name='api_reference'),
    #path('api/calls/', views.API_Calls.as_view(), name='api_calls'),
]

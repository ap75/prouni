from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list', views.OpportunityList.as_view(), name='list'),
    path('detail/<int:pk>', views.OpportunityDetail.as_view(), name='detail'),
]

from django.urls import path
from . import views, api_views

urlpatterns = [
    # path('', views.fund_list, name='fund_list'),
    # path('upload/', views.upload_funds, name='upload_funds'),
    path('api/', api_views.FundListAPIView.as_view(),
         name='api_fund_list'),
    path('api/<int:id>/', api_views.FundDetailAPIView.as_view(),
         name='api_fund_detail')

]
# for modularity. Could be done in the Fundproject URLs file which is project wide.

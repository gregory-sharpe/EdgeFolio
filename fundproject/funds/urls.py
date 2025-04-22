from django.urls import path
from . import views, api_views
# TODO allow filtering by
urlpatterns = [


    path('api/', api_views.FundListAPIView.as_view(),
         name='api_fund_list'),
    path('api/<int:id>/', api_views.FundDetailAPIView.as_view(),
         name='api_fund_detail'),
    path('upload/', views.upload_funds, name='upload_funds'),
    #     path('api/create/', api_views.FundCreateAPIView.as_view(),
    #          name='api_fund_create'),

]
# for modularity. Could be done in the Fundproject URLs file which is project wide.

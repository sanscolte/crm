from django.urls import path

from crm.views import (
    CreateServiceView,
    CreateAdvertisingCampaignView,
    CreatePotentialClientView,
    CreateContractView,
    CreateActiveClientView,

    ServiceListView,
    AdvertisingCampaignListView,
    PotentialClientListView,
    ContractListView,
    ActiveClientListView,

    ServiceDetailView,
    AdvertisingCampaignDetailView,
    PotentialClientDetailView,
    ContractDetailView,
    ActiveClientDetailView,

    ServiceDeleteView,
    AdvertisingCampaignDeleteView,
    PotentialClientDeleteView,
    ContractDeleteView,
    ActiveClientDeleteView,

    ServiceUpdateView,
    AdvertisingCampaignUpdateView,
    PotentialClientUpdateView,
    ContractUpdateView,
    ActiveClientUpdateView,

    StatisticsView,
)

app_name = 'crm'

urlpatterns = [
    path('create-service/', CreateServiceView.as_view(), name='create_service'),
    path('create-advertising-campaign/', CreateAdvertisingCampaignView.as_view(), name='create_advertising_campaign'),
    path('create-potential-client/', CreatePotentialClientView.as_view(), name='create_potential_client'),
    path('create-contract/', CreateContractView.as_view(), name='create_contract'),
    path('create-active-client/<int:pk>', CreateActiveClientView.as_view(), name='create_active_client'),

    path('services/', ServiceListView.as_view(), name='services'),
    path('advertising-campaigns/', AdvertisingCampaignListView.as_view(), name='advertising_campaigns'),
    path('potential-clients/', PotentialClientListView.as_view(), name='potential_clients'),
    path('contracts/', ContractListView.as_view(), name='contracts'),
    path('active-clients/', ActiveClientListView.as_view(), name='active_clients'),

    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service_details'),
    path('advertising-campaigns/<int:pk>/', AdvertisingCampaignDetailView.as_view(),
         name='advertising_campaign_details'),
    path('potential-clients/<int:pk>/', PotentialClientDetailView.as_view(), name='potential_client_details'),
    path('contracts/<int:pk>/', ContractDetailView.as_view(), name='contract_details'),
    path('active-clients/<int:pk>/', ActiveClientDetailView.as_view(), name='active_client_details'),

    path('services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),
    path('advertising-campaigns/<int:pk>/delete/', AdvertisingCampaignDeleteView.as_view(),
         name='advertising_campaign_delete'),
    path('potential-clients/<int:pk>/delete/', PotentialClientDeleteView.as_view(), name='potential_client_delete'),
    path('contracts/<int:pk>/delete/', ContractDeleteView.as_view(), name='contract_delete'),
    path('active-clients/<int:pk>/delete/', ActiveClientDeleteView.as_view(), name='active_client_delete'),

    path('services/<int:pk>/update/', ServiceUpdateView.as_view(), name='service_update'),
    path('advertising-campaigns/<int:pk>/update/', AdvertisingCampaignUpdateView.as_view(),
         name='advertising_campaign_update'),
    path('potential-clients/<int:pk>/update/', PotentialClientUpdateView.as_view(), name='potential_client_update'),
    path('contracts/<int:pk>/update/', ContractUpdateView.as_view(), name='contract_update'),
    path('active-clients/<int:pk>/update/', ActiveClientUpdateView.as_view(), name='active_client_update'),

    path('statistics/', StatisticsView.as_view(), name='statistics'),
]

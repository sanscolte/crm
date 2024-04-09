from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from crm.views import (
    CreateServiceView,
    CreateCampaignView,
    CreatePotentialClientView,
    CreateContractView,
    CreateActiveClientView,

    ServiceListView,
    CampaignListView,
    PotentialClientListView,
    ContractListView,
    ActiveClientListView,

    ServiceDetailView,
    CampaignDetailView,
    PotentialClientDetailView,
    ContractDetailView,
    ActiveClientDetailView,

    ServiceDeleteView,
    CampaignDeleteView,
    PotentialClientDeleteView,
    ContractDeleteView,
    ActiveClientDeleteView,

    ServiceUpdateView,
    CampaignUpdateView,
    PotentialClientUpdateView,
    ContractUpdateView,
    ActiveClientUpdateView,

    StatisticsView,
)

app_name = "crm"

urlpatterns = [
    path("create-service/", CreateServiceView.as_view(), name="create_service"),
    path("create-campaign/", CreateCampaignView.as_view(), name="create_campaign"),
    path("create-potential-client/", CreatePotentialClientView.as_view(), name="create_potential_client"),
    path("create-contract/", CreateContractView.as_view(), name="create_contract"),
    path("create-active-client/<int:pk>", CreateActiveClientView.as_view(), name="create_active_client"),

    path("services/", ServiceListView.as_view(), name="services"),
    path("campaigns/", CampaignListView.as_view(), name="campaigns"),
    path("potential-clients/", PotentialClientListView.as_view(), name="potential_clients"),
    path("contracts/", ContractListView.as_view(), name="contracts"),
    path("active-clients/", ActiveClientListView.as_view(), name="active_clients"),

    path("services/<int:pk>/", ServiceDetailView.as_view(), name="service_details"),
    path("campaigns/<int:pk>/", CampaignDetailView.as_view(), name="campaign_details"),
    path("potential-clients/<int:pk>/", PotentialClientDetailView.as_view(), name="potential_client_details"),
    path("contracts/<int:pk>/", ContractDetailView.as_view(), name="contract_details"),
    path("active-clients/<int:pk>/", ActiveClientDetailView.as_view(), name="active_client_details"),

    path("services/<int:pk>/delete/", ServiceDeleteView.as_view(), name="service_delete"),
    path("campaigns/<int:pk>/delete/", CampaignDeleteView.as_view(), name="campaign_delete"),
    path("potential-clients/<int:pk>/delete/", PotentialClientDeleteView.as_view(), name="potential_client_delete"),
    path("contracts/<int:pk>/delete/", ContractDeleteView.as_view(), name="contract_delete"),
    path("active-clients/<int:pk>/delete/", ActiveClientDeleteView.as_view(), name="active_client_delete"),

    path("services/<int:pk>/update/", ServiceUpdateView.as_view(), name="service_update"),
    path("campaigns/<int:pk>/update/", CampaignUpdateView.as_view(), name="campaign_update"),
    path("potential-clients/<int:pk>/update/", PotentialClientUpdateView.as_view(), name="potential_client_update"),
    path("contracts/<int:pk>/update/", ContractUpdateView.as_view(), name="contract_update"),
    path("active-clients/<int:pk>/update/", ActiveClientUpdateView.as_view(), name="active_client_update"),

    path("statistics/", cache_page(settings.CACHE_TIME)(StatisticsView.as_view()), name="statistics"),
]

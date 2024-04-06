from django.contrib import admin

from crm.models import (
    Service,
    AdvertisingCampaign,
    PotentialClient,
    Contract,
    ActiveClient,
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "description",
        "cost",
    )


@admin.register(AdvertisingCampaign)
class AdvertisingCampaignAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "service",
        "promotion_channel",
        "budget",
    )


@admin.register(PotentialClient)
class PotentialClientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "full_name",
        "phone",
        "email",
        "advertising_campaign",
    )


@admin.register(Contract)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "service",
        "document",
        "conclusion_date",
        "validity_period",
        "amount",
    )


@admin.register(ActiveClient)
class ActiveClientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "potential_client",
        "contract",
    )

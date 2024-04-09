from django.contrib import admin

from crm.models import (
    Service,
    Campaign,
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
    list_display_links = ("name",)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "service",
        "promotion_channel",
        "budget",
    )
    list_display_links = ("name",)


@admin.register(PotentialClient)
class PotentialClientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "full_name",
        "phone",
        "email",
        "campaign",
    )
    list_display_links = ("full_name",)


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
    list_display_links = ("name",)


@admin.register(ActiveClient)
class ActiveClientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "potential_client",
        "contract",
    )
    list_display_links = ("potential_client",)

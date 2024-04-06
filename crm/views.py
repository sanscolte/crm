from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DetailView, DeleteView, UpdateView

from crm.models import (
    Service,
    AdvertisingCampaign,
    PotentialClient,
    Contract,
    ActiveClient,
)


# PERMISSIONS GROUP CLASSES
class GroupRequiredMixin(UserPassesTestMixin):
    group_names = []

    def test_func(self):
        if not self.group_names:
            raise ImproperlyConfigured("Необходимо установить group_names в вашем представлении.")
        user_groups = self.request.user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in self.group_names)


class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


# CREATE VIEWS
class CreateServiceView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_names = ['Marketer', ]
    model = Service
    fields = '__all__'
    success_url = reverse_lazy('crm:services')


class CreateAdvertisingCampaignView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_names = ['Marketer', ]
    model = AdvertisingCampaign
    fields = '__all__'
    success_url = reverse_lazy('crm:advertising_campaigns')


class CreatePotentialClientView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_names = ['Operator', ]
    model = PotentialClient
    fields = '__all__'
    success_url = reverse_lazy('crm:potential_clients')


class CreateContractView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_names = ['Manager', ]
    model = Contract
    fields = '__all__'
    success_url = reverse_lazy('crm:contracts')


class CreateActiveClientView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_names = ['Manager', ]
    model = ActiveClient
    fields = 'contract',
    success_url = reverse_lazy('crm:active_clients')

    def form_valid(self, form):
        potential_client_id = self.kwargs.get('pk')
        form.instance.potential_client = PotentialClient.objects.get(pk=potential_client_id)
        return super().form_valid(form)


# LIST VIEWS
class ServiceListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_names = ['Marketer', ]
    model = Service


class AdvertisingCampaignListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_names = ['Marketer', ]
    model = AdvertisingCampaign


class PotentialClientListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_names = ['Operator', 'Manager']
    model = PotentialClient

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        potential_clients = self.get_queryset()

        active_clients = ActiveClient.objects.filter(potential_client__in=potential_clients)
        active_clients_ids = active_clients.values_list('potential_client_id', flat=True)

        context['active_clients_ids'] = active_clients_ids
        return context


class ContractListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_names = ['Manager', ]
    model = Contract


class ActiveClientListView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    queryset = ActiveClient.objects.select_related('potential_client')


# DETAIL VIEWS
class ServiceDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    group_names = ['Marketer', ]
    model = Service


class AdvertisingCampaignDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    group_names = ['Marketer', ]
    model = AdvertisingCampaign


class PotentialClientDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    group_names = ['Operator', ]
    model = PotentialClient


class ContractDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    group_names = ['Manager', ]
    model = Contract


class ActiveClientDetailView(LoginRequiredMixin, SuperUserRequiredMixin, DetailView):
    model = ActiveClient


# DELETE VIEWS
class ServiceDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('crm:services')


class AdvertisingCampaignDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):
    model = AdvertisingCampaign
    success_url = reverse_lazy('crm:advertising_campaigns')


class PotentialClientDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):
    model = PotentialClient
    success_url = reverse_lazy('crm:potential_clients')


class ContractDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):
    model = Contract
    success_url = reverse_lazy('crm:contracts')


class ActiveClientDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):
    model = ActiveClient
    success_url = reverse_lazy('crm:active_clients')


# UPDATE VIEWS
class ServiceUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_names = ['Marketer', ]
    model = Service
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('crm:services')


class AdvertisingCampaignUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_names = ['Marketer', ]
    model = AdvertisingCampaign
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('crm:advertising_campaigns')


class PotentialClientUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_names = ['Operator', ]
    model = PotentialClient
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('crm:potential_clients')


class ContractUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_names = ['Manager', ]
    model = Contract
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('crm:contracts')


class ActiveClientUpdateView(LoginRequiredMixin, SuperUserRequiredMixin, UpdateView):
    model = ActiveClient
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('crm:active_clients')


# TODO STATISTICS CACHE
class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        potential_clients = PotentialClient.objects.count()
        active_clients = ActiveClient.objects.count()
        total_income = sum(contract.amount for contract in Contract.objects.all())
        total_expenses = sum(campaign.budget for campaign in AdvertisingCampaign.objects.all())
        income_expenses_ratio = round((total_income / total_expenses if total_income > 0 else 0), 2)

        context['potential_clients'] = potential_clients
        context['active_clients'] = active_clients
        context['income_expenses_ratio'] = income_expenses_ratio

        return context

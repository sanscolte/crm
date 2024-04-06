from typing import List, Tuple, Any, Dict, Union

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    TemplateView,
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
)

from crm.models import (
    Service,
    AdvertisingCampaign,
    PotentialClient,
    Contract,
    ActiveClient,
)


# PERMISSIONS GROUP CLASSES
class GroupRequiredMixin(UserPassesTestMixin):
    """ Миксин проверки наличия пользователя в указанной группе прав group_names """
    group_names: List[str] = []

    def test_func(self):
        if not self.group_names:
            raise ImproperlyConfigured(
                "Необходимо установить group_names в вашем представлении."
            )
        user_groups = self.request.user.groups.values_list("name", flat=True)
        return any(group_name in user_groups for group_name in self.group_names)


class SuperUserRequiredMixin(UserPassesTestMixin):
    """ Миксин проверки пользователя на статус суперпользователя """
    def test_func(self):
        return self.request.user.is_superuser


# CREATE VIEWS
class CreateServiceView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """ Представление создания услуги """
    group_names: List[str] = [
        "Marketer",
    ]
    model = Service
    fields: Tuple[Tuple[str], str] = "__all__"
    success_url = reverse_lazy("crm:services")


class CreateAdvertisingCampaignView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """ Представление создания рекламной компании """
    group_names: List[str] = [
        "Marketer",
    ]
    model = AdvertisingCampaign
    fields: Tuple[Tuple[str], str] = "__all__"
    success_url = reverse_lazy("crm:advertising_campaigns")


class CreatePotentialClientView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """ Представление создания потенциального клиента """
    group_names: List[str] = [
        "Operator",
    ]
    model = PotentialClient
    fields: Tuple[Tuple[str], str] = "__all__"
    success_url = reverse_lazy("crm:potential_clients")


class CreateContractView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """ Представление создания контракта """
    group_names: List[str] = [
        "Manager",
    ]
    model = Contract
    fields: Tuple[Tuple[str], str] = "__all__"
    success_url = reverse_lazy("crm:contracts")


class CreateActiveClientView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """ Представление создания активного клиента """
    group_names: List[str] = [
        "Manager",
    ]
    model = ActiveClient
    fields: Tuple[str] = ("contract",)
    success_url = reverse_lazy("crm:active_clients")

    def form_valid(self, form):
        potential_client_id = self.kwargs.get("pk")
        form.instance.potential_client = PotentialClient.objects.get(
            pk=potential_client_id
        )
        return super().form_valid(form)


# LIST VIEWS
class ServiceListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """ Представление списка услуг """
    group_names: List[str] = [
        "Marketer",
    ]
    model = Service


class AdvertisingCampaignListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """ Представление списка рекламной компании """
    group_names: List[str] = [
        "Marketer",
    ]
    model = AdvertisingCampaign


class PotentialClientListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """ Представление списка потенциальных клиентов """
    group_names: List[str] = ["Operator", "Manager"]
    model = PotentialClient

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        potential_clients = self.get_queryset()

        active_clients = ActiveClient.objects.filter(
            potential_client__in=potential_clients
        )
        active_clients_ids = active_clients.values_list(
            "potential_client_id", flat=True
        )

        context["active_clients_ids"] = active_clients_ids
        return context


class ContractListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """ Представление списка контраков """
    group_names: List[str] = [
        "Manager",
    ]
    model = Contract


class ActiveClientListView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    """ Представление списка активных клиентов """
    queryset = ActiveClient.objects.select_related("potential_client")


# DETAIL VIEWS
class ServiceDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """ Представление списка деталей услуги """
    group_names: List[str] = [
        "Marketer",
    ]
    model = Service


class AdvertisingCampaignDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """ Представление списка деталей рекламной компании """
    group_names: List[str] = [
        "Marketer",
    ]
    model = AdvertisingCampaign


class PotentialClientDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """ Представление списка деталей потенциального клиента """
    group_names: List[str] = [
        "Operator",
    ]
    model = PotentialClient


class ContractDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """ Представление списка деталей контракта """
    group_names: List[str] = [
        "Manager",
    ]
    model = Contract


class ActiveClientDetailView(LoginRequiredMixin, SuperUserRequiredMixin, DetailView):
    """ Представление списка деталей активного клиента """
    model = ActiveClient


# DELETE VIEWS
class ServiceDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):  # type: ignore
    """ Представление удаления услуги """
    model = Service
    success_url = reverse_lazy("crm:services")


class AdvertisingCampaignDeleteView(  # type: ignore
    LoginRequiredMixin, SuperUserRequiredMixin, DeleteView
):
    """ Представление удаления рекламной компании """
    model = AdvertisingCampaign
    success_url = reverse_lazy("crm:advertising_campaigns")


class PotentialClientDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):  # type: ignore
    """ Представление удаления потенциального клиента """
    model = PotentialClient
    success_url = reverse_lazy("crm:potential_clients")


class ContractDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):  # type: ignore
    """ Представление удаления контракта """
    model = Contract
    success_url = reverse_lazy("crm:contracts")


class ActiveClientDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):  # type: ignore
    """ Представление удаления активного клиента """
    model = ActiveClient
    success_url = reverse_lazy("crm:active_clients")


# UPDATE VIEWS
class ServiceUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """ Представление редактирования услуги """
    group_names: List[str] = [
        "Marketer",
    ]
    model = Service
    fields: Union[Tuple[str], str] = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("crm:services")


class AdvertisingCampaignUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """ Представление редактирования рекламной компании """
    group_names: List[str] = [
        "Marketer",
    ]
    model = AdvertisingCampaign
    fields: Union[Tuple[str], str] = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("crm:advertising_campaigns")


class PotentialClientUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """ Представление редактирования потенциального клиента """
    group_names: List[str] = [
        "Operator",
    ]
    model = PotentialClient
    fields: Union[Tuple[str], str] = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("crm:potential_clients")


class ContractUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """ Представление редактирования контракта """
    group_names: List[str] = [
        "Manager",
    ]
    model = Contract
    fields: Union[Tuple[str], str] = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("crm:contracts")


class ActiveClientUpdateView(LoginRequiredMixin, SuperUserRequiredMixin, UpdateView):
    """ Представление редактирования активного клиента """
    model = ActiveClient
    fields: Union[Tuple[str], str] = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("crm:active_clients")


class StatisticsView(LoginRequiredMixin, TemplateView):
    """ Представление статистики """
    template_name = "crm/statistics.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        potential_clients: int = PotentialClient.objects.count()
        active_clients: int = ActiveClient.objects.count()
        total_income: int = sum(
            int(contract.amount) for contract in Contract.objects.all()
        )
        total_expenses: int = sum(
            int(campaign.budget) for campaign in AdvertisingCampaign.objects.all()
        )
        income_expenses_ratio: float = round(
            (total_income / total_expenses if total_income > 0 else 0), 2
        )

        context["potential_clients"] = potential_clients
        context["active_clients"] = active_clients
        context["income_expenses_ratio"] = income_expenses_ratio

        return context

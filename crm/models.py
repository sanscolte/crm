from django.db import models


class Service(models.Model):
    """Модель услуги"""

    name = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    cost = models.DecimalField(max_digits=100, decimal_places=2, verbose_name="стоимость")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class Campaign(models.Model):
    """Модель рекламной компании"""

    name = models.CharField(max_length=100, verbose_name="название")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="услуга")
    promotion_channel = models.CharField(max_length=100, verbose_name="канал продвижения")
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="бюджет")

    class Meta:
        verbose_name = "Рекламная компания"
        verbose_name_plural = "Рекламные компании"

    def __str__(self):
        return self.name


class PotentialClient(models.Model):
    """Модель потенциального клиента"""

    full_name = models.CharField(max_length=100, verbose_name="Ф.И.О")
    phone = models.CharField(max_length=11, verbose_name="телефон")
    email = models.EmailField(verbose_name="email")
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        verbose_name="рекламная кампания",
    )

    class Meta:
        verbose_name = "Потенциальный клиент"
        verbose_name_plural = "Потенциальные клиенты"

    def __str__(self):
        return self.full_name


class Contract(models.Model):
    """Модель контракта"""

    name = models.CharField(max_length=100, verbose_name="название")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="услуга")
    document = models.FileField(upload_to="documents/", verbose_name="документ")
    conclusion_date = models.DateField(verbose_name="дата заключения")
    validity_period = models.PositiveIntegerField(verbose_name="период действия")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="сумма")

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"

    def __str__(self):
        return self.name


class ActiveClient(models.Model):
    """Модель активного клиента"""

    potential_client = models.OneToOneField(
        PotentialClient, on_delete=models.CASCADE, verbose_name="потенциальный клиент"
    )
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, verbose_name="контракт")

    class Meta:
        verbose_name = "Активный клиент"
        verbose_name_plural = "Активные клиенты"

    def __str__(self):
        return self.potential_client.full_name

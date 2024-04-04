from django.db import models


class Service(models.Model):
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return self.name


class AdvertisingCampaign(models.Model):
    class Meta:
        verbose_name = 'Рекламная компания'
        verbose_name_plural = 'Рекламные компании'

    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    promotion_channel = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class PotentialClient(models.Model):
    class Meta:
        verbose_name = 'Потенциальный клиент'
        verbose_name_plural = 'Потенциальные клиенты'

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    advertising_campaign = models.ForeignKey(AdvertisingCampaign, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Contract(models.Model):
    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'

    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/')
    conclusion_date = models.DateField()
    validity_period = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class ActiveClient(models.Model):
    class Meta:
        verbose_name = 'Активный клиент'
        verbose_name_plural = 'Активные клиенты'

    potential_client = models.OneToOneField(PotentialClient, on_delete=models.CASCADE)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE)

    def __str__(self):
        return self.potential_client.full_name

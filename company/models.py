from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Company(models.Model):
    short_name = models.CharField("Кароткое название", max_length=16)
    name = models.CharField("Польное название", max_length=255, unique=True)
    inn = models.CharField("ИНН", max_length=12, )
    city = models.CharField("Город", max_length=100, null=True, blank=True)
    address = models.CharField("Адрес", max_length=255, null=True, blank=True)
    website = models.URLField("Веб-сайт", max_length=255, null=True, blank=True)
    email = models.EmailField("Почта", max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField("телефоный номер", blank=True)
    employees_count = models.PositiveIntegerField("Количество сотрудников", blank=True, default=0)
    industry = models.CharField("Отрасль", max_length=100, null=True, blank=True)
    description = models.TextField("Описание компании", null=True, blank=True)

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
        # permissions = (
        #     ("view_company", "Может просматривать компании"),
        #     ("add_company", "Может добавлять компании"),
        #     ("change_company", "Может изменять компании"),
        #     ("delete_company", "Может удалять компании"),
        # )
        permissions = (
            ("create_employee", "Может создавать сотрудников"),
        )

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField("Название площадки", max_length=100, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sites', verbose_name="Компания")
    city = models.CharField("Город", max_length=100, null=True, blank=True)
    address = models.CharField("Адрес", max_length=255, null=True, blank=True)
    email = models.EmailField("Почта", max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField("Телефоный номер", blank=True)
    employees_count = models.PositiveIntegerField("Количество сотрудников", blank=True, default=0)
    is_active = models.BooleanField("Активный", default=True)

    class Meta:
        verbose_name = "Площадка"
        verbose_name_plural = "Площадки"

    def __str__(self):
        return self.company.name + " - " + self.name


class Department(models.Model):
    short_name = models.CharField("Кароткое название", max_length=16, null=True, blank=True)
    name = models.CharField("Название", max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments', verbose_name="Компания")
    site = models.ForeignKey(Site,
                             on_delete=models.SET_NULL,
                             related_name='departments',
                             null=True, blank=True,
                             verbose_name="Площадка")
    employees_count = models.PositiveIntegerField('Количество сотрудников', default=0, null=True, blank=True)
    description = models.TextField('Описание', null=True, blank=True)

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField("Название", max_length=100)
    department = models.ForeignKey(Department,
                                   on_delete=models.CASCADE,
                                   related_name="positions",
                                   verbose_name="Департамент")

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return self.name

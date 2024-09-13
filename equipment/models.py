from django.db import models
from django.contrib.auth import get_user_model
from company.models import Department


ModelUser = get_user_model()


class Location(models.Model):
    title = models.CharField(max_length=255, verbose_name='Местоположение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

class Guarantee(models.Model):
    title = models.CharField(max_length=255, verbose_name='Гарантия')
    # file field for save document *.pdf, *.doc, *.docx
    file = models.FileField(upload_to='media/documents/', verbose_name='Файл')
    date_start = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата окончания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Гарантия'
        verbose_name_plural = 'Гарантии'

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория')
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='children',
                               verbose_name='Родительская категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Material(models.Model):

    title = models.CharField(max_length=255, verbose_name='Материал')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True,
                                 related_name='materials',
                                 verbose_name='Категория')
    unit = models.CharField(max_length=255,
                            verbose_name='Единица измерения'
                            )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class Equipment(models.Model):
    STATUS = (
        ('on_stock', 'На складе'),
        ('in_use', 'В эксплуатации'),
        ('in_repair', 'В ремонте'),
        ('returned', 'Списан')
    )
    material = models.ForeignKey(Material,
                                    on_delete=models.CASCADE,
                                    related_name='equipment',
                                    verbose_name='Материал')
    model_equipment = models.CharField(max_length=255,
                             verbose_name='Модель')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name='equipment',
                                 verbose_name='Местоположение', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='equipment',
                                   verbose_name='Отдел', null=True, blank=True)
    user  = models.ForeignKey(ModelUser, on_delete=models.SET_NULL, related_name='equipment',
                              verbose_name='Пользователь', null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS,
                              verbose_name='Статус')
    guarantee = models.ForeignKey(Guarantee,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  verbose_name='Гарантия')
    start_price = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                      verbose_name='Начальная стоимость', null=True, blank=True)
    date_start = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата окончания', null=True, blank=True)

    def __str__(self):
        return self.material.title + '- ЕО ' + str(self.pk)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'


class Consumable(models.Model):
    STATUS = (
        ('on_stock', 'На складе'),
        ('in_use', 'В эксплуатации'),
        ('returned', 'Списан')
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='consumable',
                                    verbose_name='Материал')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='consumables',
                                  verbose_name='Оборудование', null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS, verbose_name='Статус')


    def __str__(self):
        return self.material.title

    class Meta:
        verbose_name = 'Расходники'
        verbose_name_plural = 'Расходники'


class ProgramProduct(models.Model):
    STATUS = (
        ('on_stock', 'В наличии'),
        ('in_use', 'В эксплуатации'),
        ('returned', 'Лицензия закончилась'),
    )
    material = models.OneToOneField(Material, on_delete=models.CASCADE, related_name='program_product',
                                    verbose_name='Материал')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='program_products',
                                  verbose_name='Оборудование', null=True, blank=True)
    version = models.CharField(max_length=255, verbose_name='Версия')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    date_start = models.DateField(verbose_name='Дата начала Лицензии')
    date_end = models.DateField(verbose_name='Дата окончания Лицензии', null=True, blank=True)


    def __str__(self):
        return self.material.title

    class Meta:
        verbose_name = 'Программы'
        verbose_name_plural = 'Программы'


class Service(models.Model):
    material = models.OneToOneField(Material, on_delete=models.CASCADE, related_name='service',
                                    verbose_name='Материал')
    document_file = models.FileField(upload_to='media/services/documents/%Y/%m/%d/', verbose_name='Документ')

    def __str__(self):
        return self.material.title

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Order(models.Model):
    STATUS = (
        ('created', 'Создана'),
        ('accepted', 'на соглосовании'),
        ('rejected', 'Отклонена'),
        ('in_progress', 'В процессе'),
        ('delivered', 'Доставляется'),
        ('completed', 'Завершена'),
        ('canceled', 'Отменена'),
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='orders',
                                 verbose_name='Материал')
    status = models.CharField(max_length=255, choices=STATUS, default='created', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
    # user created field
    owner = models.ForeignKey(ModelUser, on_delete=models.SET_NULL, related_name='orders',
                              verbose_name="Заказчик", null=True, blank=True)

    def __str__(self):
        return self.material.title

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Warehouse(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

class WarehouseProduct(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouse_products',
                                  verbose_name='Склад')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='warehouse_products',
                                 verbose_name='Материал')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return self.material.title

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

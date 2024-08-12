from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('cancelled', 'Отменено'),
    ]

    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', null=True, blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    due_date = models.DateTimeField('Дедлайн', null=True, blank=True)
    assigned_to = models.ForeignKey(User,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    related_name='assigned_tasks',
                                    verbose_name='Ответственное лицо')
    initiated_by = models.ForeignKey(User,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True,
                                     related_name='initiated_tasks',
                                     verbose_name='Инициировал')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title




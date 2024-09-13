from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from company.models import Position
from .managers import PersonManager
from ad.models import Group


class Person(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    first_name = models.CharField(_("first name"), max_length=150, )
    last_name = models.CharField(_("last name"), max_length=150, )
    surname = models.CharField("Отчество", max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    phone_number = PhoneNumberField("Телефный номер", blank=True)
    birthday = models.DateField("День рождения", null=True, blank=True)
    position = models.ForeignKey(Position, models.SET_NULL, null=True, blank=True, verbose_name="Должность")
    ad_groups = models.ManyToManyField(Group, blank=True, related_name="persons", through='UserGroup', verbose_name="AD_Группы")
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = PersonManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


    def get_full_name(self):
        """
        Возвращает фамилии, имя и отчество с пробелом между ними
        """
        full_name = "%s %s %s" % (self.last_name, self.first_name, self.surname)
        return full_name.strip()


    def get_short_name(self):
        """Возвращает Фамилию и инициалы."""
        if self.surname:
            short_name = f"{self.last_name} {self.first_name[0]}. {self.surname[0]}."
        else:
            short_name = f"{self.last_name} {self.first_name[0]}."
        return short_name

    def has_group(self, group_name):
        if self.is_superuser:
            return True
        try:
            group = self.groups.get(name=group_name)
            return True
        except Group.DoesNotExist:
            return False

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Отправляет электронное письмо этому пользователю."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserGroup(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='user_groups')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='user_groups')

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"

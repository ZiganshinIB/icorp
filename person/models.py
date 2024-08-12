from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
# from company.models import Position
from .managers import PersonManager


class Person(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    # Имя пользователя в сиситемах
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

    # Имя
    first_name = models.CharField(_("first name"), max_length=150, )
    last_name = models.CharField(_("last name"), max_length=150, )
    # Отчество
    surname = models.CharField("Отчество", max_length=150, blank=True)
    # Почта
    email = models.EmailField(_("email address"), blank=True)
    # Телефон
    phone_number = PhoneNumberField("Телефный номер", blank=True)
    # День Рождение
    birthday = models.DateField("День рождения", null=True, blank=True)
    # !!!
    # position = models.ForeignKey(Position, models.SET_NULL, null=True, blank=True, verbose_name="Должность")
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


    def email_user(self, subject, message, from_email=None, **kwargs):
        """Отправляет электронное письмо этому пользователю."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

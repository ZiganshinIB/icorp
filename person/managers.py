from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from transliterate import translit


class PersonManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, first_name, last_name, password=None, **extra_fields):
        if not first_name:
            raise ValueError(_('The first name must be set'))
        if not last_name:
            raise ValueError(_('The last name must be set'))
        first_name = self.model.normalize_username(first_name)
        last_name = self.model.normalize_username(last_name)
        if extra_fields.get('username', None) is None:
            username = f"{translit(first_name, 'ru', reversed=True)}.{translit(last_name, 'ru', reversed=True)}".strip('`').lower()
            if self.filter(username=username).exists():
                username = f"{username}{self.count()}"
        else:
            username = extra_fields.get('username')
            extra_fields.pop('username')
        if extra_fields.get('email', None) is None:
            email = f'{username}@test.ru'
        else:
            email = extra_fields.get('email')
            extra_fields.pop('email')
        person = self.model(username=username, first_name=first_name, last_name=last_name, email=email, **extra_fields)
        person.set_password(password)
        person.save(using=self._db)
        return person

    def create_superuser(self, username, first_name, last_name, password, **extra_fields):
        print("Start create_superuser")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(first_name, last_name, password, **extra_fields)

    def with_perm(
            self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()
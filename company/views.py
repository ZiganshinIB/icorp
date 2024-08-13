from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .forms import CreateEmployeeForm
from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from transliterate import translit

User = get_user_model()


@permission_required('company.create_employee', raise_exception=True)
@login_required
def create_employee(request):
    if request.method == 'POST':
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            cd = form.save(commit=False)
            # Костыл для тестирования Стандартный пароль
            person = User.objects.create_user(
                first_name=cd.first_name,
                last_name=cd.last_name,
                surname=cd.surname,
                password='QWEuio!@#098',
                phone_number=cd.phone_number,
                birthday=cd.birthday,
                position=cd.position,
                date_joined=cd.date_joined,
                is_active=False,
            )

            return render(request, 'company/employee/create.html')
    else:
        form = CreateEmployeeForm()
    return render(request, 'company/employee/create.html', {'form': form})

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .forms import CreateEmployeeForm

User = get_user_model()


@permission_required('company.create_employee', raise_exception=True)
@login_required
def create_employee(request):
    if request.method == 'POST':
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Костыл для тестирования Стандартный пароль
            user.set_password('QWEuio!@#098')
            user.is_active = False
            user.save()
            return render(request, 'company/employee/create.html')
    else:
        form = CreateEmployeeForm()
    return render(request, 'company/employee/create.html', {'form': form})

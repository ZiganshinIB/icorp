from django import forms
from django.contrib.auth import get_user_model
from phonenumber_field import validators
from .models import Company, Position, Department, Site


User = get_user_model()


class CreateEmployeeForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), label='Компания')
    site = forms.ModelChoiceField(queryset=Site.objects.none(), label='Площадка')
    department = forms.ModelChoiceField(queryset=Department.objects.none(), label='Отдел')
    position = forms.ModelChoiceField(queryset=Position.objects.none(), label='Должность')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'surname', 'phone_number', 'birthday', 'date_joined', 'company', 'site',
                  'department', 'position']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['site'].queryset = Site.objects.filter(company_id=company_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['site'].queryset = self.instance.company.sites.order_by('name')
        if 'site' in self.data:
            try:
                site_id = int(self.data.get('site'))
                self.fields['department'].queryset = Department.objects.filter(site_id=site_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.site.departments.order_by('name')
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['position'] = Position.objects.filter(department_id=department_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['position'].queryset = self.instance.department.positions.order_by('name')



    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Такой номер телефона уже существует')
        if not validators.validate_international_phonenumber(phone_number):
            raise forms.ValidationError('Телефон должен быть в формате +7XXXXXXXXXX')
        return phone_number


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'


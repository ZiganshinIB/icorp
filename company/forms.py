from django import forms

from .models import Company, Position, Department, Site


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


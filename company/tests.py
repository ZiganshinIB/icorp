from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Permission, Group
from .models import Company, Position, Department, Site
from .forms import CreateEmployeeForm
from django.urls import reverse

User = get_user_model()


class CreateEmployeeViewTests(TestCase):

    def setUp(self):
        self.user_with_permission = User.objects.create_user(first_name='Босс', last_name='Тестов', password='testpass')
        self.user_without_permission = User.objects.create_user(first_name='Тест', last_name='Тестов', password='testpass')
        group = Group.objects.create(name='testgroup')
        group.permissions.add(Permission.objects.get(codename='create_employee'))
        self.user_with_permission.groups.add(group)

        self.company1 = Company.objects.create(
            short_name='Comp1',
            name='Company One',
            inn='123456789012',
            city='City A',
            address='Address 1',
            website='http://companyone.com',
            email='contact@companyone.com',
            phone_number='89883332211',
            employees_count=10,
            industry='Industry A',
        )
        self.site1 = Site.objects.create(
            name='Site One',
            company=self.company1
        )

        self.department1 = Department.objects.create(
            name='Department One',
            site=self.site1,
            company=self.company1
        )
        self.position1 = Position.objects.create(
            name='Position One',
            department=self.department1
        )

        self.create_employ_url = reverse('company:create_employee')
        self.login_url = reverse('login')

    def authenticate(self, user):
        self.client.login(username=user.username, password='testpass')

    def test_create_employee_view(self):
        self.authenticate(self.user_with_permission)
        response = self.client.get(self.create_employ_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        form_data = {
            'first_name': 'Алун',
            'last_name': 'Дон',
            'surname': 'Донченко',
            'birthday': '12.08.2024',
            'date_joined': '12.08.2024',
            'company': self.company1.pk,
            'site': self.site1.pk,
            'department': self.department1.pk,
            'position': self.position1.pk,
        }
        form = CreateEmployeeForm(form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
        user = form.save(commit=False)
        user.set_password('QWEuio!@#098')
        user.save()

        self.assertTrue(User.objects.filter(first_name='Алун').exists())

    def test_create_employee_view_without_permission(self):
        self.authenticate(self.user_without_permission)
        response = self.client.get(self.create_employ_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



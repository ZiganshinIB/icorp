from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from company.models import Company, Site, Position, Department


User = get_user_model()


class DepartmentAPITestCase(APITestCase):
    def setUp(self):
        self.user_with_permission = User.objects.create_user(first_name='Босс', last_name='Тестов', password='testpass')
        self.user_without_permission = User.objects.create_user(first_name='Тест', last_name='Тестов', password='testpass')
        group = Group.objects.create(name='testgroup')
        group.permissions.add(Permission.objects.get(codename='add_department'))
        group.permissions.add(Permission.objects.get(codename='change_department'))
        group.permissions.add(Permission.objects.get(codename='delete_department'))
        self.user_with_permission.groups.add(group)
        self.company1 = Company.objects.create(
            short_name='Comp1',
            name='Company One',
            inn='123456789012',
            city='City A',
            address='Address 1',
            website='http://companyone.com',
            email='contact@companyone.com',
            employees_count=10,
            industry='Industry A',)
        self.company2 = Company.objects.create(
            short_name='Comp2',
            name='Company Two',
            inn='987654321098',
        )
        self.site1 = Site.objects.create(
            name='Site One',
            company=self.company2
        )
        self.department1 = Department.objects.create(
            name='Department One',
            company=self.company1
        )
        self.department2 = Department.objects.create(
            name='Department Two',
            company=self.company2,
            site=self.site1
        )

        self.login_url = reverse('login')
        self.department_CR_url = reverse('department-list')
        self.department_UD_url = lambda pk: reverse('department-detail', kwargs={'pk': pk})

    def authenticate(self, user):
        response = self.client.post(self.login_url, {'username': user.username, 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_get_departments_with_permission(self):
        self.authenticate(self.user_with_permission)
        response = self.client.get(reverse('department-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_departments_without_permission(self):
        self.authenticate(self.user_without_permission)
        response = self.client.get(reverse('department-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_department_with_permission(self):
        self.authenticate(self.user_with_permission)
        data = {
            'name': 'Department Three',
            'company': self.company1.pk
        }
        response = self.client.post(self.department_CR_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 3)

    def test_create_department_without_permission(self):
        self.authenticate(self.user_without_permission)
        data = {
            'name': 'Department Three',
            'company': self.company1.pk
        }
        response = self.client.post(self.department_CR_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Department.objects.count(), 2)

    def test_update_department_with_permission(self):
        self.authenticate(self.user_with_permission)
        data = {
            'name': 'Department Three',
            'company': self.company1.pk
        }
        response = self.client.put(self.department_UD_url(self.department1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Department.objects.get(pk=self.department1.pk).name, 'Department Three')
        self.assertEqual(Department.objects.count(), 2)

    def test_update_department_without_permission(self):
        self.authenticate(self.user_without_permission)
        data = {
            'name': 'Department Three',
            'company': self.company1.pk
        }
        response = self.client.put(self.department_UD_url(self.department1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Department.objects.count(), 2)

    def test_delete_department_with_permission(self):
        self.authenticate(self.user_with_permission)
        response = self.client.delete(self.department_UD_url(self.department1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Department.objects.count(), 1)

    def test_delete_department_without_permission(self):
        self.authenticate(self.user_without_permission)
        response = self.client.delete(self.department_UD_url(self.department1.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Department.objects.count(), 2)


class SiteAPITestCase(APITestCase):
    def setUp(self):

        self.user_with_permission = User.objects.create_user(first_name='Босс', last_name='Тестов', password='testpass')
        self.user_without_permission = User.objects.create_user(first_name='Тест', last_name='Тестов', password='testpass')
        group = Group.objects.create(name='testgroup')
        group.permissions.add(Permission.objects.get(codename='add_site'))
        group.permissions.add(Permission.objects.get(codename='change_site'))
        group.permissions.add(Permission.objects.get(codename='delete_site'))
        self.user_with_permission.groups.add(group)
        self.company1 = Company.objects.create(
            short_name='Comp1',
            name='Company One',
            inn='123456789012',
            city='City A',
            address='Address 1',
            website='http://companyone.com',
            email='contact@companyone.com',
            phone_number='+1234567890',
            employees_count=10,
            industry='Industry A',
            description='Description of Company One'
        )
        self.site1 = Site.objects.create(
            name='Site One',
            company=self.company1
        )
        self.site2 = Site.objects.create(
            name='Site Two',
            company=self.company1
        )
        self.site3 = Site.objects.create(
            name='Site Three',
            company=self.company1
        )
        self.site_CR_url = reverse('site-list')
        self.site_UD_url = lambda pk: reverse('site-detail', args=[pk])
        self.login_url = reverse('login')

    def authenticate(self, user):
        response = self.client.post(self.login_url, {'username': user.username, 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_get_site_with_permission_list(self):
        """ Тест получения списка площадки """
        self.authenticate(self.user_with_permission)
        response = self.client.get(self.site_CR_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], self.site1.name)
        self.assertEqual(response.data[1]['name'], self.site2.name)
        self.assertEqual(response.data[2]['name'], self.site3.name)

    def test_get_site_without_permission_list(self):
        """ Тест получения списка площадки """
        self.authenticate(self.user_without_permission)
        response = self.client.get(self.site_CR_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], self.site1.name)
        self.assertEqual(response.data[1]['name'], self.site2.name)
        self.assertEqual(response.data[2]['name'], self.site3.name)

    def test_update_site_with_permission(self):
        """ Тест обновления площадки """
        self.authenticate(self.user_with_permission)
        data = {
            'name': 'Updated Site One',
            'company': self.company1.pk
        }
        response = self.client.put(self.site_UD_url(self.site1.pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.site1.refresh_from_db()
        self.assertEqual(self.site1.name, 'Updated Site One')

    def test_update_site_without_permission(self):
        """ Тест обновления площадки """
        self.authenticate(self.user_without_permission)
        data = {
            'name': 'Updated Site One',
            'company': self.company1.pk
        }
        response = self.client.put(self.site_UD_url(self.site1.pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_site_with_permission(self):
        """ Тест создания площадки """
        self.authenticate(self.user_with_permission)
        data = {
            'name': 'New Site',
            'company': self.company1.pk
        }
        response = self.client.post(self.site_CR_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Site.objects.count(), 4)

    def test_create_site_without_permission(self):
        """ Тест создания площадки """
        self.authenticate(self.user_without_permission)
        data = {
            'name': 'New Site',
            'company': self.company1.pk
        }
        response = self.client.post(self.site_CR_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_site(self):
        """ Тест удаления площадки """
        self.authenticate(self.user_with_permission)
        response = self.client.delete(self.site_UD_url(self.site1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Site.objects.count(), 2)

    def test_delete_site_without_permission(self):
        """ Тест удаления площадки """
        self.authenticate(self.user_without_permission)
        response = self.client.delete(self.site_UD_url(self.site1.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access(self):
        response = self.client.get(self.site_CR_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CompanyAPITestCase(APITestCase):
    def setUp(self):
        self.user_with_permission = User.objects.create_user(first_name='Босс', last_name='Тестов', password='testpass')
        self.user_without_permission = User.objects.create_user(first_name='Тест', last_name='Тестов',
                                                                password='testpass')
        group = Group.objects.create(name='testgroup')
        group.permissions.add(Permission.objects.get(codename='add_company'))
        group.permissions.add(Permission.objects.get(codename='change_company'))
        group.permissions.add(Permission.objects.get(codename='delete_company'))
        self.user_with_permission.groups.add(group)
        self.company1 = Company.objects.create(
            short_name='Comp1',
            name='Company One',
            inn='123456789012',
            city='City A',
            address='Address 1',
            website='http://companyone.com',
            email='contact@companyone.com',
            phone_number='+1234567890',
            employees_count=10,
            industry='Industry A',
            description='Description of Company One'
        )
        self.company2 = Company.objects.create(
            short_name='Comp2',
            name='Company Two',
            inn='987654321098',
            city='City B',
            address='Address 2',
            website='http://companytwo.com',
            email='contact@companytwo.com',
            phone_number='+0987654321',
            employees_count=20,
            industry='Industry B',
            description='Description of Company Two'
        )
        self.company_CR_url = reverse('company-list')
        self.company_UD_url = lambda pk: reverse('company-detail', kwargs={'pk': pk})
        self.token_url = reverse('login')  # URL для создания токена

    def test_create_token(self):
        username = self.user_with_permission.username
        response = self.client.post(self.token_url, {'username': username, 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)  # Проверяем, что токен возвращается

    def authenticate(self, user):
        response = self.client.post(self.token_url, {'username': user.username, 'password': 'testpass'})
        token = response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_create_company_with_permission(self):
        """Тест создания компании"""
        self.authenticate(self.user_with_permission)
        data = {
            'short_name': 'Comp3',
            'name': 'Company Three',
            'inn': '123456789012',
            'city': 'City C',
        }
        response = self.client.post(self.company_CR_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 3)

    def test_create_company_without_permission(self):
        """Тест создания компании"""
        self.authenticate(self.user_without_permission)
        data = {
            'short_name': 'Comp3',
            'name': 'Company Three',
            'inn': '123456789012',
            'city': 'City C',
        }
        response = self.client.post(self.company_CR_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_company_with_permission(self):
        """ Тест обновления компании """
        self.authenticate(self.user_with_permission)
        data = {
            'short_name': 'UpdatedComp1',
            'name': 'Updated Company One',
            'inn': '123456789012',
            'city': 'Updated City A',
            'address': 'Updated Address 1',
            'website': 'http://updatedcompanyone.com',
            'email': 'contact@updatedcompanyone.com',
            'phone_number': '89353332211',
            'employees_count': 12,
            'industry': 'Updated Industry A',
            'description': 'Updated Description of Company One'
        }
        response = self.client.put(self.company_UD_url(self.company1.pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company1.refresh_from_db()
        self.assertEqual(self.company1.name, 'Updated Company One')

    def test_update_company_without_permission(self):
        """ Тест обновления компании """
        self.authenticate(self.user_without_permission)
        data = {
            'short_name': 'UpdatedComp1',
            'name': 'Updated Company One',
            'inn': '123456789012',
            'city': 'Updated City A',
            'address': 'Updated Address 1',
            'website': 'http://updatedcompanyone.com',
            'email': 'contact@updatedcompanyone.com',
            'phone_number': '89353332211',
            'employees_count': 12,
            'industry': 'Updated Industry A',
            'description': 'Updated Description of Company One'
        }
        response = self.client.put(self.company_UD_url(self.company1.pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_company_with_permission(self):
        """ Тест удаления компании """
        self.authenticate(self.user_with_permission)
        response = self.client.delete(self.company_UD_url(self.company1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 1)

    def test_delete_company_without_permission(self):
        """ Тест удаления компании """
        self.authenticate(self.user_without_permission)
        response = self.client.delete(self.company_UD_url(self.company1.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_company_list_with_token(self):
        """ Тест получения списка компаний с токеном """
        self.authenticate(self.user_with_permission)
        response = self.client.get(self.company_CR_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.company1.name)
        self.assertEqual(response.data[1]['name'], self.company2.name)

    def test_unauthenticated_access(self):
        response = self.client.get(self.company_CR_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





from rest_framework import status
from django.core.urlresolvers import reverse

from core.tests.utils import FixtureTestCase


class DatabaseAPIListTestCase(FixtureTestCase):
    view_name = 'api-databases-list'

    def test_guest(self):
        url = reverse(self.view_name)

        self.client.logout()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # POST
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PATCH
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_databases(self):
        url = reverse(self.view_name)

        self.login_superuser()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # POST
        new_data = {'name': 'this is a name'}

        response = self.client.post(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.data
        del (response_data['id'])

        self.assertEqual(response_data, new_data)

        # PUT
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # PATCH
        updated_field = {'name': 'a new name'}

        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_databases(self):
        url = reverse(self.view_name)

        self.login_staff_2()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # POST
        new_data = {'name': 'this is a name'}

        response = self.client.post(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.data
        del (response_data['id'])

        self.assertEqual(response_data, new_data)

        # PUT
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PATCH
        updated_field = {'name': 'a new name'}

        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DatabaseAPIDetailTestCase(FixtureTestCase):
    view_name = 'api-databases-detail'

    def test_guest(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.database_1_data['id']})

        self.logout()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # POST
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PATCH
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_databases(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.database_1_data['id']})

        self.login_superuser()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.database_1_data)

        # POST
        updated_field = {'name': 'a new name'}

        new_data = self.database_1_data.copy()
        new_data.update(updated_field)

        response = self.client.post(url, updated_field, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # PATCH
        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, new_data)

        # PUT
        new_data = {'name': 'another name'}

        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_data['id'] = self.database_1_data['id']
        self.assertEqual(response.data, new_data)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_databases(self):
        url = reverse(self.view_name,
                      kwargs={'pk': self.database_1_data['id']})

        self.login_staff_2()

        # GET
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.database_1_data)

        # POST
        updated_field = {'name': 'a new name'}

        new_data = self.database_1_data.copy()
        new_data.update(updated_field)

        response = self.client.post(url, updated_field, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # PATCH
        response = self.client.patch(url, updated_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT
        new_data = {'name': 'another name'}

        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # OPTIONS
        response = self.client.options(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

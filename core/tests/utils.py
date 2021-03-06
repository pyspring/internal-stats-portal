from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import DataSource, Database, Tag, Publication


class FixtureTestCase(APITestCase):
    fixtures = ('initial_data.json',)

    datasource_1_data = {'id': 5, 'notes': 'Datasource 1'}
    database_1_data = {'id': 4, 'name': 'Database 1'}
    tag_1_data = {'id': 7, 'name': 'Tag 1'}
    publication_1_data = {'id': 15, 'name': 'staff_1_publication',
                          'description': '', 'programming_language': None,
                          'update_value': None, 'update_type': None,
                          'creator': 18, 'server_path': '',
                          'file_path': '/home/staff_1', 'publishable': False,
                          'created': '2016-11-07T21:52:58Z',
                          'modified': '2016-11-07T21:53:00Z',
                          'data_sources': [], 'responsibles': [18],
                          'databases': [], 'tags': [8]}

    @classmethod
    def setUpTestData(cls):
        # Staff group creation
        staff_group = Group.objects.create(name='staff')
        # Add datasource permission
        ct = ContentType.objects.get_for_model(DataSource)
        permission = Permission.objects.get(codename='add_datasource',
                                            content_type=ct)
        staff_group.permissions.add(permission)
        # Add database permission
        ct = ContentType.objects.get_for_model(Database)
        permission = Permission.objects.get(codename='add_database',
                                            content_type=ct)
        staff_group.permissions.add(permission)
        # Add tag permission
        ct = ContentType.objects.get_for_model(Tag)
        permission = Permission.objects.get(codename='add_tag',
                                            content_type=ct)
        staff_group.permissions.add(permission)
        # Add/edit/delete publication permission
        ct = ContentType.objects.get_for_model(Publication)
        permission = Permission.objects.filter(content_type=ct)
        staff_group.permissions.add(*permission)

        # Add staff users to staff_group
        UserModel = get_user_model()
        staff_1 = UserModel.objects.get(username='staff_1')
        staff_2 = UserModel.objects.get(username='staff_2')
        staff_group.user_set.add(staff_1, staff_2)

    def login_superuser(self):
        self.login('superuser', 'super')

    def login_staff_1(self):
        self.login('staff_1', 'staff')

    def login_staff_2(self):
        self.login('staff_2', 'staff')

    def login(self, username, password):
        self.assertTrue(
            self.client.login(username=username, password=password)
        )

    def logout(self):
        self.client.logout()

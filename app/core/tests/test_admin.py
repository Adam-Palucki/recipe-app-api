from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):  # this method will run before every test
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
        email = 'admin@drawnet.pl',
        password = 'password123'
        )
        self.client.force_login(self.admin_user)

        # test user for making tests
        self.user = get_user_model().objects.create_user(
        email = 'test@drawnet.pl',
        password = 'password123',
        name = 'Test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # core_user_changelist in the django admin documentation
        # this is some way to not making many changes just one
        # it generates url for user list page
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)  # response

        self.assertContains(res, self.user.name)  # assertContains checks if:
            # res contains item sels.user.name
            # and makes other check like if http response is 200 OK
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args = [self.user.id])
        # /admin/core/User/1 <- the number is 'id' of the user
        res = self.client.get(url)  # response

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test thst create user works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)  # response

        self.assertEqual(res.status_code, 200)

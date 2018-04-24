import io
import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import datetime as dt

from django.test.client import Client
from django.urls.base import reverse

from .models import Slip
from sliply_project.celery import app
from sliply_project.settings import BASE_DIR, MEDIA_ROOT


class SliplyModelViewTest(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def _create_user(self):
        return get_user_model().objects.create_user(
            username='sliper',
            email='myslips@sliply.io',
            first_name='S',
            last_name='Liper',
            is_active=True,
        )

    def _set_passwd_user(self):
        test_user = self._create_user()
        test_user.set_password('test')
        test_user.save()
        return test_user

    def _login_user(self):
        test_user = self._set_passwd_user()
        user_login = self.client.login(username=test_user.username, password='test')
        return user_login

    def _create_slip(self):
        self._login_user()
        test_slip = self.client.post(reverse('slip_create'), {
            'seller_name': 'Biedronka',
            'purchase_date':'2018-04-20',
            'total_amount': 10.0,
            'payment_type': 2
        })
        return test_slip

    def _file_upload(self, *args):
        file_path = os.path.join(os.path.join(BASE_DIR, 'sliply/test_image/'), 'test.jpg')
        self.assertTrue(os.path.exists(file_path))
        self._login_user()
        with io.open(file_path, 'rb') as scanfile:
            self.client.post(reverse('upload'), {'scanfile': scanfile})

    def test_no_login_redirect(self):
        response = self.client.get(reverse('slips'))
        self.assertEqual(response.status_code, 302)

    def test_user_create(self):
        self._create_user()
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_user_login(self):
        test_user = self._set_passwd_user()
        user_login = self.client.login(username=test_user.username, password='test')
        self.assertTrue(user_login)

    def test_login_user_view(self):
        test_user = self._set_passwd_user()
        self.client.login(username=test_user.username, password='test')
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_slip_create(self):
        self._create_slip()
        get_user_slip = Slip.objects.filter(owner__username='sliper')
        self.assertEqual(get_user_slip.count(), 1)
        self.assertEqual(get_user_slip[0].create_date.date(), dt.now().date())

    def test_slip_listview(self):
        self._create_slip()
        response = self.client.get(reverse('slips'))
        context_data = response.context['object_list'][0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(context_data.create_date.date(), dt.now().date())
        self.assertEqual(context_data.seller_name, "Biedronka")

    def test_if_image_uploaded(self):
        if app.control.inspect().active():
            self._file_upload()
            self.assertTrue(os.path.exists(os.path.join(MEDIA_ROOT, 'test.jpg')))
        else:
            raise Exception('This test requires Celery worker to be activated')


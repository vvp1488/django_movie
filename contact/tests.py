from django.test import TestCase, override_settings, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .models import Contact
from django.contrib.auth.models import User
from movies.models import Category, Actor
from .tasks import send_spam_email
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver


class ContactTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = Contact.objects.create(email='vitaliikondratiev@ukr.net')
        cls.category = Category.objects.create(name='movie', description='some movie')
        cls.actor = Actor.objects.create(name='Jeson', age=40, description='some des', image=' ')
        cls.c = Client()

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_contact(self):
        self.assertEqual(self.user.email, 'vitaliikondratiev@ukr.net')
        self.assertTrue(send_spam_email.delay('vitaliikondratiev@ukr.net'))

    def test_page_category(self):
        response = self.c.get(f'/ru/category/{self.category.name}/')
        self.assertEqual(response.status_code, 200)

    def test_permissions(self):
        current_user = User.objects.create(username='admin', password='admin')
        current_user.set_password('admin')
        current_user.save()
        response = self.c.get(f'/ru/actor/{self.actor.name}/')
        self.assertEqual(response.status_code, 302)

        self.c.login(username='admin', password='admin')
        response = self.c.get(f'/ru/actor/{self.actor.name}/')
        self.assertEqual(response.status_code, 200)


class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox(executable_path='/home/vitalii/DjangoProjects/geckodriver.exe')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('http://127.0.0.1:8000/ru/accounts/login/')
        username_input = self.selenium.find_element(value='id_login')
        username_input.send_keys('admin')
        password_input = self.selenium.find_element(value='id_password')
        password_input.send_keys('123456')
        self.selenium.find_element(value='Log in').click()





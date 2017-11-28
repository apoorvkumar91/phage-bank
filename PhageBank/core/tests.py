from django.test import TestCase
import unittest,os,shutil
from django.test import Client
from django.contrib.auth.models import User
from django.views.generic.base import View
from PhageBank.core.views import *
import tempfile
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import User
from PhageBank.core.models import PhageData, PreData
from PhageBank.core.forms import Add_ResearchForm, AForm, AIForm, Edit_Phage_DataForm, Edit_ResearcherForm, Edit_ResearchForm, Edit_IsolationDataForm, Edit_Experiment_Form

from faker import Faker
fake = Faker()

username=fake.word()
class URLGETTest(unittest.TestCase):
    client = Client()

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_home_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_contact_url(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_view_phages_url(self):
        response = self.client.get('/view_phages/')
        self.assertEqual(response.status_code, 200)

    def test_search_phage_url(self):
        response = self.client.get('/search_phage/')
        self.assertEqual(response.status_code, 200)

    def test_uploads_url(self):
        response = self.client.get('/uploads/form/')
        self.assertEqual(response.status_code, 302)

    def test_edit_details_url(self):
        response = self.client.get('/edit_details/')
        self.assertEqual(response.status_code, 302)

    def test_change_password_url(self):
        response = self.client.get('/change_password/')
        self.assertEqual(response.status_code, 302)

    def test_logout_url(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)

    def test_signup_url(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_mylogin_url(self):
        response = self.client.get('/mylogin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_url(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

    def test_addphage_url(self):
        response = self.client.get('/add_phage/')
        self.assertEqual(response.status_code, 302)

    def test_deleteall_url(self):
        response = self.client.get('/delete_all/')
        self.assertEqual(response.status_code, 302)

    def test_delete_url(self):
        response = self.client.get('/delete/')
        self.assertEqual(response.status_code, 302)

    def test_my_phages_url(self):
        response = self.client.get('/my_phages/')
        self.assertEqual(response.status_code, 200)


class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = SignUpForm(data={'username': 'foo',
                                'email': 'alice@example.com',
                                'password1': 'foo',
                                'password2': 'foo'})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['email'],
                         [u"This email address is already in use. Please supply a different email address."])

        form = forms.SignUpForm(data={'username': 'foo',
                                      'email': 'foo@example.com',
                                      'password1': 'foo',
                                      'password2': 'foo'})
        self.failUnless(form.is_valid())

    def test_validates_password(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        data = {
            'old_password': 'sekret',
            'new_password1': 'testclient',
            'new_password2': 'testclient2',
        }
        self.client.login(username='testclient', password='sekret')
        response = self.client.post('/change_password', data, follow=True)
        # form = PasswordChangeForm(user, data)
        # self.assertFalse(form.is_valid())
        # self.assertEqual(len(form["new_password2"].errors), 1)
        # self.assertEqual(response.status_code, 302)
        index = response.content.find(b"The two password fields didn\'t match.")
        user.delete()
        self.assertEqual(index,-1)

    def test_validates_password_success(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        data = {
            'old_password': 'sekret',
            'new_password1': 'testclient',
            'new_password2': 'testclient',
        }
        self.client.login(username='testclient', password='sekret')
        response = self.client.post('/change_password', data, follow=True)
        form = PasswordChangeForm(user, data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form["new_password2"].errors), 0)
        user.delete()

    # def testagain(self):
    #     c = Client()
    #     with open("" as fp)
    #         c.post()


class PhageViewTest(TestCase):

    def test_count(self):
        path = 'test1'
        os.mkdir(path)
        filename1 = '1' + '.jpg'
        f1 = open(os.path.join(path, filename1), 'wb')
        f1.close()

        filename2 = '2' + '.jpg'
        f2 = open(os.path.join(path, filename2), 'wb')
        f2.close()

        dir_name = os.path.join(os.curdir, path)
        val = count(dir_name)
        self.assertEqual(val, 2)
        shutil.rmtree(path)

    def test_list_path(self):
        path = "test2"
        os.mkdir(path)
        filename1 = '1' + '.jpg'
        f1 = open(os.path.join(path, filename1), 'wb')
        f1.close()
        val = list_path(path)
        self.assertEqual('1.jpg', str(val[0]))
        shutil.rmtree(path)


class ModelTest(TestCase):

    def test_validate_latest(self):
        phage = PhageData.objects.create(phage_name='TestPhage', phage_CPT_id='123456')
        phage.save()
        q = PhageData.objects.all()
        val = validate_latest_phage(q)
        self.assertEqual(val, phage.phage_name)
        phage.delete()

    # def test_my_phages(self):
    #     user = User.objects.create_user(username='testclient', password='sekret')
    #     phage = PhageData.objects.create(phage_name='TestPhage', phage_CPT_id='123456',phage_submitted_user='testclient')
    #     phage.save()
    #     self.client.login(username='testclient', password='sekret')
    #     response = self.client.get('/my_phages')
    #     # q = PhageData.objects.filter(phage_submitted_user=user.username)
    #     # val = validate_latest_phage(q)
    #     # self.assertEqual(q, phage)
    #     # self.assertTrue(form.is_valid())
    #     self.assertEqual(response.status_code, 301)
    #     user.delete()
    #     phage.delete()

    def test_isodata(self):
        isoform = Isolation_Form.objects.create(owner_name='testowner', location='testloc')


    def test_count(self):
        p1= PhageData.objects.create(phage_name='test',phage_CPT_id='123')
        p2 = PhageData.objects.create(phage_name='test123',phage_CPT_id='12345')
        p3 = PreData.objects.create(phagename='test12', testkey=p1)
        name='manish'
        val = check_entry(name)
        self.assertEqual(val, False)

        name='test'
        val2 = check_entry(name)
        self.assertEqual(val2, True)
        p1.delete()
        p2.delete()
        p3.delete()

    # def test_delete(self):
    #     user = User.objects.create_user(username='testclient', password='sekret')
    #     p1= PhageData.objects.create(phage_name='test22',phage_CPT_id='123')
    #     dest_dir = os.path.join(settings.MEDIA_ROOT, "images", p1.phage_name)
    #     docs_dest_dir = os.path.join(settings.MEDIA_ROOT, "docs", p1.phage_name)
    #     os.mkdir(dest_dir)
    #     os.mkdir(docs_dest_dir)
    #     self.client.login(username='testclient', password='sekret')
    #     data = {"name":"test22"}
    #     response = self.client.post('/delete/',str(data), follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     user.delete()
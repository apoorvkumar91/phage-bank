from django.test import TestCase
import unittest,os,shutil
from django.test import Client
from PhageBank.core.views import *
from PhageBank.core.forms import *
from faker import Faker
fake = Faker()

username = fake.word()
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
            'new_password2': 'testclient',
        }
        form = PasswordChangeForm(user, data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form["new_password2"].errors), 1)


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

    def test_file_extension(self):
        filename1 = '1' + '.jpg'
        f1 = open(filename1, 'wb')
        f1.close()

        print (validate_file_extension(filename1))
        os.remove(filename1)

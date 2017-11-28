from django.test import TestCase
import unittest,os,shutil
from django.test import Client
from PhageBank.core.views import *
from PhageBank.core.forms import *
from faker import Faker
fake = Faker()

username = fake.word()

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
        shutil.rmtree(filename1)

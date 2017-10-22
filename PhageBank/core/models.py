from __future__ import unicode_literals

from django.db import models

class PhageData(models.Model):
    phage_first_name = models.CharField(max_length=30)
    phage_second_name =  models.CharField(max_length=30, default='SOME STRING')
    # phage_host_id = models.IntegerField()
    # phage_CPT_id = models.CharField(max_length=100)
    # phage_isolator_loc = models.CharField(max_length=5000)
    # phage_experimenter_id = models.IntegerField()
    # phage_isolator_id = models.IntegerField()


class PeopleData(models.Model):
    people_first_name = models.CharField(max_length=30)
    people_second_name =  models.CharField(max_length=30)
    # phage_name = models.CharField(max_length=30)
    # phage_host_id = models.IntegerField()
    # phage_CPT_id = models.CharField(max_length=100)
    # phage_isolator_loc = models.CharField(max_length=5000)
    # phage_experimenter_id = models.IntegerField()
    # phage_isolator_id = models.IntegerField()

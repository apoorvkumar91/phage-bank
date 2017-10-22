from __future__ import unicode_literals

from django.db import models

class PhageData(models.Model):
    phage_name = models.CharField(max_length=30)
    phage_host_id = models.IntegerField()
    phage_CPT_id = models.CharField(max_length=100)
    phage_isolator_loc = models.CharField(max_length=5000)
    phage_experimenter_id = models.IntegerField()
    phage_isolator_id = models.IntegerField()

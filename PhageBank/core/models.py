from __future__ import unicode_literals

from django.db import models


class PhageData(models.Model):
    phage_name = models.CharField(max_length=30, default='none')
    phage_host_name = models.CharField(max_length=30, default='none')
    phage_isolator_name = models.CharField(max_length=30, default='none')
    phage_experimenter_name = models.CharField(max_length=30, default='none')
    phage_CPT_id = models.CharField(max_length=100, default='none')
    phage_isolator_loc = models.CharField(max_length=5000, default='none')

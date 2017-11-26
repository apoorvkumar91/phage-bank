import django_filters
from django import forms
from django.contrib.auth.models import User
from PhageBank.core.models import PhageData, ExperimentData, IsolationData


class PhageFilter(django_filters.FilterSet):
    phage_name = django_filters.CharFilter(lookup_expr='icontains')
    submitted_year = django_filters.NumberFilter(name='phage_submitted_date', lookup_expr='year')
    submitted_year__lt = django_filters.NumberFilter(name='phage_submitted_date', lookup_expr='year__lt')
    submitted_year__gt = django_filters.NumberFilter(name='phage_submitted_date', lookup_expr='year__gt')
    #phage_lab = django_filters.ModelMultipleChoiceFilter(queryset=PhageData.objects.values('phage_lab').distinct(),
    #                                                  widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = PhageData
        fields = ['phage_name',
                  'phage_host_name',
                  'phage_isolator_name',
                  'phage_experimenter_name',
                  'phage_CPT_id',
                  'phage_isolator_loc', 'phage_submitted_user', 'phage_submitted_date', 'phage_lab']
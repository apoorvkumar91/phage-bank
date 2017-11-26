import django_filters
from django import forms
from django.db import models
from django.contrib.auth.models import User
from datetimewidget.widgets import DateTimeWidget, DateWidget
from PhageBank.core.models import PhageData, ExperimentData, IsolationData



class PhageFilter(django_filters.FilterSet):
    phage_name = django_filters.CharFilter(lookup_expr='icontains')
    phage_host_name = django_filters.CharFilter(lookup_expr='icontains')
    phage_isolator_name = django_filters.CharFilter(lookup_expr='icontains')
    submitted_year_gt = django_filters.NumberFilter(label='Year Submitted After', name='phage_submitted_date', lookup_expr='year__gt')
    submitted_month_gt = django_filters.NumberFilter(label='Month Submitted After', name='phage_submitted_date', lookup_expr='month__gt')
    submitted_year_lt = django_filters.NumberFilter(label='Year Submitted Before', name='phage_submitted_date', lookup_expr='year__lt')
    submitted_month_lt = django_filters.NumberFilter(label='Month Submitted Before', name='phage_submitted_date', lookup_expr='month__lt')
    #submitted_month_lt = django_filters.NumberFilter(label='Month Submitted Before', name='phage_submitted_date',lookup_expr='month__lt')
    #date_range_gt = django_filters.DateFilter(label='Date Submitted After', name='phage_submitted_date', lookup_expr='lt',
    #                                                  widget=forms.SelectDateWidget(attrs={'placeholder': 'YYYY/MM/DD'}))

    INCIDENT_LIVE = (
        ('0', 'Lab-A'),
        ('1', 'Lab-B'),
    )
    phage_lab = django_filters.ChoiceFilter(label='Phage Lab', choices=INCIDENT_LIVE)

    class Meta:
        model = PhageData
        fields = ['phage_name',
                  'phage_host_name',
                  'phage_isolator_name',
                  'phage_experimenter_name',
                  'phage_CPT_id',
                  'phage_isolator_loc',
                  'phage_submitted_user',
                  'phage_submitted_date',
                  'submitted_year_gt',
                  'submitted_month_gt',
                  'submitted_year_lt',
                  'submitted_month_lt',
                  'phage_lab',
                  ]
        filter_overrides = {
            models.DateField: {
                'filter_class': django_filters.DateRangeFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
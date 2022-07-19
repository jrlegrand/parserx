from django.db import models

# Create your models here.
class Sig(models.Model):
    # foreign keys
    owner = models.ForeignKey('auth.User', related_name='sigs', null=True, on_delete=models.SET_NULL)
    # time stamp
    created = models.DateTimeField(auto_now_add=True)
    # original text
    # TODO: after testing, change this to unique=True... maybe... but this might mess with version control workflow...
    sig_text = models.TextField()

    class Meta:
        ordering = ['-created']

class SigParsed(models.Model):
    # foreign keys
    sig = models.ForeignKey(Sig, related_name='sig_parsed', on_delete=models.CASCADE)
    # time stamp
    created = models.DateTimeField(auto_now_add=True)
    # version
    version = models.IntegerField(null=True)
    # sig text
    sig_text = models.TextField()
    # readable sig
    sig_readable = models.TextField(null=True)
    # method
    method = models.CharField(max_length=100, null=True)
    method_text_start = models.IntegerField(null=True)
    method_text_end = models.IntegerField(null=True)
    method_text = models.CharField(max_length=100, null=True)
    method_readable = models.CharField(max_length=100, null=True)   
    # dose
    # TODO: maybe make dose fields floats instead of chars
    dose = models.FloatField(null=True)
    dose_max = models.FloatField(null=True)
    dose_unit = models.CharField(max_length=100, null=True)
    dose_text_start = models.IntegerField(null=True)
    dose_text_end = models.IntegerField(null=True)
    dose_text = models.CharField(max_length=100, null=True)
    dose_readable = models.CharField(max_length=100, null=True)   
    # strength
    strength = models.FloatField(null=True)
    strength_max = models.FloatField(null=True)
    strength_unit = models.CharField(max_length=100, null=True)
    strength_text_start = models.IntegerField(null=True)
    strength_text_end = models.IntegerField(null=True)
    strength_text = models.CharField(max_length=100, null=True)
    strength_readable = models.CharField(max_length=100, null=True)   
    # route
    route = models.CharField(max_length=100, null=True)
    route_text_start = models.IntegerField(null=True)
    route_text_end = models.IntegerField(null=True)
    route_text = models.CharField(max_length=100, null=True)
    route_readable = models.CharField(max_length=100, null=True)   
    # frequency
    frequency = models.IntegerField(null=True)
    frequency_max = models.IntegerField(null=True)
    period = models.IntegerField(null=True)
    period_max = models.IntegerField(null=True)
    period_unit = models.CharField(max_length=100, null=True)
    time_duration = models.IntegerField(null=True)
    time_duration_unit = models.CharField(max_length=100, null=True)
    day_of_week = models.CharField(max_length=100, null=True)
    time_of_day = models.CharField(max_length=100, null=True)
    offset = models.IntegerField(null=True)
    bounds = models.IntegerField(null=True)
    count = models.IntegerField(null=True)
    frequency_text_start = models.IntegerField(null=True)
    frequency_text_end = models.IntegerField(null=True)
    frequency_text = models.CharField(max_length=100, null=True)   
    frequency_readable = models.CharField(max_length=100, null=True)   
    # when
    when = models.CharField(max_length=100, null=True)
    when_text_start = models.IntegerField(null=True)
    when_text_end = models.IntegerField(null=True)
    when_text = models.CharField(max_length=100, null=True)   
    when_readable = models.CharField(max_length=100, null=True)   
    # duration
    duration = models.IntegerField(null=True)
    duration_max = models.IntegerField(null=True)
    duration_unit = models.CharField(max_length=100, null=True)
    duration_text_start = models.IntegerField(null=True)
    duration_text_end = models.IntegerField(null=True)
    duration_text = models.CharField(max_length=100, null=True)
    duration_readable = models.CharField(max_length=100, null=True)   
    # indication
    as_needed = models.BooleanField(null=True)
    indication = models.CharField(max_length=250, null=True)
    indication_text_start = models.IntegerField(null=True)
    indication_text_end = models.IntegerField(null=True)
    indication_text = models.CharField(max_length=250, null=True)
    indication_readable = models.CharField(max_length=100, null=True)
    # max
    max_numerator_value = models.IntegerField(null=True)
    max_numerator_unit = models.CharField(max_length=100, null=True)
    max_denominator_value = models.IntegerField(null=True)
    max_denominator_unit = models.CharField(max_length=100, null=True)
    max_text_start = models.IntegerField(null=True)
    max_text_end = models.IntegerField(null=True)
    max_text = models.CharField(max_length=100, null=True)
    max_readable = models.CharField(max_length=100, null=True)
    # max_dose_per_day
    max_dose_per_day = models.FloatField(null=True)

    class Meta:
        ordering = ['-created']

STATUS_CHOICES = [(0, 'incorrect'), (1, 'missing'), (2, 'optimize')]

class SigReviewed(models.Model):
    # foreign keys
    sig_parsed = models.ForeignKey(SigParsed, related_name='sig_reviewed', null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='sigs_reviewed', null=True, on_delete=models.SET_NULL)
   # time stamp
    created = models.DateTimeField(auto_now_add=True)
    # overall sig correct
    sig_correct = models.BooleanField(null=True)
    # status of individual sig components if overall sig not correct
    method_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    dose_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    strength_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    route_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    frequency_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    duration_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    indication_status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=10)
    # theme
    themes = models.CharField(max_length=250, null=True)
    # additional notes
    notes = models.TextField(null=True)

    class Meta:
        ordering = ['-created']
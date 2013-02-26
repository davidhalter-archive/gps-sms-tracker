import re

from django.db import models
from django.forms import ValidationError


class PhoneField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(PhoneField, self).__init__(*args, **kwargs)

    def clean(self, number, model_instance):
        # remove all the crap
        number = re.sub('[^\d+]', '', number)

        # change it to one format
        if re.match('^\d{10}$', number):
            number = '+93' + number[1:]
        elif re.match('^\d{13}$', number):
            number = '+' + number[2:]

        return super(PhoneField, self).clean(number, model_instance)

    def validate(self, number, model_instance):
        if not re.match('^\+\d{11}$', number):
            raise ValidationError('Need a valid phone number!')
        return super(PhoneField, self).validate(number, model_instance)


class User(models.Model):
    name = models.CharField(max_length=200)
    phone = PhoneField(max_length=20, unique=True)
    need_register = models.BooleanField(default=True)


class Coordinate(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()

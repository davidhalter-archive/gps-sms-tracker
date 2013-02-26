import time
import re

import gammu
from django.core.management.base import BaseCommand
from django.utils.timezone import utc

from main import models


class Command(BaseCommand):
    help = 'Starts an SMS Gateway (daemon).'

    def handle(self, *args, **kwargs):
        # Create state machine object
        self.latest = None
        self.init_gammu()

        while True:
            users = models.User.objects.filter(need_register=True)
            for user in users:
                self.register(user)

            self.update_db()

            time.sleep(5)

    def init_gammu(self):
        self.sm = gammu.StateMachine()
        # Read ~/.gammurc
        self.sm.ReadConfig()
        # Connect to phone
        self.sm.Init()
        netinfo = self.sm.GetNetworkInfo()

        print('Connected to the phone:')
        print('Network name: %s' % netinfo['NetworkName'])
        print('Network code: %s' % netinfo['NetworkCode'])
        print('LAC: %s' % netinfo['LAC'])
        print('CID: %s' % netinfo['CID'])

    def update_db(self):
        def degree_to_float(deg):
            deg = float(deg) / 100
            degree = int(deg)
            part = (deg - degree) / 60 * 100
            return degree + part

        new_messages = self._fetch_sms_list()
        for message_dict in new_messages:
            number = message_dict['Number']
            text = message_dict['Text']
            users = models.User.objects.filter(phone=number)
            if not users:
                print("message: phone number not registered",
                                    number, text)
            else:
                match = re.match('\*[^*]+\*([\d.]+),E,([\d.]+),N', text)
                if not match:
                    print("message: no coordinates", number, text)
                else:
                    # why is longitude first? makes no sense.
                    longitude, latitude = match.groups()
                    dt = message_dict['DateTime'].replace(tzinfo=utc)

                    dct = {
                        'user': users[0],
                        'time': dt,
                        'latitude': degree_to_float(latitude),
                        'longitude': degree_to_float(longitude)
                    }
                    print('found coordinate', number, text)
                    if not models.Coordinate.objects.filter(**dct):
                        c = models.Coordinate(**dct)
                        c.save()

    def register(self, user):
        interval = "05"  # must be between 04-59
        password = "0000"

        # set interval "TIME OK"
        self.send_sms(user, "4" + interval + password)
        time.sleep(5)  # sleep to give the device time

        # set point to point mode
        point_to_point = "0"
        self.send_sms(user, "70" + point_to_point + password)
        time.sleep(5)

        # start tracking "GPS ON OK"
        self.send_sms(user, "222" + password)
        time.sleep(5)

        user.need_register = False
        user.save()

    def send_sms(self, user, text):
        dct = {
            'Text': unicode(text),
            'Number': user.phone,
            'SMSC': {'Location': 1}
        }
        print('Send SMS: %s' % dct)
        self.sm.SendSMS(dct)

    def _fetch_sms_list(self):
        result = []
        latest = None
        for i in range(1, 1000):
            try:
                sms_dict = self.sm.GetSMS(2, i)
            except gammu.ERR_EMPTY:
                continue
            except gammu.ERR_INVALIDLOCATION:
                break

            sms = sms_dict[0]
            # somehow all sms
            if self.latest is None or self.latest < sms['DateTime']:
                if latest is None:
                    latest = sms['DateTime']
                else:
                    latest = max(latest, sms['DateTime'])
                result.append(sms)
        if latest is not None:
            self.latest = latest
        return result

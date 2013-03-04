#!/usr/bin/env bash
python manage.py sms_gateway | tee -a sms_gateway.log &
python manage.py run_server

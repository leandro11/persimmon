#!/usr/bin/bash

export DJANGO_SETTINGS_MODULE=TTMS.settings
python -m unittest tests.units.utils.test_user
python -m unittest tests.units.management.test_staff_view

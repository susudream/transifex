# -*- coding: utf-8 -*-
from django.dispatch import Signal
from django.core.management.base import BaseCommand
from optparse import make_option
from txcron import signals
from django_addons.autodiscover import autodiscover

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--interval', '-i', default=None, dest='interval',
            help='Target signal group to execute'),
    )
    help = "Emits signals associated with crontab handlers."

    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **options):
        # We need this to connect signals
        autodiscover()
        prefix = "cron_"
        interval = options.get('interval')
        if interval:
            if prefix + interval in dir(signals):
                inst = getattr(signals, prefix + interval, None)
                inst.send(None)
                return
            else:
                print "Couldn't find signal definition",
        else:
            print "No interval specified"
        print "Valid signals are:", ", ".join([i[len(prefix):] for i in dir(signals) if i.startswith(prefix)])

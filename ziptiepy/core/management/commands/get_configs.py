# python modules
from optparse import make_option
from Exscript.util.start import quickstart

# django modules
from django.core.management.base import BaseCommand, CommandError

# ziptiepy modules
from ziptiepy.core.models import Device
from ziptiepy.adapters import adapter_map

hosts = []


def do_something(job, host, conn):
    adapter_map[device.adapter].get_config(1)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true',
            dest='all',
            default=False,
            help='Get configs for all devices'),
        make_option('--deviceid',            
            dest='device_id',
            help='Get configs for this device'),    
            
        )
    def handle(self, *args, **options):
        if options['all'] and options['device_id']:
            print ("Error: --all and --deviceid detected. Use only one")
            return
            
        if options['all']:
            devices = Device.objects.all()
        
        if options['device_id']:
            try:
                devices = Device.objects.get(pk=int(options['device_id']))
            except:
                raise CommandError('Device ID "%s" does not exist' % options['device_id'])
        
        for device in devices:
            hosts.append("ssh://" + device.access_ip)
        
        print hosts
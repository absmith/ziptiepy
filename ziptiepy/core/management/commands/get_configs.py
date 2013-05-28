# python modules
import os
from optparse import make_option
from Exscript import Host, Account, Queue, Logger
from Exscript.util.start import start
from Exscript.util.decorator import autologin
from Exscript.util.log import log_to
from Exscript.util.report  import status, summarize

# django modules
from django.core.management.base import BaseCommand, CommandError

# ziptiepy modules
from ziptiepy.core.models import Credential, Device
from ziptiepy.adapters import adapter_map
from ziptiepy.adapters import Adapter

hosts = []
logger = Logger()

@log_to(logger)
@autologin()
def do_backup(job, host, conn):
  device = host.get('device')
  config = adapter_map[device.adapter].get_config(conn)
  device.save_config(config)

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
      found_credential = False
      for credential in Credential.objects.all():
        if credential.match_ip(device.access_ip):
          found_credential = True
          host = Host(device.protocol + device.access_ip)
          account = (Account(credential.username,
                        credential.password))

          if credential.enable_username and credential.enable_password:
            account.set_authorization_password(credential.enable_password)

          host.set_account(account)
          host.set('device', device)
          hosts.append(host)
          break
      if not found_credential:
       device.backup_status = "No credentials found." % device
       device.save()

    queue = Queue(max_threads = 5, verbose = -1, stderr=open(os.devnull, 'w'))
    queue.run(hosts, do_backup)
    queue.shutdown()
    
    # Any connectiveity proablem sstatus, 
    for log in logger.get_logs():
      if log.has_error():
        device = Device.objects.get(access_ip=log.get_name())
        device.backup_status = log.get_error(False)
        device.save()


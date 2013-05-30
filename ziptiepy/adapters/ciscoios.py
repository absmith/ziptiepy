# python modules
import re
from Exscript.util.match import any_match, first_match

# ziptie modules
from ziptiepy.adapters import Adapter


class CiscoIOS(Adapter):
  """   """
  def __init__(self):
      Adapter.__init__(self, 'ciscoios')

  def backup(self, conn, device):

    device.make = 'Cisco'

    self.init(conn)

    # collect data
    running_config = self.get_running_config(conn)
    device.save_config('running-config', running_config)

    startup_config = self.get_startup_config(conn)
    device.save_config('startup-config', startup_config)


    device.hostname = first_match("".join(running_config).replace('\r','\r\n'), r'^hostname (\S+)')

    device.model, device.serial_number, \
    device.type, device.software_version = self.parse_version(conn)

    device.save()

  def init(self, conn):
    # Forcing Exscript driver
    # Had no luck using guess_os()
    conn.set_driver('ios')

    # Verify guess_os() matches expected os.
    #if conn.guess_os() != 'ios':
    #    raise Exception('unsupported os: ' + repr(conn.guess_os()))

    # autoinit() automatically executes commands to make the remote
    # system behave more script-friendly. The specific commands depend
    # on the detected operating system, i.e. on what guess_os() returns.
    conn.autoinit()

  def get_running_config(self,conn):

    conn.execute('show running-config')
    return any_match(conn, r'(.*)')[:-1]

  def get_startup_config(self,conn):

    conn.execute('show startup-config')
    return any_match(conn, r'(.*)')[:-1]

  def parse_version(self, conn):

    conn.execute('show version')

    version = first_match(conn, r'^(?:Cisco )?IOS.+Version (\S[^\s,]+)')
    if not version:
      version = first_match(conn, r'^Version\s+V(\d+\.\d+\.\d+')

    type = "Router"
    if first_match(conn, r'\b(cat|(WS|ME)-C)\d{4}|catalyst|CIGESM', re.M | re.I):
      type = "Switch"
    if first_match(conn, r'\bC1200\b|\bAIR'):
      type = "Wireless Access Point"

    model = first_match(conn, r'cisco ((?:WS-C|Cat|AS|C|VG)?\d{3,4}\S*\b)\S*\b', re.M | re.I)

    serial_number = first_match(conn, r'^Processor\s+board\s+ID\s+(\w+)')

    return [model, serial_number, type, version]

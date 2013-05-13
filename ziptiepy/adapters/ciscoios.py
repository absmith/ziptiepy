from ziptiepy.adapters import Adapter


class CiscoIOS(Adapter):
    """   """
    def __init__(self):
        Adapter.__init__(self, 'ios')
    
    def get_config(self,conn):
        return
        # Verify guess_os() matches expected os.
        if conn.guess_os() != 'ios':
            raise Exception('unsupported os: ' + repr(conn.guess_os()))
        
        # autoinit() automatically executes commands to make the remote
        # system behave more script-friendly. The specific commands depend
        # on the detected operating system, i.e. on what guess_os() returns.
        conn.autoinit()

        conn.execute('show running-config')
        
        return any_match(conn, r'(<.*>)')
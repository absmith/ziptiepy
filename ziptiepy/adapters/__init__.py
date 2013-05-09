import inspect
import imp
import os

from django.conf import settings

from ziptiepy.adapters.adapter import Adapter

adapter_classes = []
adapter_map     = {}

def _import_package_files():
    """ dynamically import all the public attributes of the python modules in this
        file's directory (the package directory) and return a list of their names
    """
    exports = []
    globals_, locals_ = globals(), locals()
    package_path = os.path.dirname(__file__)
    package_name = "ziptiepy." + os.path.basename(package_path)

    for filename in os.listdir(package_path):
        modulename, ext = os.path.splitext(filename)
        if modulename[0] != '_' and ext in ('.py', '.pyw'):
            subpackage = '{}.{}'.format(package_name, modulename)  # package relative
            module = __import__(subpackage, globals_, locals_, [modulename])
            modict = module.__dict__
            names = (modict['__all__'] if '__all__' in modict else
                     [name for name in modict if name[0] != '_'])  # all public
            exports.extend(names)
            globals_.update((name, modict[name]) for name in names)
    return exports

if __name__ != '__main__':
    __all__ = ['__all__'] + _import_package_files()  # __all__ includes itself!
    


def isadapter(o):
    return inspect.isclass(o) and issubclass(o, Adapter) and not o is Adapter

def add_adapter(cls):
    adapter = cls()
    adapter_classes.append(cls)
    adapter_map[adapter.name] = adapter

# Load built-in adapters.
for name, obj in locals().items():
    if isadapter(obj):
        add_adapter(obj)
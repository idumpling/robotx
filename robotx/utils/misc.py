"""some minor funcs"""


from pkgutil import iter_modules

import netifaces
#from fabric.colors import green
#from fabric.colors import red
#from fabric.colors import yellow


def walk_modules(path, load=False):
    """Loads a module and all its submodules from a the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.

    For example: walk_modules('scmd.utils')
    """

    mods = []
    mod = __import__(path, {}, {}, [''])
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = __import__(fullpath, {}, {}, [''])
                mods.append(submod)
    return mods


def get_ip():
    """get worker ip addrs"""
    nics = netifaces.interfaces()
    addrs = netifaces.ifaddresses(nics[1])
    worker_ip = addrs[netifaces.AF_INET][0]['addr']
    return worker_ip


def print_output(startend='', passfail='', starttime='', endtime='',
                 msg='', others=''):
    """output the info"""
    if len(msg) >= 70:
        msg = msg[:67] + '...'
    else:
        msg = msg + ' ' * (70 - len(msg))
    if startend == 'start':
        #output_info = msg + yellow(' | RUNNING |')
        output_info = msg + ' | RUNNING |'
        print '-' * 80
        print output_info
        print 'Starting Time: ', starttime
        print '-' * 80
    if startend == 'end':
        if passfail == 'PASSED':
            output_info = msg + ' | PASSED |'
        else:
            output_info = msg + ' | FAILED |'
        print '-' * 80
        print output_info
        print others
        print 'Starting Time: ', starttime
        print 'End Time:      ', endtime
        print '-' * 80

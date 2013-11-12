import os
import shutil
import sys


def copy_helper(name, directory, template_dir):
    """
    Copies either a project layout template
    into the specified directory.
    """
    top_dir = os.path.join(directory, name)
    try:
        os.mkdir(top_dir)
    except OSError as (errno, strerror):
        if errno == 17:
            sys.stderr.write('Directory %r already exists\n' % name)
        else:
            sys.stderr.write(strerror + '\n')
        return

    # Determine where the project templates are. Use
    # scmd.__path__[0] because we don't know into which directory
    # scmd has been installed.

    for d, subdirs, files in os.walk(template_dir):
        relative_dir = d[len(template_dir)+1:]
        if relative_dir:
            os.mkdir(os.path.join(top_dir, relative_dir))
        for subdir in subdirs[:]:
            if subdir.startswith('.'):
                subdirs.remove(subdir)
        for f in files:
            if f.endswith('.pyc') or f.endswith('empty'):
                # Ignore .pyc, .empty files
                continue
            path_old = os.path.join(d, f)
            path_new = os.path.join(top_dir, relative_dir, f)
            try:
                shutil.copy(path_old, path_new)
                _make_writeable(path_new)
            except OSError:
                sys.stderr.write("Notice: Couldn't set permission bits on %s. \
                        You're probably using an uncommon filesystem setup. \
                        No problem.\n" % path_new)


def _make_writeable(filename):
    """
    Make sure that the file is writeable. Useful if our source is
    read-only.
    """
    import stat
    if sys.platform.startswith('java'):
        # On Jython there is no os.access()
        return
    if not os.access(filename, os.W_OK):
        st = os.stat(filename)
        new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
        os.chmod(filename, new_permissions)


if __name__ == '__main__':
    from ipdb import set_trace
    set_trace()
    name = 'just_test'
    directory = os.getcwd()
    from robotx import template
    template_dir = os.path.join(template.__path__[0], 'project_template')
    copy_helper(name, directory, template_dir)

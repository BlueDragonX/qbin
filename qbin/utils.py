"""
Common utility functions used by the application.
"""

import os
import random
import string
import subprocess
from .errors import ExecutionError


def execute(args, exitcode=0, redirect=True):
    """
    Return the output of a command. Raise a ExecuteError if the exit code does
    not match exitcode. By default stderr is redirected to stdout. Set redirect
    to False to avoid this behavior.
    """
    got_exitcode = 0
    stderr = None
    if redirect:
        stderr = subprocess.STDOUT

    try:
        output = subprocess.check_output(args, stderr=stderr)
    except subprocess.CalledProcessError as e:
        output = e.output
        got_exitcode = e.returncode

    if got_exitcode != exitcode:
        raise ExecutionError(args, got_exitcode, output)
    return output


def mount(source, directory, fstype=None, bind=False, options=[]):
    """
    Mount a filesystem. Paremeters are:

        source -- The device or source directory to mount.
        directory -- The directory path to mount the filesystem at.
        fstype -- The filesystem type. Defaults to auto.
        bind -- True if this is a bind mount. Will bind recursively (rbind).
        options -- A list of mount options.

    Raise an ResourceError if the mount fails. The ResourceError will have its
    resource set to the mount directory and the mount error message as the
    reason.
    """
    args = ['mount']
    if fstype:
        args += ['-t', fstype]
    if bind:
        args += ['--rbind']
    args += [source, directory]
    execute(args)


def umount(directory, lazy=False):
    """
    Unmount a filesystem. Set lazy to True to perform a lazy unmount. Raise a
    ResourceError if the unmount fails. The ResourceError will have its
    resource set to the umount directory and the umount error message as the
    reason.
    """
    args = ['umount']
    if lazy:
        args.append('-l')
    args.append(directory)
    execute(args)


def untar(archive, directory, preserve=False):
    """
    Extract the contents of a tar archive to the given directory and optionally
    preserve archive permissions.
    """
    flags = 'xf'
    if preserve:
        flags = 'p%s' % flags
    args = ['tar', flags, archive, '-C', directory]
    execute(args)


def randstr(length):
    """
    Return a randomly generated string of letters (lower and uppercase) and
    numbers with the given length.
    """
    chars = string.letters + string.digits
    return ''.join([random.choice(chars) for x in range(length)])


def mkdir(directory, mode=0755):
    """
    Create a directory and its parents if they do not exist. The create mode
    may be given and defaults to 0755. Return True if the directory was created
    or False if it already existed. Raised OSError on failure.
    """
    path = os.path.abspath(directory)
    if os.path.isdir(path):
        return False
    os.makedirs(path, mode)
    return True


def mktempdir(prefix='', mode=0777):
    """
    Create a directory under /tmp and return its absolute path. The directory
    name will consist of qbin_ followed by the prefix (of provided) and finally
    a randome string. Raise OSError on creation failure or RuntimeError if we
    exceed the number of attempts to create a directory.
    """
    prefix = 'qbin_%s' % prefix
    for x in range(10):
        name = prefix + randstr(8)
        path = os.path.join('/tmp', name)
        if not os.path.exists(path):
            mkdir(path, mode)
            return path
    raise RuntimeError('not enough entropy to create temporary directory')

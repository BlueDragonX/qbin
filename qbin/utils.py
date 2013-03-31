"""
Common utility functions used by the application.
"""

import subprocess
from .errors import ExecuteError


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
        raise ExecuteError(args, got_exitcode, output)
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


def umount(directory):
    """
    Unmount a filesystem. Raise a ResourceError if the unmount fails. The
    ResourceError will have its resource set to the umount directory and the
    umount error message as the reason.
    """
    args = ['umount', directory]
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

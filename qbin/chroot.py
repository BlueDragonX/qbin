"""
Utilities for managing chroots.
"""

import os
import shutil
import subprocess
from StringIO import StringIO
from .errors import ExecutionError
from .utils import mkdir, mktempdir, mount, umount, untar


class Chroot(object):
    """
    Manage a single chroot.
    """

    def __init__(self, root):
        """
        Construct a chroot rooted at the given path.
        """
        self.root = root
        self.tmp = self.locate_tmp_source()

    def locate_tmp_source(self):
        """
        Locate the tmp mount source for this chroot or None if it has not been
        created.
        """
        dest = self.path('/tmp')
        with open('/etc/mtab') as mtab:
            for line in mtab:
                parts = line.split(' ')
                if parts[1] == dest:
                    return parts[0]
        return None

    def path(self, path):
        """
        Return an absolute path to a file in the chroot. Path should be
        absolute in relation to the chroot. No checks are done to ensure the
        paths exist.
        """
        if path[:len(os.sep)] == os.sep:
            path = path[len(os.sep):]
        return os.path.join(self.root, path)

    def is_created(self):
        """
        Return True if the chroot exists or False.
        """
        return os.path.isdir(self.root) and os.listdir(self.root)

    def create(self, stage, portage):
        """
        Create the chroot if it does not eixist. Use the provided stage and
        portage tarball paths. Does not start() the chroot. Return True on
        success or False if the chroot exists. Raise OSError if the chroot
        directory cannot be created. Raise ExecuteError if the provided
        tarballs fail to extract.
        """
        if self.is_created():
            return False

        resolv = '/etc/resolv.conf'
        mkdir(self.root)
        untar(stage, self.root, True)
        untar(portage, self.path('/usr'))
        shutil.copy(resolv, self.path(resolv))
        return True

    def destroy(self):
        """
        Delete a chroot. Return True on success or False if it does not exist.
        """
        if not self.is_created():
            return False

        self.stop()
        shutil.rmtree(self.root)
        return True

    def is_started(self):
        """
        Return True if the chroot has been started or False.
        """
        return self.tmp

    def start(self):
        """
        Start the chroot. Return True on success or False if already started.
        Raise OSError if tmp directory creation fails. Raise ExecuteError on
        mount failure.
        """
        if self.is_started():
            return False

        self.tmp = mktempdir('chroot_')
        mount('/dev', self.path('/dev'), bind=True)
        mount('none', self.path('/proc'), fstype='proc')
        mount('/sys', self.path('/sys'), bind=True)
        mount(self.tmp, self.path('/tmp'), bind=True)
        return True

    def stop(self):
        """
        Stop the chroot. Return True on success or False if not started. Raise
        ExecuteError on umount failures.
        """
        if not self.is_started():
            return False

        mounts = [
            '/dev',
            '/proc',
            '/sys',
            '/tmp',
        ]

        for mount in mounts:
            try:
                umount(self.path(mount), True)
            except ExecutionError:
                pass
        shutil.rmtree(self.tmp)
        self.tmp = None
        return True

    def call(self, args, checkcode=None, stdin=None, stdout=None, stderr=None):
        """
        Call the command specified by args in the chroot and return the exit
        code.

        Settings checkcode will cause the method to raise an ExecutionError if
        the exit code does not match this value. In this case the only value
        the method will return is the value of checkcode. Raise a ValueError if
        checkcode cannot be coerced to an integer.

        The stdin, stdout, and stderr params may be set to perform I/O
        redirection. This method uses subprocess.call() to perform the
        execution and so the valid values for stdout, stderr, and stdin are the
        same.
        """
        if not args:
            raise ValueError('args may not be an empty value')

        if checkcode is not None:
            checkcode = int(checkcode)

        chrootargs = ['chroot', self.root] + args
        exitcode = subprocess.call(
            chrootargs, stdout=stdout, stderr=stderr, stdin=stdin, shell=False)

        if checkcode is not None and checkcode != exitcode:
            raise ExecutionError(args, exitcode)
        return exitcode

    def call_output(self, args, checkcode=None, stdin=None, stderr=None):
        """
        Call the command specified by args in the chroot and return a
        two-tupple containing the command's exit code and stdout output.

        Aside from the stdout param, which is removed, all parameters are
        identical in usage to call(). The stderr param may be set to
        subprocess.STDOUT to have its output captured and returned.
        """
        if not args:
            raise ValueError('args may not be an empty value')

        if checkcode is not None:
            checkcode = int(checkcode)

        output = None
        with StringIO() as output_buffer:
            chrootargs = ['chroot', self.root] + args
            exitcode = subprocess.call(
                chrootargs, stdout=output_buffer, stderr=stderr, stdin=stdin,
                shell=False)
            output = output_buffer.getvalue()

        if checkcode is not None and checkcode != exitcode:
            raise ExecutionError(args, exitcode, output)
        return (exitcode, output)

    def __str__(self):
        """
        Convert the object into a printable string.
        """
        return "chroot at '%s'" % self.root

    def __repr__(self):
        """
        Return a string representation of the object.
        """
        return "<Chroot(%s)>" % repr(self.root)

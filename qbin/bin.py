"""
Application entry points.
"""

import sys
from chroot import Chroot
from utils import mkdir, mount, umount, untar


def test_mount():
    """
    Ad-hoc mount test.
    """
    mkdir('/tmp/a')
    mkdir('/tmp/b')
    mount('/tmp/a', '/tmp/b', bind=True)
    umount('/tmp/b')


def test_untar():
    """
    Ad-hoc untar test.
    """
    archives = [
        ('/tmp/stage3-amd64-20130321.tar.bz2', True),
        ('/tmp/portage-latest.tar.bz2', False)
    ]

    dest = '/tmp/stage3'
    mkdir(dest)
    for archive, preserve in archives:
        print("Extracting %s..." % archive)
        untar(archive, dest, preserve)


def test_chroot_create():
    """
    Ad-hoc chroot creation test.
    """
    stage3 = (
        '/home/sadpengu/Sandbox/packages/qbin/assets/'
        'stage3-amd64-20130321.tar.bz2')
    portage = (
        '/home/sadpengu/Sandbox/packages/qbin/assets/'
        'portage-latest.tar.bz2')
    chroot = Chroot('/tmp/chroot')
    if chroot.create(stage3, portage):
        print("Created chroot at %s" % chroot.root)
    else:
        print("Chroot already exists at %s" % chroot.root)


def test_chroot_destroy():
    """
    Ad-hoc chroot destroy test.
    """
    chroot = Chroot('/tmp/chroot')
    if chroot.destroy():
        print("Destroyed chroot at %s" % chroot.root)
    else:
        print("Chroot does not exist at %s" % chroot.root)


def test_chroot_start():
    """
    Ad-hoc chroot start test.
    """
    chroot = Chroot('/tmp/chroot')
    if chroot.start():
        print("Started chroot with tmp %s" % chroot.tmp)
    else:
        print("Chroot already started with tmp %s" % chroot.tmp)


def test_chroot_stop():
    """
    Ad-hoc chroot stop test.
    """
    chroot = Chroot('/tmp/chroot')
    tmp = chroot.tmp
    if chroot.stop():
        print("Stopped chroot with tmp %s" % tmp)
    else:
        print("Chroot already stopped")


def test_chroot_call():
    """
    Ad-hoc chroot call test.
    """
    chroot = Chroot('/tmp/chroot')
    sys.exit(chroot.call(sys.argv[1:]))

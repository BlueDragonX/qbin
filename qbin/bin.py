"""
Application entry points.
"""

import sys
from buildroot import BuildRoot
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


def test_buildroot_create():
    """
    Ad-hoc buildroot creation test.
    """
    stage3 = (
        '/home/sadpengu/Sandbox/packages/qbin/assets/'
        'stage3-amd64-20130321.tar.bz2')
    portage = (
        '/home/sadpengu/Sandbox/packages/qbin/assets/'
        'portage-latest.tar.bz2')
    buildroot = BuildRoot('/tmp/buildroot')
    if buildroot.create(stage3, portage):
        print("Created buildroot at %s" % buildroot.root)
    else:
        print("BuildRoot already exists at %s" % buildroot.root)


def test_buildroot_destroy():
    """
    Ad-hoc buildroot destroy test.
    """
    buildroot = BuildRoot('/tmp/buildroot')
    if buildroot.destroy():
        print("Destroyed buildroot at %s" % buildroot.root)
    else:
        print("BuildRoot does not exist at %s" % buildroot.root)


def test_buildroot_start():
    """
    Ad-hoc buildroot start test.
    """
    buildroot = BuildRoot('/tmp/buildroot')
    if buildroot.start():
        print("Started buildroot with tmp %s" % buildroot.tmp)
    else:
        print("BuildRoot already started with tmp %s" % buildroot.tmp)


def test_buildroot_stop():
    """
    Ad-hoc buildroot stop test.
    """
    buildroot = BuildRoot('/tmp/buildroot')
    tmp = buildroot.tmp
    if buildroot.stop():
        print("Stopped buildroot with tmp %s" % tmp)
    else:
        print("BuildRoot already stopped")


def test_buildroot_call():
    """
    Ad-hoc buildroot call test.
    """
    buildroot = BuildRoot('/tmp/buildroot')
    sys.exit(buildroot.call(sys.argv[1:]))

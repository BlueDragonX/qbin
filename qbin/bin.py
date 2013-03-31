"""
Application entry points.
"""

import os
from utils import mount, umount, untar


def mkdir(dir):
    try:
        os.makedirs(dir)
    except OSError:
        pass


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

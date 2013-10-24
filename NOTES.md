Dev Notes
=========

Phase 1 Features
----------------
* decide on an API implementation
  - JSON is suitable
  - HTTP? How do we secure this? Easy to implement.
  - BSD socket? How do we implement this? Easy to secure.
* build server
  - build packages in chroot
  - query package status and details
  - update existing packages
* chroot build environment
  - single chroot
  - create and delete
  - copy parent make.conf
* cli admin tool
  - explicitly build packages
  - remove packages
  - query package list
  - query package details
* cli client tool
  - install packages
  - build missing packages
  - verify use flags

Phase 2 Features
----------------
* build server
  - operate on specific chroot
  - manage chroots
  - scheduled updates
  - auto-purge packages
* chroot build environment
  - support multiple chroots
  - manage make.conf file
  - manage package.* files
  - package deduplication
* cli admin tool
  - manage chroots
* cli client tool
  - update system

Phase 1 Design
--------------
* chroot
  - low level
    - manage chroot paths
    - manage chroot files
    - mount chroot dirs
    - execute in chroot
* package manager
  - build package(s)
  - query package(s)
  - remove package(s)

What's Going On
---------------
Emerge a package:
- 

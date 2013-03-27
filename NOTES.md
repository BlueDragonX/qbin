Dev Notes
=========

Phase 1 Features
----------------
* device on an API implementation
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
  - manage global use flags
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
  - manage package.* files
* cli admin tool
  - manage chroots
* cli client tool
  - update system

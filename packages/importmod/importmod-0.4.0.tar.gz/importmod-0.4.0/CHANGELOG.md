# Changelog

## [0.4.0] 2021-05-31

### Dependencies
- Removed dependency on outdated omwcmd by re-implemented the function it was needed for in python.
- Updated to work with portmod 2.0_rc10

### New
- Added update checking for packages hosted on GitLab and GitHub.
  This only works when checking for updates of all packages, not for checking packages
  updated within a period.
- Added detection of file changes on Nexus even without version bumps

### Changed
- InstallDirs in the package generator output will be sorted by source file name and path.

### Bugfixes
- Made the update checker report the newest version of a package in the database,
  rather than the first version encountered

## [0.3.0] 2020-06-25

### Dependencies
- Requires RedBaron

### New Features
- Made pybuild generation use old version as a starting point.
- Refactored interface to use `importmod` as main command, with subcommands for importing mods and update detection.
- Added subcommand to validate NexusMods files (i.e. check that the files in the portmod repo match the files on NexusMods).
- Added subcommand to scan textures to determine a texture size that can be used in Portmod.

### Bugfixes
- Fixed bug in parsing updates from mw.modhistory.com
- Fixed parsing of version numbers and atoms from NexusMods
- Fixed handling of exceptions when parsing NexusMods mods
- Fixed incorrect separator in update output
- Use source name (minus extension) in InstallDir.S when generating pybuilds
- Parse numeric components of atoms as integers to remove leading zeroes.
- Fixed suffix parsing so that "_alpha" suffixes aresn't considered corruptions of "_p"
- Ignore old versions of Nexus files when detecting the latest version numbers
  (Oddly, some mods have old versions with larger version numbers).
- Fixed omwcmd dds command syntax to match newest version.

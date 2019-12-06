Changelog
=========

2.4 - Unreleased
----------------

- Add Python 3.8 to tox.ini. Remove old Python versions.
  [stefan]

- Fix escape sequence warning in byte string literal.
  [stefan]


2.3 - 2019-02-08
----------------

- Add MANIFEST.in.
  [stefan]

- Release as wheel.
  [stefan]

- Drop explicit GPL because the PSF license is GPL-compatible anyway.
  [stefan]

2.2 - 2017-02-05
----------------

- Support Python 2.6-3.6 without 2to3.
  [stefan]

2.1 - 2014-04-19
----------------

- Remove setuptools from install_requires because it isn't.
  [stefan]

2.0 - 2012-04-27
----------------

- Open /dev/tty in binary mode under Python 3.
  [stefan]

- Disable buffering if the device is not seekable.
  [stefan]

- Remove getmaxyx since it cannot be implemented reliably.
  [stefan]

- Support Python 2.5.
  [stefan]

- Change license to GPL or PSF to avoid relicensing of PSF code.
  [stefan]

1.0 - 2012-04-11
----------------

- Initial release.
  [stefan]

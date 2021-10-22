Changelog
=========

3.0 - Unreleased
----------------

- Add Python 3.8-3.10 to tox.ini. Remove old Python versions.
  [stefan]

- Replace deprecated ``python setup.py test`` in tox.ini.
  [stefan]

- Remove deprecated ``test_suite`` from setup.py.
  [stefan]

- Fix escape sequence warning in byte string literal.
  [stefan]

- Open /dev/tty in binary mode under both Python 2 and 3.
  [stefan]

- Officially change opentty's bufsize argument default from 1 to -1.
  Under Python 3, 1 has effectively meant -1 all along but Python 3.8
  now issues a warning.
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

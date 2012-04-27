from setuptools import setup, find_packages

version = '2.0'

setup(name='term',
      version=version,
      description='An enhanced version of the tty module',
      long_description=open('README.txt').read() + '\n' +
                       open('CHANGES.txt').read(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      keywords='terminal tty raw cbreak opentty getyx cursor position',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='http://pypi.python.org/pypi/term',
      license='GPL or PSF',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      use_2to3=True,
      test_suite='term.tests',
      install_requires=[
          'setuptools',
      ],
)

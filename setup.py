from setuptools import setup, find_packages

version = '3.0'

setup(name='term',
      version=version,
      description='An enhanced version of the tty module',
      long_description=open('README.rst').read() + '\n' +
                       open('CHANGES.rst').read(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      keywords='terminal tty raw cbreak opentty getyx cursor position',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='https://github.com/stefanholek/term',
      project_urls={
          'Documentation': 'https://term.readthedocs.io/en/stable',
          'Issue Tracker': 'https://github.com/stefanholek/term/issues',
          'Source Code': 'https://github.com/stefanholek/term',
      },
      license='PSF-2.0',
      packages=find_packages(),
      zip_safe=True,
)

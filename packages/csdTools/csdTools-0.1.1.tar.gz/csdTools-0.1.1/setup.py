from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

version = '0.1.1'
short_des = ('A collection of scripts wrapping scipy.signal.csd for some '
             + 'extra features. Most notably, wrapped csd allows one to have'
             + ' more averaging in higher frequency bins of spectrum while '
             + 'getting same number of points per decade.')
dwnld_url = ('https://gitlab.com/anchal-physics/csdTools/-/archive/'
             + version + '/csdtools-' + version + '.tar.gz')
# Chose either "3 - Alpha" or "4 - Beta"
# or "5 - Production/Stable" as the current state of your package
classifiers = ['Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'Topic :: Software Development :: Build Tools',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python :: 3']

setup(name='csdTools',
      packages=['csdTools'],
      version=version,
      license='LICENSE',
      description=short_des,
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Anchal Gupta',
      author_email='anchal@caltech.edu',
      url='https://gitlab.com/anchal-physics/csdTools',
      download_url=dwnld_url,
      keywords=['CSD', 'SCIPY', 'UNCERTAINTY', 'STANDARD DEVIATION'],
      install_requires=['numpy', 'scipy'],
      classifiers=classifiers)

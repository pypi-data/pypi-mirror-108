""" Build ``ckitoolz`` with or without Cython.

By default, CyToolz will be built using Cython if available.
If Cython is not available, then the default C compiler will be used
to compile the distributed *.c files instead.

Pass "--cython" or "--with-cython" as a command line argument to setup.py to
force the project to build using Cython (and fail if Cython is unavailable).

Pass "--no-cython" or "--without-cython" to disable usage of Cython.

For convenience, developmental versions (with 'dev' in the version number)
automatically use Cython unless disabled via a command line argument.

To summarize differently, the rules are as follows (apply first applicable rule):

  1. If `--no-cython` or `--without-cython` are used, then only build from `.*c` files.
  2. If this is a dev version, then cythonize only the files that have changed.
  3. If `--cython` or `--with-cython` are used, then force cythonize all files.
  4. If no arguments are passed, then force cythonize all files if Cython is available,
     else build from `*.c` files.  This is default when installing via pip.

By forcing cythonization of all files (except in dev) if Cython is available,
we avoid the case where the generated `*.c` files are not forward-compatible.

"""
import os.path
import sys
from setuptools import setup, Extension, Command, find_packages
from shutil import rmtree
import os

here = os.path.abspath(os.path.dirname(__file__))

class UploadCommand(Command):
    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Removing build files...")
        os.system("rm -rf *.egg-info")
        os.system("rm -rf build")
        os.system("rm -rf dist")

        # self.status("Pushing git tags…")
        # os.system("git tag v{0}".format(about["__version__"]))
        # os.system("git push --tags")

        sys.exit()


class InstallCommand(Command):
    description = 'Build and install the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and install to local…')
        os.system('{0} setup.py install'.format(sys.executable))

        self.status('Removing build files...')
        os.system('rm -rf *.egg-info')
        os.system('rm -rf build')
        os.system('rm -rf dist')

        sys.exit()

about = {}
VERSION = None
FOLDER = "ckitoolz"
if not VERSION:
    with open(os.path.join(here, FOLDER, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


info = {}
filename = os.path.join('ckitoolz', '_version.py')
exec(compile(open(filename, "rb").read().replace(b'\r\n', b'\n'),
             filename, 'exec'), info)
VERSION = info['__version__']

try:
    from Cython.Build import cythonize
    has_cython = True
except ImportError:
    has_cython = False

use_cython = True
is_dev = 'dev' in VERSION
strict_cython = is_dev
if '--no-cython' in sys.argv:
    use_cython = False
    sys.argv.remove('--no-cython')
if '--without-cython' in sys.argv:
    use_cython = False
    sys.argv.remove('--without-cython')
if '--cython' in sys.argv:
    strict_cython = True
    sys.argv.remove('--cython')
if '--with-cython' in sys.argv:
    strict_cython = True
    sys.argv.remove('--with-cython')

if use_cython and not has_cython:
    if strict_cython:
        raise RuntimeError('Cython required to build dev version of ckitoolz.')
    print('ALERT: Cython not installed.  Building without Cython.')
    use_cython = False

if use_cython:
    suffix = '.pyx'
else:
    suffix = '.c'

ext_modules = []
for modname in ['dicttoolz', 'functoolz', 'itertoolz', 'recipes', 'utils']:
    ext_modules.append(Extension('ckitoolz.' + modname.replace('/', '.'),
                                 ['ckitoolz/' + modname + suffix]))

if use_cython:
    try:
        from Cython.Compiler.Options import get_directive_defaults
        directive_defaults = get_directive_defaults()
    except ImportError:
        # for Cython < 0.25
        from Cython.Compiler.Options import directive_defaults
    directive_defaults['embedsignature'] = True
    directive_defaults['binding'] = True
    directive_defaults['language_level'] = '3'  # TODO: drop Python 2.7 and update this (and code) to 3
    # The distributed *.c files may not be forward compatible.
    # If we are cythonizing a non-dev version, then force everything to cythonize.
    # ext_modules = cythonize(ext_modules)
    ext_modules = cythonize(ext_modules, force=not is_dev)

setup(
    name='ckitoolz',
    cmdclass={
          # $ python setup.py pypi    # upload repository to pypi
          "pypi": UploadCommand,
          'get': InstallCommand,  # install package to local
      },
    version=VERSION,
    description=('Cython implementation of Kitoolz: '
                    'High performance functional utilities'),
    ext_modules=ext_modules,
    long_description=(open('README.rst').read()
                        if os.path.exists('README.rst')
                        else ''),
    # long_description_content_type="text/markdown",
    long_description_content_type="text/x-rst",
    url='https://github.com/szj2ys/ckitoolz.git',
    author='https://raw.github.com/pytoolz/cytoolz/master/AUTHORS.md',
    author_email='erik.n.welch@gmail.com',
    maintainer='Erik Welch',
    maintainer_email='erik.n.welch@gmail.com',
    license = 'BSD',
    packages=['ckitoolz', 'ckitoolz.curried'],
    package_data={'ckitoolz': ['*.pyx', '*.pxd', 'curried/*.pyx', 'tests/*.py']},
    # include_package_data = True,
    keywords=('functional utility itertools functools iterator generator '
                'curry memoize lazy streaming bigdata cython toolz ckitoolz'),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    install_requires=['kitoolz >= 0.1.2'],
    extras_require={'cython': ['cython']},
    python_requires=">=3.5",
    zip_safe=False,
)

import os
import sys
import re
import glob
from setuptools import setup, find_packages, Command
from shutil import rmtree


here = os.path.abspath(os.path.dirname(__file__))
VERSION = None
FOLDER = "exceling"
about = {}
if not VERSION:
    with open(os.path.join(here, FOLDER, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

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

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

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

# long_description: Take from README file
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

# Version Number
with open(os.path.join(os.path.dirname(__file__), 'exceling', '__init__.py')) as f:
    version = re.compile(r".*__version__ = '(.*?)'", re.S).match(f.read()).group(1)

# Dependencies
if sys.platform.startswith('win'):
    if sys.version_info[:2] >= (3, 7):
        pywin32 = 'pywin32 >= 224'
    else:
        pywin32 = 'pywin32'
    install_requires = [pywin32]
    # This places dlls next to python.exe for standard setup and in the parent folder for virtualenv
    data_files = [('', glob.glob('exceling*.dll'))]
elif sys.platform.startswith('darwin'):
    install_requires = ['psutil >= 2.0.0', 'appscript >= 1.0.1']
    data_files = [(os.path.expanduser("~") + '/Library/Application Scripts/com.microsoft.Excel', ['exceling/exceling.applescript'])]
else:
    if os.environ.get('READTHEDOCS', None) == 'True' or os.environ.get('INSTALL_ON_LINUX') == '1':
        data_files = []
        install_requires = []
    else:
        raise OSError("exceling requires an installation of Excel and therefore only works on Windows and macOS. To enable the installation on Linux nevertheless, do: export INSTALL_ON_LINUX=1; pip install exceling")

extras_require = {
    'pro': ['cryptography', 'Jinja2'],
    'all': ['cryptography', 'pandas', 'matplotlib', 'flask', 'pillow']
}

setup(
    name='exceling',
    version=about["__version__"],
    url='https://www.xlwings.org',
    license='BSD 3-clause',
    author='Zoomer Analytics LLC',
    author_email='felix.zumstein@zoomeranalytics.com',
    description='Make Excel fly: Interact with Excel from Python and vice versa.',
    long_description=readme,
    data_files=data_files,
    packages=find_packages(exclude=('tests', 'tests.*',)),
    package_data={'exceling': ['exceling.bas', '*.xlsm', '*.xlam', 'exceling.applescript', 'addin/exceling.xlam', 'addin/xlwings_unprotected.xlam']},
    keywords=['xls', 'excel', 'spreadsheet', 'workbook', 'vba', 'macro'],
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={'console_scripts': ['exceling=exceling.cli:main'],},
    cmdclass={
        # $ python setup.py pypi    # upload repository to pypi
        "pypi": UploadCommand,
        'get': InstallCommand,   # install package to local
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'License :: OSI Approved :: BSD License'],
    platforms=['Windows', 'Mac OS X'],
    python_requires='>=3.6',
)

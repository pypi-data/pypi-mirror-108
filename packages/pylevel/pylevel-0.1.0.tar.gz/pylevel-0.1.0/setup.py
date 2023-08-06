import sys
from setuptools import setup, Command

try:
    from setuptools_rust import RustExtension
except ImportError:
    import subprocess

    errno = subprocess.call([sys.executable, "-m", "pip", "install", "setuptools-rust==0.11.6"])
    if errno:
        print("Please install setuptools-rust package")
        raise SystemExit(errno)
    else:
        from setuptools_rust import RustExtension


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        '''
        Finds all the tests modules in tests/, and runs them.
        '''
        from pylevel import tests
        import unittest
        unittest.main(tests, argv=sys.argv[:1])


cmdclass = {'test': TestCommand}


setup_requires = ["setuptools-rust>=0.11", "wheel"]
install_requires = []

setup(
    name="pylevel",
    version= __import__('pylevel').__version__,
    description='A LevelDB driver',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url='http://github.com/nakagami/pylevel/',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Rust",
        "Operating System :: POSIX",
    ],
    keywords=['LevelDB'],
    license='MIT',
    author='Hajime Nakagami',
    author_email='nakagami@gmail.com',
    packages=["pylevel"],
    rust_extensions=[RustExtension("pylevel.rslevel")],
    setup_requires=setup_requires,
    zip_safe=False,
    cmdclass=cmdclass,
)

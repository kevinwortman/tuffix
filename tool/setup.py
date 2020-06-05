# this is just a hello-world-grade setup.py, needs work!
import setuptools
setuptools.setup(
    name='tuffix',
    version='0.0.0',
    packages=setuptools.find_packages(),

    install_requires=['packaging', 'pyfakefs', 'python-apt']
)

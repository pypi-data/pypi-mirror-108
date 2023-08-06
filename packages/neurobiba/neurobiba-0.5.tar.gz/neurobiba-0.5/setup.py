from setuptools import setup, find_packages
from setuptools.command.install import install as InstallCommand

class Install(InstallCommand):
    """ Customized setuptools install command which uses pip. """

    def run(self, *args, **kwargs):
        import pip
        pip.main(['install', '.'])
        InstallCommand.run(self, *args, **kwargs)
        
setup(
    name='neurobiba',
    version='0.5',
    description='small collection of functions for neural networks',
    url='https://github.com/displaceman/neurobiba',
    author_email='cumnaamys@gmail.com',
    author='displaceman',
    license='GPL',
    cmdclass={
        'install': Install,
    },
    packages=find_packages(),
    install_requires=['simplejson'],
    zip_safe=False)

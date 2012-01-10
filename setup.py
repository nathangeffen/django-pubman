from distutils.core import setup

setup(
    name='django-pubman',
    version='0.5beta',
    description='A simple content management system for Django.',
    author='Nathan Geffen',
    author_email='nathangeffen@gmail.com',
    url='https://launchpad.net/django-pubman',    
    packages=['pubman',],
    license='MIT',
    long_description=open('README').read(),
)

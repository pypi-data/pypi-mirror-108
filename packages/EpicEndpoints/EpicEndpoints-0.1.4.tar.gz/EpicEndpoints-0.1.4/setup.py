from setuptools import setup

setup(
   name='EpicEndpoints',
   version='0.1.4',
   description=""" An easy way to access Epic Games\' endpoints without clutter. """,
   long_description_content_type="text/markdown",
   long_description=open('README.md').read(),
   url='https://github.com/AtomicXYZ/EpicEndpoints',
   author='AtomicXYZ',
   packages=['EpicEndpoints'],
   
   license='LICENSE',
   
   install_requires=[
       "requests",
   ],
   project_urls = {
    'Documentation': 'https://github.com/AtomicXYZ/EpicEndpoints',
   }
)
from setuptools import setup

setup(name='validaus',
      version='0.1.6',
      description='Validaus Python Module',
      url='https://www.validaus.com',
      author='Validaus Inc.',
      license='MIT',
      packages=['validaus'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
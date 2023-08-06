import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(name='django-quickstarter',
      version='0.1',
      packages=find_packages(exclude=[
          'docs',
      ]),
      description='Django-based project boilerplate that follows best practices',
      long_description=README,
      url='https://www.example.com/',
      author='John Doe',
      author_email='test' '@' 'exmaple.com',
      license='MIT',

      classifiers=[
          'Development Status :: 3 - Alpha',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],

      install_requires=[
          'Django',
          'django-crispy-forms',
      ],
      setup_requires=[
      ],
      scripts=[
          'manage.py',
      ],
      )
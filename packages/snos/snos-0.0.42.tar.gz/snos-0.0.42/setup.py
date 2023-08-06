from setuptools import setup, find_namespace_packages

setup(name='snos',
      description='Command line tool for keeping notes simple way.',
      long_description='Command line tool for keeping notes simple way.',
      version='0.0.42',
      url='https://github.com/ferdielik/snos',
      author='Ferdi Elik',
      author_email='elik.ferdi@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3'
      ],
      scripts=['snos/snos'],
      packages=find_namespace_packages(include=['snos'])
      )
